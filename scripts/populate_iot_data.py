#!/usr/bin/env python3
"""
Script para popular o backend com dados IoT simulados
Envia 250 métricas de sensores ESP32 via OpenTelemetry
"""

import requests
import random
import time
import json
from datetime import datetime, timedelta

# Configuração
BACKEND_URL = "http://172.161.94.218:8081"
API_KEY = "chave-iot"
TOTAL_METRICS = 20

# Autenticar
print("[AUTH] Autenticando no backend...")
auth_response = requests.post(
    f"{BACKEND_URL}/auth/token",
    headers={"X-API-KEY": API_KEY}
)

if auth_response.status_code != 200:
    print(f"[ERRO] Erro na autenticacao: {auth_response.status_code}")
    print(auth_response.text)
    exit(1)

TOKEN = auth_response.json()["token"]
print(f"[OK] Token obtido: {TOKEN[:20]}...")

# Headers para requisições
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Simular dados de sensores
SENSORS = ["DHT22", "MQ135", "LDR"]
LOCATIONS = ["Sala A", "Sala B", "Sala C", "Lab 1", "Lab 2"]

def generate_metric_payload():
    """Gera payload OpenTelemetry com métricas aleatórias"""
    now = datetime.utcnow()
    timestamp_ns = int(now.timestamp() * 1_000_000_000)
    
    # Valores realistas
    temperature = round(random.uniform(18.0, 28.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    co2 = random.randint(400, 1200)
    luminosity = random.randint(100, 800)
    
    return {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "esp32-sensors"}},
                        {"key": "device.id", "value": {"stringValue": f"ESP32-{random.randint(1000, 9999)}"}},
                        {"key": "location", "value": {"stringValue": random.choice(LOCATIONS)}},
                        {"key": "sensor.type", "value": {"stringValue": random.choice(SENSORS)}}
                    ]
                },
                "scopeMetrics": [
                    {
                        "scope": {
                            "name": "humainze-iot",
                            "version": "1.0.0"
                        },
                        "metrics": [
                            {
                                "name": "environment.temperature",
                                "unit": "celsius",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": temperature,
                                            "attributes": [
                                                {"key": "sensor", "value": {"stringValue": "DHT22"}}
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "environment.humidity",
                                "unit": "percent",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": humidity,
                                            "attributes": [
                                                {"key": "sensor", "value": {"stringValue": "DHT22"}}
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "environment.co2",
                                "unit": "ppm",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": float(co2),
                                            "attributes": [
                                                {"key": "sensor", "value": {"stringValue": "MQ135"}}
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "environment.luminosity",
                                "unit": "lux",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": float(luminosity),
                                            "attributes": [
                                                {"key": "sensor", "value": {"stringValue": "LDR"}}
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

# Enviar métricas
print(f"\n[IoT] Enviando {TOTAL_METRICS} metricas IoT...")
success_count = 0
error_count = 0

for i in range(1, TOTAL_METRICS + 1):
    otel_payload = generate_metric_payload()
    
    # Wrap no formato esperado pelo backend
    payload = {
        "teamTag": "IOT",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payloadJson": json.dumps(otel_payload)
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/otel/v1/metrics",
            headers=headers,
            json=payload,
            timeout=5
        )
        
        if response.status_code in [200, 201, 202]:
            success_count += 1
            if i % 50 == 0:
                print(f"[OK] {i}/{TOTAL_METRICS} enviadas")
        else:
            error_count += 1
            if error_count <= 5:
                print(f"[ERRO] Erro na metrica {i}: {response.status_code}")
                print(f"[DEBUG] Response: {response.text[:200]}")
        
        # Pequeno delay para não sobrecarregar
        time.sleep(0.1)
        
    except Exception as e:
        error_count += 1
        if error_count <= 5:
            print(f"[ERRO] Excecao na metrica {i}: {str(e)}")

print(f"\n[RESULTADO]")
print(f"[OK] Sucesso: {success_count}/{TOTAL_METRICS}")
print(f"[ERRO] Erros: {error_count}/{TOTAL_METRICS}")
print(f"[INFO] Taxa de sucesso: {(success_count/TOTAL_METRICS)*100:.1f}%")
