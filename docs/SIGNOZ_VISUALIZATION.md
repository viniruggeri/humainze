# 🔍 Visualizar Métricas no SigNoz

## 📍 Acesso

```
URL: http://localhost:3301
```

Se rodando em servidor remoto:
```
URL: http://<seu-servidor>:3301
```

---

## 🚀 Configuração do Backend (Java)

### 1. Verificar application-dev.yml

```yaml
otel:
  exporter:
    otlp:
      endpoint: http://localhost:4318  # SigNoz OTEL Receiver
      protocol: http
  metrics:
    export:
      interval: 60000  # Export a cada 60 segundos
```

### 2. Verificar application-prod.yml

```yaml
otel:
  exporter:
    otlp:
      endpoint: http://signoz-otel:4318  # Use docker service name se em Docker
      protocol: http
  metrics:
    export:
      interval: 30000  # Mais frequente em prod
```

### 3. Variáveis de Ambiente (opcional)

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http
export OTEL_METRICS_EXPORTER=otlp
```

---

## 🐳 Docker Compose - Levantar SigNoz

Crie `docker-compose-signoz.yml`:

```yaml
version: '3.8'

services:
  otel-collector:
    image: signoz/otel-collector:latest
    command:
      - "--config=/etc/otel-collector-config.yaml"
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP
    depends_on:
      - postgres
      - signoz

  signoz:
    image: signoz/signoz:latest
    container_name: signoz
    ports:
      - "3301:3301"  # Web UI
    environment:
      - OTEL_RECEIVER_OTLP_DISABLED=false
      - POSTGRES_HOST=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    depends_on:
      - postgres
    volumes:
      - signoz-data:/var/lib/signoz

  postgres:
    image: postgres:15
    container_name: signoz-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: signoz
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  signoz-data:
  postgres-data:
```

**Executar:**
```bash
docker-compose -f docker-compose-signoz.yml up -d
```

**Acessar:**
```
http://localhost:3301
```

---

## 📊 Criar Dashboard para IoT

### Passo 1: Acessar Dashboard

1. Abra http://localhost:3301
2. Clique em **"Dashboards"** → **"+ New Dashboard"**
3. Nome: `IoT Metrics`
4. Clique **"Create"**

### Passo 2: Adicionar Widget de Temperatura

1. Clique **"+ Add Panel"**
2. Selecione **"Time Series"**
3. Em **"Metrics"**, procure por `temperature`
4. Clique em **"Filters"** → Adicione:
   - Campo: `team`
   - Operador: `=`
   - Valor: `IOT`
5. Configure:
   - **Título**: "Temperatura Ambiente"
   - **Y-Axis Label**: "°C"
   - **Refresh**: "5 seconds"
6. Clique **"Save"**

### Passo 3: Adicionar Widget de Umidade

Repita os passos acima para:
- Métrica: `humidity`
- Título: "Umidade do Ar"
- Y-Axis Label: "%"

### Passo 4: Adicionar Widget de CO2

Repita para:
- Métrica: `co2_ppm`
- Título: "Nível de CO2"
- Y-Axis Label: "ppm"
- Adicione threshold visual (ex: 1000 ppm em vermelho)

### Passo 5: Tabela com Últimos Valores

1. Clique **"+ Add Panel"**
2. Selecione **"Table"**
3. Query customizada:

```sql
SELECT
  JSON_EXTRACT(payloadJson, '$.location') as Localização,
  JSON_EXTRACT(payloadJson, '$.metric') as Métrica,
  JSON_EXTRACT(payloadJson, '$.value') as Valor,
  timestamp as Timestamp
