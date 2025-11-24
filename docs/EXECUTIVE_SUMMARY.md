# 📢 Resumo Executivo - Humainze Backend

**Data**: 21/11/2025  
**Versão**: 1.0  
**Status**: ✅ Production Ready

---

## 🎯 Visão Geral

O **Humainze Backend** é uma **solução completa de observabilidade open-source** sem dependências externas.

### Diferenciais

- ✅ **Backend Java como coletor OTLP** - recebe métricas/traces/logs via HTTP
- ✅ **Persistência em banco SQL** - OracleDB (prod) ou H2 (dev)
- ✅ **APIs REST padronizadas** - paginação, filtros, ordenação
- ✅ **Dashboard Streamlit (porta 8501)** - 100% Python, visualização em tempo real
- ✅ **Sistema de alertas integrado** - visualização no dashboard
- ✅ **Totalmente open-source** - sem custos de licenciamento

### Stack Tecnológico

- **Backend:** Java 21, Spring Boot 3.5.7, Spring Security + JWT
- **Persistência:** Spring Data JPA, OracleDB (prod), H2 (dev)
- **Observabilidade:** Backend Java como coletor OTLP via HTTP
- **Dashboard:** Python 3.11, Streamlit (porta 8501), Plotly, Pandas
- **Deploy:** Azure VM (IP: 172.161.94.218)

---

## 🚀 Como Começar?

### Para o Time IA 🤖

**Documentação**: `docs/INTEGRATION_GUIDE_IA.md`

**Quick Start:**
```python
import requests

# 1. Obter token
response = requests.post(
    "http://localhost:8080/auth/token",
    headers={"X-API-KEY": "chave-ia"}
)
token = response.json()["token"]

# 2. Enviar métrica
requests.post(
    "http://localhost:8080/otel/v1/metrics",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "teamTag": "IA",
        "timestamp": "2025-11-20T15:00:00Z",
        "payloadJson": '{"metric":"model_accuracy","value":0.95}'
    }
)

# 3. Enviar alerta inteligente (com GPT-4)
requests.post(
    "http://localhost:8080/alerts",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "teamTag": "IA",
        "type": "DRIFT",
        "message": "Drift detectado - gerado por GPT-4"
    }
)
```

---

### Para o Team IoT 📡

**Documentação**: `docs/INTEGRATION_GUIDE_IOT.md`

**Quick Start (Python/Raspberry Pi):**
```python
import requests
import json
from datetime import datetime, timezone

def send_metric(metric, value, location):
    requests.post(
        "http://localhost:8080/otel/v1/metrics",
        headers={"X-API-KEY": "chave-iot"},
        json={
            "teamTag": "IOT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payloadJson": json.dumps({
                "metric": metric,
                "value": value,
                "location": location
            })
        }
    )

# Enviar temperatura
send_metric("temperature", 25.5, "sala-1")

# Enviar umidade
send_metric("humidity", 65.2, "sala-1")

# Enviar CO2
send_metric("co2_ppm", 850, "sala-2")
```

**Quick Start (Arduino/ESP32 - C++):**
```cpp
void sendMetric(const char* metric, float value) {
  HTTPClient http;
  http.begin("http://192.168.1.100:8080/otel/v1/metrics");
  http.addHeader("X-API-KEY", "chave-iot");
  http.addHeader("Content-Type", "application/json");
  
  String payload = R"({
    "teamTag":"IOT",
    "timestamp":"2025-11-20T14:30:00Z",
    "payloadJson":"{\"metric\":\")" + String(metric) + R"(\",\"value\":)" + 
    String(value) + R"(\"}"
  })";
  
  http.POST(payload);
  http.end();
}

void loop() {
  float temp = readTemperature();
  sendMetric("temperature", temp);
  delay(60000); // A cada 60 segundos
}
```

---

## 📊 Visualizar Dados

**Dashboard Streamlit**: `http://172.161.94.218:8501` (Azure) ou `http://localhost:8501` (local)

**Recursos disponíveis:**
- Gráficos interativos (Plotly)
- Métricas em tempo real (IoT e IA)
- Sistema de alertas
- Filtros por team e período
- Auto-refresh a cada 5 segundos

**Exemplo de Dashboard IA:**
- Widget 1: Acurácia do Modelo (Gauge)
- Widget 2: Detecção de Drift (Time Series)
- Widget 3: Latência de Inferência (Time Series)
- Widget 4: Alertas Recentes (Table)

**Exemplo de Dashboard IoT:**
- Widget 1: Temperatura (Time Series)
- Widget 2: Umidade (Time Series)
- Widget 3: CO2 (Time Series)
- Widget 4: Últimas Leituras (Table)

---

## 🔑 API Keys & Permissões

| Time | API Key | Pode Enviar Para | Role |
|------|---------|------------------|------|
| **IA** | `chave-ia` | `/otel/v1/**`, `/alerts/**` | ROLE_IA |
| **IoT** | `chave-iot` | `/otel/v1/**` | ROLE_IOT |
| **Admin** | `chave-admin` | `/admin/**`, `/alerts/**` | ROLE_ADMIN |

---

## 📈 Exemplos de Métricas

### IA

