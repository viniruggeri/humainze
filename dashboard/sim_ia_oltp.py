#!/usr/bin/env python3
"""
Simulador de Sistema IA - ROLE_IA
Envia traces, logs e métricas OTLP para o collector (porta 4318)
Simula operações reais de IA em tempo real
"""

import requests
import time
import random
import json
from datetime import datetime, timezone

JAVA_BASE_URL = "http://localhost:8080"
COLLECTOR_URL = "http://localhost:4318"
API_KEY_IA = "chave-ia"

class IASimulator:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        self.operation_count = 0
        
    def authenticate(self):
        """Autentica como ROLE_IA"""
        print("\n🤖 [IA] Autenticando sistema IA...")
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": API_KEY_IA}
            )
            response.raise_for_status()
            self.token = response.json()["token"]
            print(f"✅ [IA] Token obtido: {self.token[:40]}...")
            return True
        except Exception as e:
            print(f"❌ [IA] Erro na autenticação: {e}")
            return False
    
    def send_metrics(self):
        """Envia métricas OTLP para o collector"""
        payload = {
            "resourceMetrics": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-ia"}},
                        {"key": "team", "value": {"stringValue": "IA"}},
                        {"key": "instance", "value": {"stringValue": f"ia-worker-{random.randint(1,3)}"}}
                    ]
                },
                "scopeMetrics": [{
                    "scope": {"name": "ia-operations", "version": "1.0.0"},
                    "metrics": [
                        {
                            "name": "mobile_dashboard_views",
                            "description": "Visualizações do dashboard mobile",
                            "unit": "views",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": random.uniform(10, 100),
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "platform", "value": {"stringValue": random.choice(["ios", "android"])}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "prediction_count",
                            "description": "Total de predições realizadas",
                            "unit": "predictions",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": random.uniform(50, 300),
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "model", "value": {"stringValue": "prophet_v2"}},
                                        {"key": "success", "value": {"boolValue": True}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "anomalies_detected",
                            "description": "Anomalias detectadas pelos modelos",
                            "unit": "anomalies",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": random.uniform(0, 15),
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "severity", "value": {"stringValue": random.choice(["low", "medium", "high"])}},
                                        {"key": "detector", "value": {"stringValue": "isolation_forest"}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "model_inference_duration_ms",
                            "description": "Duração da inferência do modelo",
                            "unit": "ms",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": random.uniform(50, 500),
                                    "timeUnixNano": int(time.time() * 1e9)
                                }]
                            }
                        }
                    ]
                }]
            }]
        }
        
        try:
            response = self.session.post(
                f"{COLLECTOR_URL}/v1/metrics",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"✅ [METRICS] IA - {payload['resourceMetrics'][0]['scopeMetrics'][0]['metrics'][0]['gauge']['dataPoints'][0]['asDouble']:.0f} views")
            else:
                print(f"❌ [METRICS] Erro {response.status_code}")
        except Exception as e:
            print(f"❌ [METRICS] Exceção: {e}")
    
    def send_traces(self, operation_type="prediction"):
        """Envia traces OTLP para o collector"""
        trace_id = f"{random.getrandbits(128):032x}"
        parent_span_id = f"{random.getrandbits(64):016x}"
        child_span_id = f"{random.getrandbits(64):016x}"
        
        operations = {
            "prediction": {
                "parent": "mobile_dashboard_request",
                "child": "prophet_model_inference",
                "duration": random.uniform(0.5, 2.0)
            },
            "anomaly_detection": {
                "parent": "anomaly_detection_pipeline",
                "child": "isolation_forest_scoring",
                "duration": random.uniform(0.2, 1.0)
            },
            "cache_check": {
                "parent": "cache_lookup",
                "child": "redis_get",
                "duration": random.uniform(0.01, 0.05)
            }
        }
        
        op = operations[operation_type]
        start_time = time.time() - op["duration"]
        
        payload = {
            "resourceSpans": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-ia"}},
                        {"key": "team", "value": {"stringValue": "IA"}}
                    ]
                },
                "scopeSpans": [{
                    "scope": {"name": "ia-ml-pipeline", "version": "1.0.0"},
                    "spans": [
                        {
                            "traceId": trace_id,
                            "spanId": parent_span_id,
                            "name": op["parent"],
                            "kind": 1,
                            "startTimeUnixNano": int(start_time * 1e9),
                            "endTimeUnixNano": int(time.time() * 1e9),
                            "attributes": [
                                {"key": "http.method", "value": {"stringValue": "POST"}},
                                {"key": "http.route", "value": {"stringValue": "/predict/dashboard"}},
                                {"key": "user.id", "value": {"stringValue": f"user_{random.randint(100,999)}"}}
                            ],
                            "status": {"code": 1}
                        },
                        {
                            "traceId": trace_id,
                            "spanId": child_span_id,
                            "parentSpanId": parent_span_id,
                            "name": op["child"],
                            "kind": 3,
                            "startTimeUnixNano": int((start_time + 0.1) * 1e9),
                            "endTimeUnixNano": int((time.time() - 0.1) * 1e9),
                            "attributes": [
                                {"key": "ml.model.name", "value": {"stringValue": "prophet"}},
                                {"key": "ml.prediction.count", "value": {"intValue": random.randint(50, 200)}}
                            ],
                            "events": [
                                {
                                    "timeUnixNano": int((start_time + 0.2) * 1e9),
                                    "name": "model_loaded",
                                    "attributes": [{"key": "cache", "value": {"stringValue": "hit"}}]
                                },
                                {
                                    "timeUnixNano": int((start_time + 0.5) * 1e9),
                                    "name": "data_preprocessed",
                                    "attributes": [{"key": "rows", "value": {"intValue": random.randint(100, 500)}}]
                                }
                            ],
                            "status": {"code": 1}
                        }
                    ]
                }]
            }]
        }
        
        try:
            response = self.session.post(
                f"{COLLECTOR_URL}/v1/traces",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"✅ [TRACES] {op['parent']} → {op['child']} ({op['duration']*1000:.0f}ms)")
            else:
                print(f"❌ [TRACES] Erro {response.status_code}")
        except Exception as e:
            print(f"❌ [TRACES] Exceção: {e}")
    
    def send_logs(self, level="INFO"):
        """Envia logs OTLP para o collector"""
        log_messages = {
            "INFO": [
                f"Dashboard prediction cache hit - saved {random.uniform(1, 5):.1f}s",
                f"Model inference completed - {random.randint(50, 300)} predictions generated",
                f"Alert sent to backend - anomaly severity: {random.choice(['low', 'medium', 'high'])}",
                f"JWT token refreshed successfully - valid for 24h",
                f"Database query executed - {random.randint(100, 1000)} rows returned"
            ],
            "WARN": [
                f"Prediction cache expired - re-training Prophet model",
                f"Anomaly score threshold exceeded: {random.uniform(0.7, 0.95):.2f}",
                f"Model latency high: {random.uniform(2, 5):.1f}s (threshold: 2s)",
                f"Memory usage elevated: {random.uniform(70, 85):.0f}%",
                f"Database connection pool near capacity: {random.randint(8, 10)}/10"
            ],
            "ERROR": [
                f"Failed to load ML model from registry - fallback to local cache",
                f"Database connection timeout after {random.randint(5, 10)}s",
                f"OTLP export failed - metrics buffer at {random.randint(80, 95)}%",
                f"JWT validation failed - token expired {random.randint(1, 24)}h ago",
                f"Prediction failed for team {random.randint(1, 3)} - insufficient data"
            ]
        }
        
        severity_map = {"INFO": 9, "WARN": 13, "ERROR": 17}
        
        payload = {
            "resourceLogs": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-ia"}},
                        {"key": "team", "value": {"stringValue": "IA"}}
                    ]
                },
                "scopeLogs": [{
                    "scope": {"name": "ia-logger", "version": "1.0.0"},
                    "logRecords": [{
                        "timeUnixNano": int(time.time() * 1e9),
                        "severityNumber": severity_map[level],
                        "severityText": level,
                        "body": {"stringValue": random.choice(log_messages[level])},
                        "attributes": [
                            {"key": "module", "value": {"stringValue": random.choice(["ml.inference", "api.mobile", "cache.manager", "db.connector"])}},
                            {"key": "operation", "value": {"stringValue": f"op_{self.operation_count}"}},
                            {"key": "thread", "value": {"stringValue": f"worker-{random.randint(1, 4)}"}}
                        ]
                    }]
                }]
            }]
        }
        
        try:
            response = self.session.post(
                f"{COLLECTOR_URL}/v1/logs",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                msg = payload['resourceLogs'][0]['scopeLogs'][0]['logRecords'][0]['body']['stringValue']
                print(f"✅ [LOGS] {level} - {msg[:60]}...")
            else:
                print(f"❌ [LOGS] Erro {response.status_code}")
        except Exception as e:
            print(f"❌ [LOGS] Exceção: {e}")
    
    def run_simulation(self, iterations=30, interval=3):
        """Executa simulação completa de operações IA"""
        print(f"\n🚀 Iniciando simulador IA - Service: humainze-ia")
        print(f"📡 Collector: {COLLECTOR_URL}")
        print(f"🔁 Iterações: {iterations}, Intervalo: {interval}s\n")
        
        for i in range(iterations):
            self.operation_count = i + 1
            print(f"\n--- Iteração {i+1}/{iterations} ---")
            
            # Enviar métricas
            self.send_metrics()
            
            # Enviar traces (varia o tipo)
            operation = random.choice(["prediction", "anomaly_detection", "cache_check"])
            self.send_traces(operation)
            
            # Enviar logs (varia severidade)
            if random.random() < 0.7:
                self.send_logs("INFO")
            elif random.random() < 0.9:
                self.send_logs("WARN")
            else:
                self.send_logs("ERROR")
            
            if i < iterations - 1:
                print(f"⏳ Aguardando {interval}s...")
                time.sleep(interval)
        
        print(f"\n✅ Simulação IA concluída! {iterations} operações processadas.")


if __name__ == "__main__":
    simulator = IASimulator()
    
    # Autenticar (opcional para demo)
    # simulator.authenticate()
    
    # Rodar simulação
    simulator.run_simulation(iterations=30, interval=3)
