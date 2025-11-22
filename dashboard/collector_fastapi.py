import sqlite3
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
import json
import time
import gzip
from datetime import datetime
from typing import List, Dict, Any, Optional
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2
from google.protobuf.json_format import MessageToDict

app = FastAPI(title="Humainze OTLP Collector & API")

# Configuração do Banco de Dados SQLite
DB_NAME = "humainze_metrics.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabela simples para armazenar métricas achatadas
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (timestamp DATETIME, 
                  service_name TEXT, 
                  metric_name TEXT, 
                  value REAL, 
                  unit TEXT, 
                  attributes TEXT)''')
    
    # Tabela para Traces (Spans)
    c.execute('''CREATE TABLE IF NOT EXISTS traces
                 (timestamp DATETIME, 
                  trace_id TEXT,
                  span_id TEXT,
                  parent_span_id TEXT,
                  service_name TEXT, 
                  operation_name TEXT, 
                  duration_ms REAL, 
                  status_code TEXT,
                  attributes TEXT)''')

    # Tabela para Logs
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (timestamp DATETIME, 
                  service_name TEXT, 
                  severity_text TEXT, 
                  body TEXT, 
                  attributes TEXT)''')

    conn.commit()
    conn.close()

init_db()

def save_metric(timestamp, service_name, metric_name, value, unit, attributes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?)", 
              (timestamp, service_name, metric_name, value, unit, json.dumps(attributes)))
    conn.commit()
    conn.close()

def save_trace(timestamp, trace_id, span_id, parent_span_id, service_name, operation_name, duration_ms, status_code, attributes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO traces VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (timestamp, trace_id, span_id, parent_span_id, service_name, operation_name, duration_ms, status_code, json.dumps(attributes)))
    conn.commit()
    conn.close()

def save_log(timestamp, service_name, severity_text, body, attributes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", 
              (timestamp, service_name, severity_text, body, json.dumps(attributes)))
    conn.commit()
    conn.close()

# --- OTLP Receiver ---

@app.post("/v1/metrics")
async def receive_metrics(request: Request):
    try:
        body = await request.body()
        
        # 1. Decompress GZIP if needed
        if 'gzip' in request.headers.get('content-encoding', ''):
            try:
                body = gzip.decompress(body)
            except Exception as e:
                print(f"Erro ao descomprimir GZIP: {e}")
        
        # 2. Detectar Formato (Protobuf vs JSON)
        content_type = request.headers.get('content-type', '')
        data = {}

        # Tenta Protobuf primeiro (padrão do OTel HTTP)
        if 'application/x-protobuf' in content_type or not body.startswith(b'{'):
            try:
                request_proto = metrics_service_pb2.ExportMetricsServiceRequest()
                request_proto.ParseFromString(body)
                data = MessageToDict(request_proto, preserving_proto_field_name=True)
            except Exception as e:
                print(f"Erro ao parsear Protobuf: {e}")
                # Fallback para JSON
                try:
                    data = json.loads(body.decode('utf-8'))
                except:
                    raise e
        else:
            # JSON direto
            try:
                data = json.loads(body)
            except:
                data = json.loads(body.decode('utf-8'))
        
        # Parser simplificado de OTLP JSON (funciona para ambos agora)
        for resource_metric in data.get('resource_metrics', data.get('resourceMetrics', [])):
            # Extrair atributos do recurso (ex: service.name)
            resource_attrs = {}
            # Protobuf converte para 'attributes', JSON as vezes usa 'attributes'
            res = resource_metric.get('resource', {})
            attrs = res.get('attributes', [])
            
            for attr in attrs:
                key = attr.get('key')
                val = attr.get('value', {})
                # Tenta pegar stringValue, intValue, boolValue, etc.
                # MessageToDict usa snake_case (string_value), JSON usa camelCase (stringValue)
                resource_attrs[key] = val.get('string_value') or val.get('stringValue') or \
                                      str(val.get('int_value')) or str(val.get('intValue')) or \
                                      str(val.get('bool_value')) or str(val.get('boolValue')) or ''
            
            service_name = resource_attrs.get('service.name', 'unknown')

            for scope_metric in resource_metric.get('scope_metrics', resource_metric.get('scopeMetrics', [])):
                for metric in scope_metric.get('metrics', []):
                    metric_name = metric.get('name')
                    unit = metric.get('unit', '')
                    
                    # Lidar com diferentes tipos de dados (Gauge, Sum, etc)
                    data_points = []
                    if 'gauge' in metric:
                        data_points = metric['gauge'].get('data_points', metric['gauge'].get('dataPoints', []))
                    elif 'sum' in metric:
                        data_points = metric['sum'].get('data_points', metric['sum'].get('dataPoints', []))
                    elif 'histogram' in metric:
                        data_points = metric['histogram'].get('data_points', metric['histogram'].get('dataPoints', []))
                    
                    for dp in data_points:
                        # Timestamp OTLP é em nanosegundos
                        # MessageToDict pode converter int64 para string, então garantimos int
                        ts_val = dp.get('time_unix_nano') or dp.get('timeUnixNano')
                        ts_nano = int(ts_val) if ts_val else int(time.time() * 1e9)
                        timestamp = datetime.fromtimestamp(ts_nano / 1e9)
                        
                        # Valor pode ser asDouble ou asInt
                        val_double = dp.get('as_double') or dp.get('asDouble')
                        val_int = dp.get('as_int') or dp.get('asInt')
                        value = val_double if val_double is not None else (val_int if val_int is not None else 0)
                        
                        # Atributos específicos do datapoint
                        dp_attrs = {}
                        for attr in dp.get('attributes', []):
                            key = attr.get('key')
                            val = attr.get('value', {})
                            dp_attrs[key] = val.get('string_value') or val.get('stringValue') or \
                                            str(val.get('int_value')) or str(val.get('intValue')) or \
                                            str(val.get('bool_value')) or str(val.get('boolValue')) or ''
                        
                        # Mesclar atributos
                        full_attributes = {**resource_attrs, **dp_attrs}
                        
                        save_metric(timestamp, service_name, metric_name, value, unit, full_attributes)

        return {"status": "success"}
    except Exception as e:
        print(f"Erro ao processar métrica: {e}")
        # Não retorna 500 para não spamar o log do Java, apenas loga o erro
        return {"status": "error", "message": str(e)}

