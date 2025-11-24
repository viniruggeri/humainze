# 🤖 Guia de Integração - Time de IA

## 📏 Visão Geral

Este guia descreve como o serviço de IA (Python com FastAPI/Flask) integra-se com o **backend Java Humainze** para:

1. **Autenticar** via JWT (login simples)
2. **Enviar métricas** de modelos ML (acurácia, drift, latência, loss)
3. **Criar alertas cognitivos** (drift detectado, erro de modelo)
4. **Visualizar tudo** no **Dashboard Streamlit** (porta 8501)
5. **Consultar histórico** via APIs REST com paginação

### Por que Backend Java como Observabilidade?

✅ **Solução 100% open-source** - sem dependências externas  
✅ **Persistência em SQL** - métricas armazenadas em OracleDB/H2  
✅ **APIs REST padronizadas** - `/export/metrics`, `/alerts`  
✅ **Dashboard customizável** - Python + Streamlit, fácil de modificar  
✅ **Sistema de alertas integrado** - DRIFT, MODEL_ERROR, SERVICE_DOWN  
✅ **Simples e eficaz** - sem complexidade de setup

---

## 🔐 Autenticação

### Login e Obtenção de Token JWT

O time IA tem credenciais pré-cadastradas:
- **Team:** `IA`
- **Secret:** `ia-secret`

**Passo 1: Login**

```python
import requests

BASE_URL = "http://localhost:8080"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "team": "IA",
        "secret": "ia-secret"
    }
)

token_data = response.json()
TOKEN = token_data["token"]
print(f"Token obtido: {TOKEN[:20]}...")
```

**Resposta:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJJQSIsInJvbGVzIjpbIlJPTEVfSUEiXX0...",
  "team": "IA",
  "roles": ["ROLE_IA"]
}
```

**Passo 2: Usar Token em Todas as Requisições**

```python
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Exemplo: enviar métrica
response = requests.post(
    f"{BASE_URL}/otel/v1/metrics",
    headers=headers,
    json={...}
)
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

## 📊 Visualizar no Dashboard

### Acesso ao Dashboard Streamlit

**URL Local**: `http://localhost:8501`  
**URL Azure**: `http://172.161.94.218:8501`

### Funcionalidades Disponíveis

1. **Tab "🤖 Métricas IA"**:
   - Gráficos interativos de acurácia, loss, drift
   - Time series com Plotly
   - Filtros por período e tipo de métrica
   - Auto-refresh a cada 5 segundos

2. **Tab "🚨 Alertas Ativos"**:
   - Banner com contagem de alertas não resolvidos
   - Histórico completo com paginação
   - Botão para resolver alertas

3. **Filtros Disponíveis**:
   - Team: IA, IOT, ADMIN
   - Período: última hora, 6h, 24h, 7 dias
   - Tipo de métrica
   - Status de alerta

### Exemplo de Uso

```python
# Após enviar métricas, acesse:
# http://localhost:8501

# Selecione tab "Métricas IA"
# Escolha período: "Últimas 24 horas"
# Veja gráfico de model_accuracy em tempo real
```
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
- [ ] Dashboard acessível (porta 8501)
- [ ] Métricas visualizadas no dashboard
- [ ] Alertas sendo enviados corretamente
- [ ] Equipe notificada dos novos endpoints

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| `401 Unauthorized` | Verifique token JWT ou `X-API-KEY: chave-ia` |
| `403 Forbidden` | Team tag não corresponde à role |
| `500 Internal Server Error` | Verifique formato do `payloadJson` |
| Dashboard não carrega | Verifique se backend está rodando (porta 8080) |
| GPT-4 não responde | Verifique `OPENAI_API_KEY` |

---

## 📞 Suporte

Repositório Backend: <https://github.com/viniruggeri/humainze>

Repositório IoT: <https://github.com/viniruggeri/humainze-iot>

