# 🤖 Guia de Integração - Time de IA

## 📍 Visão Geral

Este guia descreve como o serviço de IA (Python com FastAPI/Flask) integra-se com o backend Java Humainze para:

1. **Autenticar** via API Key ou JWT
2. **Enviar métricas** de modelos (acurácia, drift, latência, etc.)
3. **Enviar alertas** cognitivos gerados por GPT-4
4. **Visualizar tudo** no SigNoz em tempo real

---

## 🔐 Autenticação

### Opção 1: API Key (Recomendado para Scripts)

```python
import requests

API_KEY = "chave-ia"
BASE_URL = "http://localhost:8080"

# Usa API Key direto no header
headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(
    f"{BASE_URL}/otel/v1/metrics",
    headers=headers
)
```

### Opção 2: JWT (Recomendado para Long-Running Services)

```python
import requests
from datetime import datetime

API_KEY = "chave-ia"
BASE_URL = "http://localhost:8080"

# 1. Obter JWT
auth_response = requests.post(
    f"{BASE_URL}/auth/token",
    headers={"X-API-KEY": API_KEY}
)

token = auth_response.json()["token"]

# 2. Usar JWT em requisições
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Agora usa o token nas requisições
response = requests.get(
    f"{BASE_URL}/otel/v1/metrics",
    headers=headers
)
```

### Configurar no `.env` da IA

```env
HUMAINZE_API_KEY=chave-ia
HUMAINZE_BASE_URL=http://localhost:8080
HUMAINZE_TEAM_TAG=IA
```

---

## 📊 Enviar Métricas de Modelo

### Endpoint

```
POST /otel/v1/metrics
```

### Payload Padrão

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T14:30:00Z",
  "payloadJson": "{\"metric\":\"model_accuracy\",\"value\":0.95,\"model\":\"v2.1\",\"dataset\":\"test\"}"
}
```

### Exemplo Prático - Após Treino do Modelo

```python
import requests
import json
from datetime import datetime, timezone