@app.post("/v1/traces")
async def receive_traces(request: Request):
    try:
        body = await request.body()
        if 'gzip' in request.headers.get('content-encoding', ''):
            body = gzip.decompress(body)
        
        content_type = request.headers.get('content-type', '')
        data = {}

        if 'application/x-protobuf' in content_type or not body.startswith(b'{'):
            try:
                request_proto = trace_service_pb2.ExportTraceServiceRequest()
                request_proto.ParseFromString(body)
                data = MessageToDict(request_proto, preserving_proto_field_name=True)
            except:
                data = json.loads(body.decode('utf-8'))
        else:
            try:
                data = json.loads(body)
            except:
                data = json.loads(body.decode('utf-8'))

        for resource_span in data.get('resource_spans', []):
            resource_attrs = {}
            res = resource_span.get('resource', {})
            for attr in res.get('attributes', []):
                key = attr.get('key')
                val = attr.get('value', {})
                resource_attrs[key] = val.get('string_value') or val.get('stringValue') or str(val)
            
            service_name = resource_attrs.get('service.name', 'unknown')

            for scope_span in resource_span.get('scope_spans', []):
                for span in scope_span.get('spans', []):
                    trace_id = span.get('trace_id')
                    span_id = span.get('span_id')
                    parent_span_id = span.get('parent_span_id', '')
                    name = span.get('name')
                    
                    start_time = int(span.get('start_time_unix_nano', 0))
                    end_time = int(span.get('end_time_unix_nano', 0))
                    duration_ms = (end_time - start_time) / 1e6
                    timestamp = datetime.fromtimestamp(start_time / 1e9)
                    
                    status = span.get('status', {})
                    status_code = status.get('code', 'UNSET')
                    
                    span_attrs = {}
                    for attr in span.get('attributes', []):
                        key = attr.get('key')
                        val = attr.get('value', {})
                        span_attrs[key] = val.get('string_value') or val.get('stringValue') or str(val)
                    
                    full_attributes = {**resource_attrs, **span_attrs}
                    
                    save_trace(timestamp, trace_id, span_id, parent_span_id, service_name, name, duration_ms, status_code, full_attributes)

        return {"status": "success"}
    except Exception as e:
        print(f"Erro ao processar trace: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/v1/logs")
