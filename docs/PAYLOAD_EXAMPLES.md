# 📋 Exemplos de Payloads JSON - Copy & Paste Ready

## 🔐 Autenticação

### Obter JWT com API Key

```bash
curl -X POST http://localhost:8080/auth/token \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json"
```

**Resposta:**
```json
{
  "token": "eyJhbGciOiJIUzUxMiJ9..."
}
```

---

## 📊 Métricas IoT

### 1. Temperatura (DHT22)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:30:00Z",
  "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\",\"unit\":\"celsius\"}"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-iot" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IOT",
    "timestamp": "2025-11-20T14:30:00Z",
    "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\",\"unit\":\"celsius\"}"
  }'
```

---

### 2. Umidade (DHT22)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:30:00Z",
  "payloadJson": "{\"metric\":\"humidity\",\"value\":65.2,\"sensor\":\"DHT22\",\"location\":\"sala-1\",\"unit\":\"percent\"}"
}
```

---

### 3. CO2 (MQ-135)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:31:00Z",
  "payloadJson": "{\"metric\":\"co2_ppm\",\"value\":850,\"sensor\":\"MQ-135\",\"location\":\"sala-2\",\"threshold\":1000}"
}
```

---

### 4. Luminosidade (LDR)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:32:00Z",
  "payloadJson": "{\"metric\":\"brightness_percent\",\"value\":78,\"sensor\":\"LDR\",\"location\":\"sala-1\",\"unit\":\"percent\"}"
}
```

---

### 5. Movimento (PIR)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:33:00Z",
  "payloadJson": "{\"metric\":\"motion_detected\",\"value\":1,\"sensor\":\"PIR\",\"location\":\"porta-entrada\"}"
}
```

---

### 6. Bateria do Dispositivo

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:34:00Z",
  "payloadJson": "{\"metric\":\"battery_percent\",\"value\":87,\"device_id\":\"sensor-sala-1\",\"unit\":\"percent\"}"
}
```

---

### 7. Pressão Atmosférica (BMP280)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:35:00Z",
  "payloadJson": "{\"metric\":\"pressure_hpa\",\"value\":1013.25,\"sensor\":\"BMP280\",\"location\":\"sala-1\"}"
}
```

---

### 8. Altitude (BMP280)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:36:00Z",
  "payloadJson": "{\"metric\":\"altitude_meters\",\"value\":156.3,\"sensor\":\"BMP280\",\"location\":\"sala-1\"}"
}
```

---

### 9. Umidade do Solo (Capacitivo)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:37:00Z",
  "payloadJson": "{\"metric\":\"soil_moisture_percent\",\"value\":62.3,\"sensor\":\"Capacitive\",\"location\":\"jardim-1\"}"
}
```

---

### 10. Ruído Ambiente (INMP441)

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:38:00Z",
  "payloadJson": "{\"metric\":\"noise_level_db\",\"value\":65.2,\"sensor\":\"INMP441\",\"location\":\"sala-reunioes\"}"
}
```

---

## 🤖 Métricas IA

### 1. Acurácia do Modelo

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:00:00Z",
  "payloadJson": "{\"metric\":\"model_accuracy\",\"value\":0.95,\"model\":\"v2.1\",\"dataset\":\"test_set\",\"epoch\":50}"
}
```

---

### 2. Loss do Modelo

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:01:00Z",
  "payloadJson": "{\"metric\":\"model_loss\",\"value\":0.12,\"model\":\"v2.1\",\"dataset\":\"training\",\"epoch\":50}"
}
```

---

### 3. Latência de Inferência

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:02:00Z",
  "payloadJson": "{\"metric\":\"inference_time_ms\",\"value\":125,\"model\":\"v2.1\",\"endpoint\":\"/predict\",\"batch_size\":32}"
}
```

---

### 4. Precisão (Precision)

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:03:00Z",
  "payloadJson": "{\"metric\":\"model_precision\",\"value\":0.92,\"model\":\"v2.1\",\"class\":\"anomaly\",\"dataset\":\"test\"}"
}
```

---