FROM metrics
WHERE attributes['team'] = 'IOT'
ORDER BY timestamp DESC
LIMIT 50
```

4. Clique **"Save"**

---

## 📊 Criar Dashboard para IA

### Passo 1: Novo Dashboard

1. Clique **"+ New Dashboard"**
2. Nome: `IA Models`
3. Clique **"Create"**

### Passo 2: Acurácia do Modelo

1. Clique **"+ Add Panel"**
2. Selecione **"Gauge"** (ou "Time Series")
3. Métrica: `model_accuracy`
4. Filtro: `team = IA`
5. Título: "Model Accuracy v2.1"
6. Configure threshold:
   - 🟢 Verde: >= 0.90
   - 🟡 Amarelo: 0.80-0.89
   - 🔴 Vermelho: < 0.80

### Passo 3: Detecção de Drift

1. Clique **"+ Add Panel"**
2. Selecione **"Time Series"**
3. Métrica: `model_drift_score`
4. Filtro: `team = IA`
5. Adicione linha horizontal de threshold (0.3)
6. Título: "Model Drift Score"

### Passo 4: Latência de Inferência

1. Clique **"+ Add Panel"**
2. Selecione **"Time Series"**
3. Métrica: `inference_time_ms`
4. Filtro: `team = IA`
5. Título: "Inference Latency"
6. Y-Axis Label: "ms"

### Passo 5: Múltiplas Métricas de Desempenho

1. Clique **"+ Add Panel"**
2. Selecione **"Time Series"**
3. Adicione múltiplas queries:
   - `model_precision`
   - `model_recall`
   - `model_f1_score`
4. Filtro: `team = IA`
5. Título: "Classification Metrics"
6. Legend: "bottom"

---

## 🔔 Configurar Alertas no SigNoz

### Alerta 1: Drift Detectado

1. Vá para **"Alerts"** → **"+ New Alert"**
2. Nome: `Model Drift Alert`
3. Condição:
   ```
   model_drift_score > 0.3 AND team = "IA"
   ```
4. Duração: "5 minutes" (trigger após 5 min contínuos)
5. Ação: **"Send to Slack/Email"**
6. Mensagem:
   ```
   ⚠️ DRIFT DETECTADO
   Modelo v2.1 apresenta drift > 0.3
   Acurácia pode estar degradada
   ```

### Alerta 2: Acurácia Baixa

1. **"+ New Alert"**
2. Nome: `Low Model Accuracy`
3. Condição:
   ```
   model_accuracy < 0.80 AND team = "IA"
   ```
4. Duração: "3 minutes"
5. Ação: Send notification

### Alerta 3: Latência Alta

1. **"+ New Alert"**
2. Nome: `High Inference Latency`
3. Condição:
   ```
   inference_time_ms > 500 AND team = "IA"
   ```
4. Duração: "2 minutes"

### Alerta 4: Serviço IoT Offline

1. **"+ New Alert"**
2. Nome: `IoT Service Down`
3. Condição:
   ```
   no_data_for(5m) AND team = "IOT"
   ```
4. Ação: Send critical notification

---

## 🔗 Integrações

### Slack

1. Em **"Alerts"** → **"Notification Channels"** → **"+ Add"**
2. Tipo: **"Slack"**
3. Webhook URL: `https://hooks.slack.com/services/...`
4. Clique **"Test"** e **"Save"**

### Email

1. Em **"Alerts"** → **"Notification Channels"** → **"+ Add"**
2. Tipo: **"Email"**
3. Adicione emails dos times
4. Clique **"Save"**

### PagerDuty

1. Em **"Alerts"** → **"Notification Channels"** → **"+ Add"**
2. Tipo: **"PagerDuty"**
3. Cole API Key do PagerDuty
4. Clique **"Save"**

---

## 📈 Queries Recomendadas

### Query 1: Temperatura Média por Localização (IoT)

```sql
SELECT
  JSON_EXTRACT(payloadJson, '$.location') as location,
  AVG(JSON_EXTRACT(payloadJson, '$.value')) as avg_temperature,
  MAX(JSON_EXTRACT(payloadJson, '$.value')) as max_temperature,
  MIN(JSON_EXTRACT(payloadJson, '$.value')) as min_temperature,
  DATE_TRUNC(timestamp, 1h) as hour
FROM metrics
WHERE
  metric_name = 'temperature'
  AND attributes['team'] = 'IOT'
GROUP BY location, hour
ORDER BY hour DESC
```

---