async def receive_logs(request: Request):
    try:
        body = await request.body()
        if 'gzip' in request.headers.get('content-encoding', ''):
            body = gzip.decompress(body)
        
        content_type = request.headers.get('content-type', '')
        data = {}

        if 'application/x-protobuf' in content_type or not body.startswith(b'{'):
            try:
                request_proto = logs_service_pb2.ExportLogsServiceRequest()
                request_proto.ParseFromString(body)
                data = MessageToDict(request_proto, preserving_proto_field_name=True)
            except:
                data = json.loads(body.decode('utf-8'))
        else:
            try:
                data = json.loads(body)
            except:
                data = json.loads(body.decode('utf-8'))

        for resource_log in data.get('resource_logs', []):
            resource_attrs = {}
            res = resource_log.get('resource', {})
            for attr in res.get('attributes', []):
                key = attr.get('key')
                val = attr.get('value', {})
                resource_attrs[key] = val.get('string_value') or val.get('stringValue') or str(val)
            
            service_name = resource_attrs.get('service.name', 'unknown')

            for scope_log in resource_log.get('scope_logs', []):
                for log_record in scope_log.get('log_records', []):
                    time_nano = int(log_record.get('time_unix_nano', 0))
                    timestamp = datetime.fromtimestamp(time_nano / 1e9)
                    
                    severity_text = log_record.get('severity_text', 'INFO')
                    
                    body_val = log_record.get('body', {})
                    log_body = body_val.get('string_value') or body_val.get('stringValue') or str(body_val)
                    
                    log_attrs = {}
                    for attr in log_record.get('attributes', []):
                        key = attr.get('key')
                        val = attr.get('value', {})
                        log_attrs[key] = val.get('string_value') or val.get('stringValue') or str(val)
                    
                    full_attributes = {**resource_attrs, **log_attrs}
                    
                    save_log(timestamp, service_name, severity_text, log_body, full_attributes)

        return {"status": "success"}
    except Exception as e:
        print(f"Erro ao processar log: {e}")
        return {"status": "error", "message": str(e)}

# --- API para o Dashboard (com filtro de Role) ---

@app.get("/api/metrics")
def get_metrics(role: str):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    
    # Query base
    query = "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 500"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    data = [dict(row) for row in rows]
    
    # Filtragem de Segurança (RBAC) no lado da API Python
    filtered_data = []
    
    for row in data:
        attributes = json.loads(row['attributes'])
        metric_name = row['metric_name']
        
        # Lógica de Zero Trust / RBAC
        if role == "ROLE_ADMIN":
            filtered_data.append(row) # Admin vê tudo
            
        elif role == "ROLE_IOT":
            # IoT vê apenas coisas marcadas como IOT ou métricas de sensores
            if "IOT" in str(attributes) or "temperature" in metric_name or "humidity" in metric_name:
                filtered_data.append(row)
                
        elif role == "ROLE_IA":
            # IA vê apenas coisas marcadas como IA ou métricas de modelo
            if "IA" in str(attributes) or "model" in metric_name or "accuracy" in metric_name:
                filtered_data.append(row)
    
    return filtered_data

@app.get("/api/traces")
def get_traces(role: str):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM traces ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    
    data = [dict(row) for row in rows]
    filtered_data = []
    
    for row in data:
        attributes = json.loads(row['attributes'])
        # RBAC Logic
        if role == "ROLE_ADMIN":
            filtered_data.append(row)
        elif role == "ROLE_IOT":
            if "IOT" in str(attributes):
                filtered_data.append(row)
        elif role == "ROLE_IA":
            if "IA" in str(attributes):
                filtered_data.append(row)
                
    return filtered_data

@app.get("/api/logs")
def get_logs(role: str):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    
    data = [dict(row) for row in rows]
    filtered_data = []
    
    for row in data:
        attributes = json.loads(row['attributes'])
        # RBAC Logic
        if role == "ROLE_ADMIN":
            filtered_data.append(row)
        elif role == "ROLE_IOT":
            if "IOT" in str(attributes):
                filtered_data.append(row)
        elif role == "ROLE_IA":
            if "IA" in str(attributes):
                filtered_data.append(row)
                
    return filtered_data

if __name__ == '__main__':
    print("🚀 Humainze Collector & API rodando na porta 4318...")
    uvicorn.run(app, host='0.0.0.0', port=4318)