### 5. Recall (Sensitivity)

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:04:00Z",
  "payloadJson": "{\"metric\":\"model_recall\",\"value\":0.88,\"model\":\"v2.1\",\"class\":\"anomaly\",\"dataset\":\"test\"}"
}
```

---

### 6. F1 Score

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:05:00Z",
  "payloadJson": "{\"metric\":\"model_f1_score\",\"value\":0.90,\"model\":\"v2.1\",\"dataset\":\"test\"}"
}
```

---

### 7. Detecção de Drift (KL Divergence)

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:06:00Z",
  "payloadJson": "{\"metric\":\"model_drift_score\",\"value\":0.23,\"model\":\"v2.1\",\"method\":\"kullback_leibler\",\"threshold\":0.3,\"feature\":\"user_age\"}"
}
```

---

### 8. Uso de GPU

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:07:00Z",
  "payloadJson": "{\"metric\":\"gpu_usage_percent\",\"value\":78.5,\"model\":\"v2.1\",\"gpu_id\":0,\"gpu_name\":\"NVIDIA A100\"}"
}
```

---

### 9. Memória Utilizada

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:08:00Z",
  "payloadJson": "{\"metric\":\"memory_usage_mb\",\"value\":2048,\"model\":\"v2.1\",\"total_memory_mb\":8192,\"memory_type\":\"GPU\"}"
}
```

---

### 10. Taxa de Erro na Predição

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:09:00Z",
  "payloadJson": "{\"metric\":\"prediction_error_rate\",\"value\":0.03,\"model\":\"v2.1\",\"total_predictions\":1000,\"error_count\":30}"
}
```

---

### 11. AUC-ROC Score

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:10:00Z",
  "payloadJson": "{\"metric\":\"model_auc_roc\",\"value\":0.98,\"model\":\"v2.1\",\"dataset\":\"test\"}"
}
```

---

### 12. Taxa de Predições em Tempo Real

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:11:00Z",
  "payloadJson": "{\"metric\":\"predictions_per_second\",\"value\":850,\"model\":\"v2.1\",\"endpoint\":\"/predict\",\"time_window_seconds\":60}"
}
```

---

### 13. Uso de CPU

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:12:00Z",
  "payloadJson": "{\"metric\":\"cpu_usage_percent\",\"value\":45.2,\"model\":\"v2.1\",\"num_cores\":8}"
}
```

---

### 14. Cache Hit Rate

```json
{
  "teamTag": "IA",
  "timestamp": "2025-11-20T15:13:00Z",
  "payloadJson": "{\"metric\":\"cache_hit_rate\",\"value\":0.87,\"cache_type\":\"model_output\",\"total_requests\":10000,\"cache_hits\":8700}"
}
```

---

## 🚨 Alertas IA (com GPT-4)

### 1. Alerta de Drift

```json
{
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Drift detectado no modelo v2.1 - acurácia caiu para 0.75 (limite: 0.80). Feature 'user_age_distribution' apresenta mudança significativa de 32%. Retrainamento automático será disparado em 5 minutos."
}
```

---

### 2. Alerta de Erro em Predição

```json
{
  "teamTag": "IA",
  "type": "MODEL_ERROR",
  "message": "Erro em predição detectado: 42 requisições retornaram NaN (3.2% do total). Input data pode conter valores inválidos ou fora do range esperado. Verificar pipeline de pré-processamento e validação de entrada."
}
```

---

### 3. Alerta de Serviço Offline

```json
{
  "teamTag": "IA",
  "type": "SERVICE_DOWN",
  "message": "Serviço de inferência offline por 5 minutos (desde 15:10). Último heartbeat bem-sucedido: 2025-11-20T15:05:00Z. Status HTTP atual: 503. Tentando reconectar a cada 10 segundos."
}
```

---

### 4. Alerta Customizado - Consumo Alto de GPU

```json
{
  "teamTag": "IA",
  "type": "CUSTOM",
  "message": "Consumo de GPU acima do normal: 92% (threshold configurado: 80%). Possível fila de predições acumulada ou modelo mal otimizado. Considerar escalar recursos ou distribuir carga entre GPUs."
}
```

---

### 5. Alerta Customizado - Memory Leak

```json
{
  "teamTag": "IA",
  "type": "CUSTOM",
  "message": "Possível memory leak detectado: memória crescendo linearmente (+2.5% a cada 5 min) sem picos de carga correspondentes. Investigar processes de limpeza de recursos e liberação de memória não utilizada."
}
```

---

### 6. Alerta Customizado - Latência Alta

```json
{
  "teamTag": "IA",
  "type": "CUSTOM",
  "message": "Latência de inferência acima do normal: 523ms (SLA: 300ms). Possível gargalo em pré-processamento ou modelo sobrecarregado. Verificar CPU/GPU e considerar otimizações."
}
```

---

### 7. Alerta Customizado - Taxa de Erro

```json
{
  "teamTag": "IA",
  "type": "CUSTOM",
  "message": "Taxa de erro em predição acima do threshold: 8.5% (limite: 5%). Modelo pode estar degradado ou dataset de entrada mudou. Revalidação e potencial retrain recomendados."
}
```

---

## 📥 Requisições de Leitura

### Listar Últimas Métricas IoT

```bash
curl "http://localhost:8080/export/metrics?teamTag=IOT&page=0&size=20&sort=timestamp,desc" \
  -H "X-API-KEY: chave-iot"
