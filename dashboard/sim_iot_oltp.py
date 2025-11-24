#!/usr/bin/env python3
"""
Simulador de Dispositivos IoT - ROLE_IOT
Envia traces, logs e métricas OTLP para o collector (porta 4318)
Simula sensores ESP32 em tempo real
"""

import requests
import time
import random
import json
from datetime import datetime, timezone

JAVA_BASE_URL = "http://localhost:8080"
COLLECTOR_URL = "http://localhost:4318"
API_KEY_IOT = "chave-iot"

class IOTSimulator:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        self.device_id = f"ESP32-{random.randint(1000, 9999)}"
        self.reading_count = 0
        
    def authenticate(self):
        """Autentica como ROLE_IOT"""
        print("\n📡 [IOT] Autenticando dispositivos IoT...")
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": API_KEY_IOT}
            )
            response.raise_for_status()
            self.token = response.json()["token"]
            print(f"✅ [IOT] Token obtido: {self.token[:40]}...")
            return True
        except Exception as e:
            print(f"❌ [IOT] Erro na autenticação: {e}")
            return False
    
    def send_metrics(self):
        """Envia métricas OTLP para o collector"""
        temp = random.uniform(18.0, 28.0)
        humidity = random.uniform(40.0, 70.0)
        co2 = random.uniform(400.0, 1200.0)
        lux = random.uniform(100.0, 800.0)
        
        payload = {
            "resourceMetrics": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-iot"}},
                        {"key": "device.id", "value": {"stringValue": self.device_id}},
                        {"key": "team", "value": {"stringValue": "IOT"}},
                        {"key": "location", "value": {"stringValue": "office_1"}}
                    ]
                },
                "scopeMetrics": [{
                    "scope": {
                        "name": "iot-sensors",
                        "version": "1.0.0"
                    },
                    "metrics": [
                        {
                            "name": "temperature",
                            "description": "Temperatura ambiente em °C",
                            "unit": "celsius",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": temp,
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "sensor.type", "value": {"stringValue": "DHT22"}},
                                        {"key": "sensor.location", "value": {"stringValue": "office_1"}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "humidity",
                            "description": "Umidade relativa do ar em %",
                            "unit": "percent",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": humidity,
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "sensor.type", "value": {"stringValue": "DHT22"}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "air_quality_ppm",
                            "description": "Qualidade do ar (CO2) em PPM",
                            "unit": "ppm",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": co2,
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "sensor.type", "value": {"stringValue": "MQ135"}}
                                    ]
                                }]
                            }
                        },
                        {
                            "name": "luminosity_lux",
                            "description": "Luminosidade em Lux",
                            "unit": "lux",
                            "gauge": {
                                "dataPoints": [{
                                    "asDouble": lux,
                                    "timeUnixNano": int(time.time() * 1e9),
                                    "attributes": [
                                        {"key": "sensor.type", "value": {"stringValue": "BH1750"}}
                                    ]
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
                print(f"✅ [METRICS] Temp:{temp:.1f}°C Hum:{humidity:.0f}% CO2:{co2:.0f}ppm Lux:{lux:.0f}")
            else:
                print(f"❌ [METRICS] Erro {response.status_code}")
        except Exception as e:
            print(f"❌ [METRICS] Exceção: {e}")
    
    def send_traces(self):
        """Envia traces OTLP para o collector"""
        trace_id = f"{random.getrandbits(128):032x}"
        span_id = f"{random.getrandbits(64):016x}"
        child_span_id = f"{random.getrandbits(64):016x}"
        
        reading_duration = random.uniform(0.3, 1.0)
        start_time = time.time() - reading_duration
        
        payload = {
            "resourceSpans": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-iot"}},
                        {"key": "device.id", "value": {"stringValue": self.device_id}},
                        {"key": "team", "value": {"stringValue": "IOT"}}
                    ]
                },
                "scopeSpans": [{
                    "scope": {
                        "name": "iot-operations",
                        "version": "1.0.0"
                    },
                    "spans": [
                        {
                            "traceId": trace_id,
                            "spanId": span_id,
                            "name": "sensor_reading_cycle",
                            "kind": 1,
                            "startTimeUnixNano": int(start_time * 1e9),
                            "endTimeUnixNano": int(time.time() * 1e9),
                            "attributes": [
                                {"key": "sensor.count", "value": {"intValue": 4}},
                                {"key": "reading.status", "value": {"stringValue": "success"}},
                                {"key": "device.location", "value": {"stringValue": "office_1"}},
                                {"key": "reading.number", "value": {"intValue": self.reading_count}}
                            ],
                            "events": [
                                {
                                    "timeUnixNano": int((start_time + 0.1) * 1e9),
                                    "name": "sensors_initialized",
                                    "attributes": [
                                        {"key": "sensor.types", "value": {"stringValue": "DHT22,MQ135,BH1750"}}
                                    ]
                                },
                                {
                                    "timeUnixNano": int((start_time + 0.5) * 1e9),
                                    "name": "data_collected",
                                    "attributes": [
                                        {"key": "readings.count", "value": {"intValue": 4}}
                                    ]
                                },
                                {
                                    "timeUnixNano": int((time.time() - 0.05) * 1e9),
                                    "name": "data_transmitted",
                                    "attributes": [
                                        {"key": "protocol", "value": {"stringValue": "HTTP"}},
                                        {"key": "endpoint", "value": {"stringValue": "/v1/metrics"}}
                                    ]
                                }
                            ],
                            "status": {"code": 1}
                        },
                        {
                            "traceId": trace_id,
                            "spanId": child_span_id,
                            "parentSpanId": span_id,
                            "name": "dht22_read",
                            "kind": 3,
                            "startTimeUnixNano": int((start_time + 0.1) * 1e9),
                            "endTimeUnixNano": int((start_time + 0.4) * 1e9),
                            "attributes": [
                                {"key": "sensor.type", "value": {"stringValue": "DHT22"}},
                                {"key": "sensor.pin", "value": {"intValue": 4}}
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
                print(f"✅ [TRACES] sensor_reading_cycle → 4 sensors ({reading_duration*1000:.0f}ms)")
            else:
                print(f"❌ [TRACES] Erro {response.status_code}")
        except Exception as e:
            print(f"❌ [TRACES] Exceção: {e}")
    
    def send_logs(self, level="INFO"):
        """Envia logs OTLP para o collector"""
        log_messages = {
            "INFO": [
                f"Leitura de sensores concluída: 4 sensores OK",
                f"Conectado ao WiFi: FIAP-IoT (RSSI: -{random.randint(40, 70)} dBm)",
                f"Dados enviados para backend: 200 OK",
                f"Uptime: {random.randint(1, 720)}h (memória livre: {random.randint(50, 80)}%)",
                f"Bateria: {random.randint(60, 100)}% (modo sleep ativo)"
            ],
            "WARN": [
                f"Temperatura acima do normal: {random.uniform(28, 32):.1f}°C",
                f"Umidade baixa detectada: {random.uniform(20, 35):.1f}%",
                f"Qualidade do ar degradada: {random.uniform(1200, 1800):.0f} PPM",
                f"WiFi instável: {random.randint(2, 5)} reconexões na última hora",
                f"Bateria baixa: {random.randint(10, 25)}% (carregar em breve)"
            ],
            "ERROR": [
                f"Falha na leitura do sensor DHT22 (timeout após {random.randint(2, 5)}s)",
                f"Erro ao conectar WiFi (tentativa {random.randint(1, 3)}/3)",
                f"Erro HTTP ao enviar dados: 503 Service Unavailable",
                f"Memória crítica: {random.randint(90, 98)}% (resetando...)",
                f"Sensor MQ135 não responde (verificar conexão)"
            ]
        }
        
        severity_map = {"INFO": 9, "WARN": 13, "ERROR": 17}
        
        payload = {
            "resourceLogs": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "humainze-iot"}},
                        {"key": "device.id", "value": {"stringValue": self.device_id}},
                        {"key": "team", "value": {"stringValue": "IOT"}}
                    ]
                },
                "scopeLogs": [{
                    "scope": {
                        "name": "iot-logger",
                        "version": "1.0.0"
                    },
                    "logRecords": [{
                        "timeUnixNano": int(time.time() * 1e9),
                        "severityNumber": severity_map[level],
                        "severityText": level,
                        "body": {"stringValue": random.choice(log_messages[level])},
                        "attributes": [
                            {"key": "device.id", "value": {"stringValue": self.device_id}},
                            {"key": "log.source", "value": {"stringValue": "esp32_main"}},
                            {"key": "firmware.version", "value": {"stringValue": "1.0.0"}},
                            {"key": "reading.number", "value": {"intValue": self.reading_count}}
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
        """Executa simulação completa de dispositivo IoT"""
        print(f"\n🚀 Iniciando simulador IoT - Device: {self.device_id}")
        print(f"📡 Collector: {COLLECTOR_URL}")
        print(f"🔁 Iterações: {iterations}, Intervalo: {interval}s\n")
        
        for i in range(iterations):
            self.reading_count = i + 1
            print(f"\n--- Leitura {i+1}/{iterations} ---")
            
            # Enviar métricas
            self.send_metrics()
            
            # Enviar traces
            self.send_traces()
            
            # Enviar logs (varia severidade)
            if random.random() < 0.75:
                self.send_logs("INFO")
            elif random.random() < 0.92:
                self.send_logs("WARN")
            else:
                self.send_logs("ERROR")
            
            if i < iterations - 1:
                print(f"⏳ Aguardando {interval}s...")
                time.sleep(interval)
        
        print(f"\n✅ Simulação IoT concluída! {iterations} leituras processadas.")


if __name__ == "__main__":
    simulator = IOTSimulator()
    
    # Autenticar (opcional para demo)
    # simulator.authenticate()
    
    # Rodar simulação
    simulator.run_simulation(iterations=30, interval=3)