✅ Model accuracy, loss, precision, recall  
✅ F1 Score, AUC-ROC  
✅ Inference latency  
✅ Model drift detection  
✅ GPU/CPU usage  
✅ Memory consumption  
✅ Training progress  

### IoT

✅ Temperatura (DHT22)  
✅ Umidade (DHT22)  
✅ CO2 (MQ-135)  
✅ Luminosidade (LDR)  
✅ Movimento (PIR)  
✅ Bateria do dispositivo  
✅ Pressão atmosférica  
✅ Altitude, Ruído, Umidade do solo  

---

## 🚨 Alertas Inteligentes

O time IA pode enviar alertas gerados por **GPT-4**:

```python
# Exemplo: Alerta de Drift com GPT-4
alert_message = "Drift detectado no modelo v2.1 - acurácia caiu para 0.75 " + \
                "(limite: 0.80). Feature 'user_age_distribution' mudou 32%. " + \
                "Retrainamento automático será disparado."

requests.post(
    "http://localhost:8080/alerts",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "teamTag": "IA",
        "type": "DRIFT",
        "message": alert_message
    }
)
```

**Tipos de Alerta Suportados:**
- `DRIFT` - Data drift detectado
- `MODEL_ERROR` - Erro em predição
- `SERVICE_DOWN` - Serviço offline
- `CUSTOM` - Alerta customizado

---

## 🧪 Teste Rápido (cURL)

### Autenticação

```bash
curl -X POST http://localhost:8080/auth/token \
  -H "X-API-KEY: chave-ia"
```

**Resposta:**
```json
{"token": "eyJhbGciOiJIUzUxMiJ9..."}
```

### Enviar Métrica IoT

```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-iot" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IOT",
    "timestamp": "2025-11-20T14:30:00Z",
    "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\"}"
  }'
```

### Enviar Alerta IA

```bash
curl -X POST http://localhost:8080/alerts \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IA",
    "type": "DRIFT",
    "message": "Drift detectado no modelo v2.1"
  }'
```

### Listar Métricas

```bash
curl "http://localhost:8080/export/metrics?teamTag=IA&page=0&size=20" \
  -H "X-API-KEY: chave-ia"
```

---

## 📁 Documentação Disponível

| Documento | Para Quem | O Quê |
|-----------|-----------|-------|
| `INTEGRATION_GUIDE_IA.md` | Team IA | Enviar métricas de modelos, alertas com GPT-4, Python examples |
| `INTEGRATION_GUIDE_IOT.md` | Team IoT | Arduino/ESP32/RPi, sensores, auto-inicialização, testes |
| `PAYLOAD_EXAMPLES.md` | Todos | Copy & Paste: 25+ exemplos de payload prontos |
| `DASHBOARD_GUIDE.md` | Todos | Dashboard Streamlit (porta 8501), gráficos interativos |
| `ZERO_TRUST_AUTH.md` | Devs | Arquitetura de autenticação Zero Trust |
| `INDEX.md` | Todos | Índice e mapa de navegação |

**Localização:** `/docs/`

---

## ✅ Testes HTTP Inclusos

**Arquivo:** `http-tests/integration-tests.http`

Contém:
- 15+ testes IoT prontos
- 20+ testes IA prontos
- 7+ testes de alerta
- Tudo com exemplos reais

**Como usar:**
1. Abra em IntelliJ/VS Code
2. Clique no play verde
3. Veja a resposta na barra lateral

---

## 🔍 Próximas Etapas (Recomendado)

**Agora:**
1. Ler documentação do seu time (IA ou IoT)
2. Fazer um teste rápido (cURL)
3. Configurar seu cliente (Python/Arduino/etc)
4. Enviar primeira métrica

**Depois:**
1. Acessar dashboard Streamlit (porta 8501)
2. Visualizar métricas em tempo real
3. Configurar alertas
4. Implementar auto-retrain (IA)
5. Escalar para produção

---

## 🆘 Troubleshooting Comum

| Problema | Solução |
|----------|---------|
| `401 Unauthorized` | Verifique a API Key no header `X-API-KEY` |
| `403 Forbidden` | Verifique se a role do seu time tem permissão |
| `Invalid JSON` | Valide formato do `payloadJson` (deve ser STRING escapado) |
| Dashboard não carrega | Verifique se backend está rodando (porta 8080) |
| Conexão recusada | Verifique IP/porta do backend (default: localhost:8080) |

---

## 📞 Suporte

- **Backend Team**: backend-team@humainze.ai
- **IA Team**: ia-team@humainze.ai
- **IoT Team**: iot-team@humainze.ai
- **DevOps**: devops@humainze.ai

---

## 🎉 Resumo Final

✅ Backend pronto para receber métricas de IA e IoT  
✅ Autenticação Zero Trust implementada  
✅ Dashboard Streamlit na porta 8501  
✅ Alertas inteligentes com GPT-4  
✅ Documentação completa  
✅ Exemplos prontos para usar  
✅ Testes HTTP inclusos  

**Status:** 🟢 **PRONTO PARA PRODUÇÃO**

---

**Documento preparado para**: Humainze Team  
**Data**: 20/11/2025  
**Versão**: 1.0  
**Próxima revisão**: 30/11/2025  

---

🚀 **Bom trabalho! Vamos integrar!** 🚀