```

---

### Listar Últimas Métricas IA

```bash
curl "http://localhost:8080/export/metrics?teamTag=IA&page=0&size=20&sort=timestamp,desc" \
  -H "X-API-KEY: chave-ia"
```

---

### Listar Alertas

```bash
curl "http://localhost:8080/alerts?teamTag=IA&page=0&size=20" \
  -H "X-API-KEY: chave-ia"
```

---

### Resolver Alerta

```bash
curl -X PUT "http://localhost:8080/alerts/1/resolve" \
  -H "X-API-KEY: chave-ia"
```

---

## 📊 Visualização no Dashboard

Após enviar métricas, acesse o **Dashboard Streamlit** para visualizar:

**URL Local**: `http://localhost:8501`  
**URL Azure**: `http://172.161.94.218:8501`

### Exemplos de Visualização

**Tab "📡 Métricas IoT":**
- Time series de temperatura, umidade, CO2
- Gauge com valores atuais
- Filtros por sensor e local

**Tab "🤖 Métricas IA":**
- Gráficos de acurácia, loss, drift
- Line charts de evolução temporal
- Filtros por modelo e dataset

**Tab "🚨 Alertas":**
- Banner com contagem de alertas ativos
- Histórico completo com paginação
- Botão para resolver alertas

---

## 📝 Template Genérico

Para qualquer métrica, use este template:

```json
{
  "teamTag": "IA_ou_IOT",
  "timestamp": "2025-11-20T15:00:00Z",
  "payloadJson": "{\"metric\":\"NOME_METRICA\",\"value\":VALOR,\"campo1\":\"valor1\",\"campo2\":NUMERO}"
}
```

---

## 🧪 Teste Rápido - One-liner

```bash
# IoT - Temperatura
curl -X POST http://localhost:8080/otel/v1/metrics -H "X-API-KEY: chave-iot" -H "Content-Type: application/json" -d '{"teamTag":"IOT","timestamp":"2025-11-20T14:30:00Z","payloadJson":"{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\"}"}'

# IA - Acurácia
curl -X POST http://localhost:8080/otel/v1/metrics -H "X-API-KEY: chave-ia" -H "Content-Type: application/json" -d '{"teamTag":"IA","timestamp":"2025-11-20T15:00:00Z","payloadJson":"{\"metric\":\"model_accuracy\",\"value\":0.95,\"model\":\"v2.1\"}"}'

# Alerta
curl -X POST http://localhost:8080/alerts -H "X-API-KEY: chave-ia" -H "Content-Type: application/json" -d '{"teamTag":"IA","type":"DRIFT","message":"Drift detectado"}'
```

---

## 📋 Checklist de Envio

- [ ] `teamTag` correto (IA ou IOT)
- [ ] `timestamp` em ISO 8601 (2025-11-20T14:30:00Z)
- [ ] `payloadJson` é uma STRING (JSON encoded)
- [ ] Todos os campos de `payloadJson` têm nomes significativos
- [ ] API Key correta no header `X-API-KEY`
- [ ] HTTP 200/201 recebido
- [ ] Métrica aparece em `/export/metrics`
- [ ] Dashboard visualizando dados (porta 8501)

