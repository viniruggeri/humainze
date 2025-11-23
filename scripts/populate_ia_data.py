#!/usr/bin/env python3
"""
Script para popular o backend com dados de IA simulados
Envia 250 predições de modelo ML via API REST
"""

import requests
import random
import time
import json
from datetime import datetime, timedelta

# Configuração
BACKEND_URL = "http://172.161.94.218:8081"
API_KEY = "chave-ia"
TOTAL_PREDICTIONS = 10

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

# Tipos de predições
MODELS = ["stress_detector_v2", "productivity_analyzer_v1", "wellness_monitor_v3"]
FEATURE_SETS = [
    "temperature,humidity,co2,luminosity,noise",
    "heart_rate,movement,screen_time,break_frequency",
    "posture,eye_strain,keyboard_activity,mouse_clicks"
]
PREDICTIONS = [
    {"label": "baixo_stress", "confidence": 0.85},
    {"label": "medio_stress", "confidence": 0.72},
    {"label": "alto_stress", "confidence": 0.91},
    {"label": "produtividade_alta", "confidence": 0.88},
    {"label": "produtividade_media", "confidence": 0.75},
    {"label": "fadiga_detectada", "confidence": 0.82},
    {"label": "ambiente_ideal", "confidence": 0.94},
    {"label": "necessita_pausa", "confidence": 0.79}
]

def generate_prediction_payload():
    """Gera payload de predição simulada"""
    prediction = random.choice(PREDICTIONS)
    
    # Adicionar ruído à confiança
    confidence = min(0.99, max(0.60, prediction["confidence"] + random.uniform(-0.10, 0.10)))
    
    # Simular drift ocasional
    drift_score = random.uniform(0.01, 0.25) if random.random() > 0.7 else 0.0
    
    return {
        "model_name": random.choice(MODELS),
        "model_version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 20)}",
        "features": random.choice(FEATURE_SETS),
        "prediction": prediction["label"],
        "confidence": round(confidence, 4),
        "drift_score": round(drift_score, 4),
        "inference_time_ms": random.randint(15, 150),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata": {
            "user_id": f"USER{random.randint(1000, 9999)}",
            "session_id": f"SESSION-{random.randint(10000, 99999)}",
            "device_type": random.choice(["desktop", "mobile", "tablet"]),
            "location": random.choice(["Sala A", "Sala B", "Lab 1", "Lab 2", "Home Office"])
        }
    }

# Endpoint para enviar predições (assumindo que existe ou criando via metrics)
def send_as_metric(prediction_data):
    """Envia predição como métrica OpenTelemetry"""
    now = datetime.utcnow()
    timestamp_ns = int(now.timestamp() * 1_000_000_000)
    
    return {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "ml-inference"}},
                        {"key": "model.name", "value": {"stringValue": prediction_data["model_name"]}},
                        {"key": "model.version", "value": {"stringValue": prediction_data["model_version"]}}
                    ]
                },
                "scopeMetrics": [
                    {
                        "scope": {
                            "name": "humainze-ia",
                            "version": "1.0.0"
                        },
                        "metrics": [
                            {
                                "name": "ml.prediction.confidence",
                                "unit": "ratio",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": prediction_data["confidence"],
                                            "attributes": [
                                                {"key": "prediction", "value": {"stringValue": prediction_data["prediction"]}},
                                                {"key": "model", "value": {"stringValue": prediction_data["model_name"]}}
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "ml.model.drift",
                                "unit": "ratio",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": prediction_data["drift_score"],
                                            "attributes": [
                                                {"key": "model", "value": {"stringValue": prediction_data["model_name"]}}
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "ml.inference.duration",
                                "unit": "ms",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(timestamp_ns),
                                            "asDouble": float(prediction_data["inference_time_ms"]),
                                            "attributes": [
                                                {"key": "model", "value": {"stringValue": prediction_data["model_name"]}}
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

# Enviar predições
print(f"\n[IA] Enviando {TOTAL_PREDICTIONS} predicoes de IA...")
success_count = 0
error_count = 0

for i in range(1, TOTAL_PREDICTIONS + 1):
    prediction_data = generate_prediction_payload()
    otel_payload = send_as_metric(prediction_data)
    
    # Wrap no formato esperado pelo backend
    payload = {
        "teamTag": "IA",
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
                print(f"[OK] {i}/{TOTAL_PREDICTIONS} enviadas")
        else:
            error_count += 1
            if error_count <= 5:
                print(f"[ERRO] Erro na predicao {i}: {response.status_code}")
                print(f"[DEBUG] Response: {response.text[:200]}")
        
        # Pequeno delay para não sobrecarregar
        time.sleep(0.1)
        
    except Exception as e:
        error_count += 1
        if error_count <= 5:
            print(f"[ERRO] Excecao na predicao {i}: {str(e)}")

print(f"\n[RESULTADO]")
print(f"[OK] Sucesso: {success_count}/{TOTAL_PREDICTIONS}")
print(f"[ERRO] Erros: {error_count}/{TOTAL_PREDICTIONS}")
print(f"[INFO] Taxa de sucesso: {(success_count/TOTAL_PREDICTIONS)*100:.1f}%")