class HumainzeClient:
    def __init__(self, api_key, base_url="http://localhost:8080"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    def send_metric(self, metric_name, value, extra_data=None):
        """Envia uma métrica para o Humainze"""
        payload_data = {
            "metric": metric_name,
            "value": value
        }
        
        if extra_data:
            payload_data.update(extra_data)
        
        body = {
            "teamTag": "IA",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payloadJson": json.dumps(payload_data)
        }
        
        response = requests.post(
            f"{self.base_url}/otel/v1/metrics",
            json=body,
            headers=self.headers
        )
        
        return response.status_code in [200, 201]

# Uso
client = HumainzeClient("chave-ia")

# Após treino
client.send_metric(
    "model_accuracy",
    value=0.95,
    extra_data={
        "model": "v2.1",
        "dataset": "test_set",
        "epoch": 50
    }
)

# Métrica de latência de inferência
client.send_metric(
    "inference_time_ms",
    value=125,
    extra_data={
        "model": "v2.1",
        "endpoint": "/predict"
    }
)

# Detecção de drift
client.send_metric(
    "model_drift_score",
    value=0.23,
    extra_data={
        "model": "v2.1",
        "method": "kullback_leibler",
        "threshold": 0.3
    }
)
```

---

## 🚨 Enviar Alertas (com GPT-4)

### Endpoint

```
POST /alerts
```

### Payload

```json
{
  "teamTag": "IA",
  "type": "DRIFT|MODEL_ERROR|SERVICE_DOWN|CUSTOM",
  "message": "Descrição gerada por GPT-4"
}
```

### Exemplo Prático - Alerta com GPT-4

```python
import requests
import json
import openai
from datetime import datetime, timezone

class HumainzeAlertClient:
    def __init__(self, api_key, base_url="http://localhost:8080", openai_key=None):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        if openai_key:
            openai.api_key = openai_key
    
    def generate_alert_message(self, alert_type, metric_data):
        """Usa GPT-4 para gerar mensagem de alerta cognitiva"""
        prompt = f"""
        Você é um especialista em ML Ops. Gere um alerta técnico conciso (máx 200 caracteres) para:
        
        Tipo: {alert_type}
        Dados: {json.dumps(metric_data, indent=2)}
        
        Seja direto, específico e acionável.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def send_alert(self, alert_type, metric_data):
        """Envia um alerta inteligente"""
        # Gerar mensagem com GPT-4
        message = self.generate_alert_message(alert_type, metric_data)
        
        body = {
            "teamTag": "IA",
            "type": alert_type,
            "message": message
        }
        
        response = requests.post(
            f"{self.base_url}/alerts",
            json=body,
            headers=self.headers
        )
        
        return response.status_code in [200, 201]

# Uso
alert_client = HumainzeAlertClient(
    "chave-ia",
    openai_key="sk-..."
)

# Detectou drift
alert_client.send_alert("DRIFT", {
    "model": "v2.1",
    "drift_score": 0.45,
    "threshold": 0.3,
    "feature": "user_age_distribution"
})

# Erro em predição
alert_client.send_alert("MODEL_ERROR", {
    "model": "v2.1",
    "error": "NaN detected in predictions",
    "count": 42,
    "percentage": 3.2
})

# Serviço offline
alert_client.send_alert("SERVICE_DOWN", {
    "service": "inference_api",
    "last_heartbeat": "2025-11-20T14:20:00Z",
    "status_code": 503
})
```

---

## 📥 Receber Métricas do Backend

### Endpoint

```
GET /export/metrics?page=0&size=100&sort=timestamp,desc
```

### Exemplo - Monitoramento Contínuo

```python
import requests
from datetime import datetime, timedelta

class HumainzeMetricsClient:
    def __init__(self, api_key, base_url="http://localhost:8080"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    def get_latest_metrics(self, limit=20):
        """Busca as últimas métricas"""
        response = requests.get(
            f"{self.base_url}/export/metrics",
            params={"page": 0, "size": limit, "sort": "timestamp,desc"},
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_metrics_by_team(self, team_tag, hours=24):
        """Busca métricas de um time nos últimos N horas"""
        response = requests.get(
            f"{self.base_url}/export/metrics",
            params={
                "teamTag": team_tag,
                "page": 0,
                "size": 500,
                "sort": "timestamp,desc"
            },
            headers=self.headers
        )
        
        return response.json()

# Uso
metrics_client = HumainzeMetricsClient("chave-ia")

# Buscar últimas métricas
latest = metrics_client.get_latest_metrics(limit=50)

for metric in latest["content"]:
    print(f"{metric['teamTag']} - {metric['timestamp']}")
    print(f"  Payload: {metric['payloadJson']}")
```

---

## 🔍 Visualizar no SigNoz

### Configuração de OTEL no Backend

O backend Java já está configurado para exportar métricas para o SigNoz via OTEL/HTTP.

**Variáveis de Ambiente** (arquivo `.env` ou `application-prod.yml`):

```yaml
otel:
  exporter:
    otlp:
      endpoint: http://signoz-otel:4318
      protocol: http
  metrics:
    export:
      interval: 60000  # 60 segundos
```

### URL do SigNoz

```
http://localhost:3301/dashboard
```

### Dashboard Recomendado

1. **Acesse**: http://localhost:3301/dashboard
2. **Nova Query** → Metrics
3. **Métrica**: `model_accuracy`, `inference_time_ms`, `model_drift_score`
4. **Filtro**: `team="IA"`
5. **Agregação**: Last value, Average, Max

### Exemplo de Query OTEL

```
SELECT
  attributes['model'] as model,
  value as accuracy,
  timestamp
FROM metrics
WHERE
  metric_name = 'model_accuracy'
  AND attributes['team'] = 'IA'
ORDER BY timestamp DESC
LIMIT 100
```

---

## 🧪 Teste Rápido

### cURL - Enviar Métrica

```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IA",
    "timestamp": "2025-11-20T14:30:00Z",
    "payloadJson": "{\"metric\":\"model_accuracy\",\"value\":0.95,\"model\":\"v2.1\"}"
  }'
```

### cURL - Enviar Alerta

```bash
curl -X POST http://localhost:8080/alerts \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IA",
    "type": "DRIFT",
    "message": "Drift detectado no modelo v2.1 - acurácia caiu para 0.75"
  }'
```

### cURL - Listar Métricas

```bash
curl http://localhost:8080/export/metrics?page=0&size=10 \
  -H "X-API-KEY: chave-ia"
```

---

## 📋 Checklist de Integração

- [ ] Credenciais configuradas no `.env`
- [ ] Cliente Python criado (ver exemplo acima)
- [ ] Primeiro envio de métrica testado
- [ ] GPT-4 integrado para alertas
- [ ] SigNoz acessível em http://localhost:3301
- [ ] Dashboard criado no SigNoz
- [ ] Alertas sendo enviados corretamente
- [ ] Equipe notificada dos novos endpoints

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| `401 Unauthorized` | Verifique `X-API-KEY: chave-ia` |
| `403 Forbidden` | Team tag não corresponde à role |
| `500 Internal Server Error` | Verifique formato do `payloadJson` |
| Métricas não aparecem no SigNoz | Verifique endpoint OTEL em `application.yml` |
| GPT-4 não responde | Verifique `OPENAI_API_KEY` |

---

## 📞 Suporte

Contate: backend-team@humainze.ai

Repositório: https://github.com/humanize/humainze-dash