### Query 2: Evolução da Acurácia do Modelo (IA)

```sql
SELECT
  JSON_EXTRACT(payloadJson, '$.model') as model,
  JSON_EXTRACT(payloadJson, '$.value') as accuracy,
  JSON_EXTRACT(payloadJson, '$.epoch') as epoch,
  timestamp
FROM metrics
WHERE
  metric_name = 'model_accuracy'
  AND attributes['team'] = 'IA'
ORDER BY timestamp DESC
LIMIT 500
```

---

### Query 3: Detecção de Anomalias em Drift

```sql
SELECT
  JSON_EXTRACT(payloadJson, '$.model') as model,
  JSON_EXTRACT(payloadJson, '$.value') as drift_score,
  JSON_EXTRACT(payloadJson, '$.threshold') as threshold,
  CASE
    WHEN JSON_EXTRACT(payloadJson, '$.value') > JSON_EXTRACT(payloadJson, '$.threshold')
    THEN 'ANOMALY'
    ELSE 'NORMAL'
  END as status,
  timestamp
FROM metrics
WHERE
  metric_name = 'model_drift_score'
  AND attributes['team'] = 'IA'
ORDER BY timestamp DESC
```

---

### Query 4: Correlação entre Temperatura e Umidade

```sql
SELECT
  ROUND(AVG(CASE WHEN metric_name = 'temperature' THEN JSON_EXTRACT(payloadJson, '$.value') END), 2) as avg_temp,
  ROUND(AVG(CASE WHEN metric_name = 'humidity' THEN JSON_EXTRACT(payloadJson, '$.value') END), 2) as avg_humidity,
  DATE_TRUNC(timestamp, 1h) as hour
FROM metrics
WHERE
  attributes['team'] = 'IOT'
  AND metric_name IN ('temperature', 'humidity')
GROUP BY hour
ORDER BY hour DESC
LIMIT 168  -- Últimas 7 dias
```

---

### Query 5: Taxa de Erro em Predições

```sql
SELECT
  JSON_EXTRACT(payloadJson, '$.model') as model,
  JSON_EXTRACT(payloadJson, '$.error_count') as error_count,
  JSON_EXTRACT(payloadJson, '$.total_predictions') as total_predictions,
  ROUND(
    (JSON_EXTRACT(payloadJson, '$.error_count') / 
     JSON_EXTRACT(payloadJson, '$.total_predictions')) * 100, 2
  ) as error_rate_percent,
  timestamp
FROM metrics
WHERE
  metric_name = 'prediction_error_rate'
  AND attributes['team'] = 'IA'
ORDER BY timestamp DESC
```

---

## 📉 Troubleshooting

| Problema | Solução |
|----------|---------|
| Sem dados no SigNoz | Verifique se backend está enviando via OTEL_EXPORTER_OTLP_ENDPOINT |
| Endpoint OTEL 4318 não acessível | `docker ps` → verifique se container está rodando |
| Dashboard vazio | Aguarde 1 min após primeiro envio de métrica |
| Query lenta | Reduza time range ou adicione índices |
| Alertas não disparam | Verifique Notification Channel configurado |

---

## 🧪 Teste Completo

```bash
# 1. Levantar SigNoz
docker-compose -f docker-compose-signoz.yml up -d

# 2. Esperar 30 segundos para inicializar
sleep 30

# 3. Enviar métrica de teste (IoT)
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-iot" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IOT",
    "timestamp": "2025-11-20T14:30:00Z",
    "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\"}"
  }'

# 4. Enviar métrica de teste (IA)
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IA",
    "timestamp": "2025-11-20T15:00:00Z",
    "payloadJson": "{\"metric\":\"model_accuracy\",\"value\":0.95,\"model\":\"v2.1\"}"
  }'

# 5. Acessar SigNoz
# Abra http://localhost:3301 no navegador

# 6. Criar dashboard e adicionar widgets
# Siga os passos acima
```

---

## 📞 Suporte

Documentação oficial SigNoz: https://signoz.io/docs/

Repositório: https://github.com/humanize/humainze-dash

