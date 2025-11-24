# 📡 Guia de Integração - Time de IoT

## 📏 Visão Geral

Este guia descreve como dispositivos IoT (Arduino, ESP32, Raspberry Pi, etc.) enviam dados para o **backend Java Humainze** para:

1. **Autenticar** via JWT (login simples)
2. **Enviar métricas** de sensores (temperatura, umidade, CO2, etc.)
3. **Persistir dados** em banco relacional (OracleDB/H2)
4. **Visualizar tudo** no **Dashboard Streamlit customizado**

### Por que Backend Java?

✅ **Open-source completo** - solução sem dependências externas  
✅ **Persistência em banco SQL** - OracleDB (prod) ou H2 (dev)  
✅ **APIs REST com paginação** - `/export/metrics`, `/export/traces`, `/export/logs`  
✅ **Dashboard customizável** - Streamlit + Plotly, fácil de modificar  
✅ **Sistema de alertas integrado** - banner em tempo real + histórico

---

## 🔐 Autenticação

### Login e Obtenção de Token JWT

O time IoT tem credenciais pré-cadastradas:
- **Team:** `IOT`
- **Secret:** `iot-secret`

**Passo 1: Login**

```http
POST http://backend:8080/auth/login
Content-Type: application/json

{
  "team": "IOT",
  "secret": "iot-secret"
}
```

**Resposta:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "team": "IOT",
  "roles": ["ROLE_IOT"]
}
```

**Passo 2: Usar Token**

Em toda requisição subsequente, adicione o header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

### Configurar no Dispositivo

**Arduino/ESP32 com WiFi**:

```cpp
#define API_KEY "chave-iot"
#define HUMAINZE_HOST "192.168.1.100"  // IP do seu backend
#define HUMAINZE_PORT 8080
#define TEAM_TAG "IOT"
```

**Python (Raspberry Pi)**:

```python
import os

API_KEY = os.getenv("IOT_API_KEY", "chave-iot")
HUMAINZE_HOST = os.getenv("HUMAINZE_HOST", "localhost")
HUMAINZE_PORT = int(os.getenv("HUMAINZE_PORT", "8080"))
HUMAINZE_BASE_URL = f"http://{HUMAINZE_HOST}:{HUMAINZE_PORT}"
TEAM_TAG = "IOT"
```

---

## 📊 Enviar Métricas de Sensores

### Endpoint

```
POST /otel/v1/metrics
```

### Payload Padrão

```json
{
  "teamTag": "IOT",
  "timestamp": "2025-11-20T14:30:00Z",
  "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\"}"
}
```

---

## 🔧 Exemplos por Plataforma

### 1️⃣ Arduino/ESP32 (C++)

#### Bibliotecas Necessárias

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
```

#### Código Completo

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"
#include <time.h>

// Configurações WiFi
const char* ssid = "SSID_WiFi";
const char* password = "Senha_WiFi";

// Configurações Humainze
const char* API_KEY = "chave-iot";
const char* HUMAINZE_HOST = "192.168.1.100";
const int HUMAINZE_PORT = 8080;
const char* TEAM_TAG = "IOT";

// Sensor DHT22
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// Identificador do dispositivo
const char* DEVICE_ID = "sensor-sala-1";
const char* DEVICE_LOCATION = "sala-1";

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Conectar ao WiFi
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  }
  
  // Configurar sincronização de hora (necessária para timestamp)
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.println("Sincronizando hora...");
  time_t now = time(nullptr);
  while (now < 24 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("\n✓ Hora sincronizada!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Ler dados do sensor
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if (!isnan(temperature) && !isnan(humidity)) {
      Serial.printf("Temperatura: %.2f°C, Umidade: %.2f%%\n", temperature, humidity);
      
      // Enviar temperatura
      sendMetric("temperature", temperature, "{\"sensor\":\"DHT22\",\"location\":\"" + String(DEVICE_LOCATION) + "\"}");
      
      // Enviar umidade
      sendMetric("humidity", humidity, "{\"sensor\":\"DHT22\",\"location\":\"" + String(DEVICE_LOCATION) + "\"}");
    }
  }
  
  delay(60000); // Enviar a cada 60 segundos
}

void sendMetric(const char* metricName, float value, String extraJson) {
  HTTPClient http;
  
  // Construir URL
  String url = String("http://") + HUMAINZE_HOST + ":" + HUMAINZE_PORT + "/otel/v1/metrics";
  
  // Construir timestamp ISO 8601
  time_t now = time(nullptr);
  struct tm* timeinfo = gmtime(&now);
  char timestamp[30];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", timeinfo);
  
  // Construir payloadJson
  StaticJsonDocument<256> payloadDoc;
  payloadDoc["metric"] = metricName;
  payloadDoc["value"] = value;
  payloadDoc["device_id"] = DEVICE_ID;
  
  // Parse extra JSON
  StaticJsonDocument<128> extraDoc;
  deserializeJson(extraDoc, extraJson);
  for (JsonPair p : extraDoc.as<JsonObject>()) {
    payloadDoc[p.key()] = p.value();
  }
  
  String payloadJsonStr;
  serializeJson(payloadDoc, payloadJsonStr);
  
  // Construir body
  StaticJsonDocument<512> body;
  body["teamTag"] = TEAM_TAG;
  body["timestamp"] = timestamp;
  body["payloadJson"] = payloadJsonStr;
  
  String bodyStr;
  serializeJson(body, bodyStr);
  
  // Fazer requisição HTTP
  http.begin(url);
  http.addHeader("X-API-KEY", API_KEY);
  http.addHeader("Content-Type", "application/json");
  
  int httpResponseCode = http.POST(bodyStr);
  
  if (httpResponseCode > 0) {
    Serial.printf("✓ Métrica enviada: %s (HTTP %d)\n", metricName, httpResponseCode);
  } else {
    Serial.printf("✗ Erro ao enviar métrica: %s\n", http.errorToString(httpResponseCode).c_str());
  }
  
  http.end();
}
```

**Instalação no Arduino IDE**:
```
Sketch → Include Library → Manage Libraries
Buscar: "ArduinoJson"
Buscar: "DHT sensor library"
Instalar ambas
```

---

### 2️⃣ Raspberry Pi (Python)

#### Instalação

```bash
pip install requests Adafruit-DHT
```

#### Código Completo

```python
#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime, timezone
import Adafruit_DHT

# Configurações
API_KEY = "chave-iot"
HUMAINZE_HOST = "localhost"
HUMAINZE_PORT = 8080
HUMAINZE_BASE_URL = f"http://{HUMAINZE_HOST}:{HUMAINZE_PORT}"
TEAM_TAG = "IOT"

# Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

# Dispositivo
DEVICE_ID = "sensor-sala-1"
DEVICE_LOCATION = "sala-1"

class HumainzeIoTClient:
    def __init__(self, api_key, base_url):
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
            "value": value,
            "device_id": DEVICE_ID
        }
        
        if extra_data:
            payload_data.update(extra_data)
        
        body = {
            "teamTag": TEAM_TAG,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "payloadJson": json.dumps(payload_data)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/otel/v1/metrics",
                json=body,
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Métrica enviada: {metric_name} = {value}")
                return True
            else:
                print(f"✗ Erro ao enviar métrica: HTTP {response.status_code}")
                print(f"  Resposta: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Erro de conexão: {e}")
            return False

def main():
    client = HumainzeIoTClient(API_KEY, HUMAINZE_BASE_URL)
    
    print("🌡️  Iniciando coleta de dados do sensor DHT22...")
    print(f"📍 Localização: {DEVICE_LOCATION}")
    print(f"🆔 Dispositivo: {DEVICE_ID}")
    print()
    
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            
            if humidity is not None and temperature is not None:
                print(f"📊 Leitura: {temperature:.2f}°C, {humidity:.2f}%")
                
                # Enviar temperatura
                client.send_metric(
                    "temperature",
                    round(temperature, 2),
                    {
                        "sensor": "DHT22",
                        "location": DEVICE_LOCATION,
                        "unit": "celsius"
                    }
                )
                
                # Enviar umidade
                client.send_metric(
                    "humidity",
                    round(humidity, 2),
                    {
                        "sensor": "DHT22",
                        "location": DEVICE_LOCATION,
                        "unit": "percent"
                    }
                )
                
                # Opcional: enviar índice de calor
                heat_index = calculate_heat_index(temperature, humidity)
                client.send_metric(
                    "heat_index",
                    round(heat_index, 2),
                    {
                        "sensor": "DHT22",
                        "location": DEVICE_LOCATION,
                        "unit": "celsius"
                    }
                )
            else:
                print("✗ Erro ao ler sensor")
            
            print()
            time.sleep(60)  # Enviar a cada 60 segundos
        
        except KeyboardInterrupt:
            print("\n🛑 Encerrando...")
            break
        except Exception as e:
            print(f"✗ Erro: {e}")
            time.sleep(5)

def calculate_heat_index(temp_c, humidity):
    """Calcula índice de calor (Steadman)"""
    temp_f = (temp_c * 9/5) + 32
    c1, c2, c3 = -42.379, 2.04901523, 10.14333127
    c4, c5, c6 = -0.22475541, -0.00683783, -0.05481717
    
    hi_f = (c1 + c2*temp_f + c3*humidity + c4*temp_f*humidity +
            c5*temp_f*temp_f + c6*humidity*humidity)
    
    return (hi_f - 32) * 5/9

if __name__ == "__main__":
    main()
```

**Executar com systemd** (auto-iniciar):

```bash
sudo nano /etc/systemd/system/humainze-iot.service
```

```ini
[Unit]
Description=Humainze IoT Sensor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/humainze-iot
ExecStart=/usr/bin/python3 /home/pi/humainze-iot/sensor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable humainze-iot
sudo systemctl start humainze-iot
```

---

### 3️⃣ Outros Sensores (Genérico)

#### Sensor de CO2 (MQ-135)

```python
def read_co2_sensor(analog_pin):
    """Lê sensor MQ-135 de CO2"""
    # Calibração específica do seu sensor
    value = read_analog(analog_pin)  # 0-4095
    ppm = (value / 4095.0) * 5000    # Escala até 5000 ppm
    return ppm

# Enviar
client.send_metric(
    "co2_ppm",
    read_co2_sensor(A0),
    {"sensor": "MQ-135", "location": "sala-1"}
)
```

#### Sensor de Luminosidade (LDR)

```python
def read_light_sensor(analog_pin):
    """Lê sensor LDR"""
    value = read_analog(analog_pin)
    brightness = (value / 4095.0) * 100  # Percentual 0-100%
    return brightness

# Enviar
client.send_metric(
    "brightness_percent",
    read_light_sensor(A1),
    {"sensor": "LDR", "location": "sala-1"}
)
```

#### Sensor de Movimento (PIR)

```python
def read_motion_sensor(digital_pin):
    """Lê sensor PIR de movimento"""
    return 1 if read_digital(digital_pin) else 0

# Enviar
client.send_metric(
    "motion_detected",
    read_motion_sensor(D5),
    {"sensor": "PIR", "location": "sala-1"}
)
```

---

## 📥 Receber Métricas do Backend

### Endpoint

```
GET /export/metrics?page=0&size=100&sort=timestamp,desc
```

### Exemplo - Dashboard Local

```python
import requests
import json

def get_latest_metrics(team_tag="IOT", limit=20):
    """Busca as últimas métricas"""
    headers = {
        "X-API-KEY": "chave-iot",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"http://localhost:8080/export/metrics",
        params={
            "teamTag": team_tag,
            "page": 0,
            "size": limit,
            "sort": "timestamp,desc"
        },
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Últimas {len(data['content'])} métricas:\n")
        
        for metric in data["content"]:
            payload = json.loads(metric["payloadJson"])
            print(f"⏰ {metric['timestamp']}")
            print(f"   📡 {payload['metric']}: {payload['value']}")
            print()
        
        return data
    else:
        print(f"✗ Erro: HTTP {response.status_code}")
        return None

# Uso
get_latest_metrics()
```

---

## 📊 Visualizar no Dashboard

### Acesso ao Dashboard Streamlit

**URL Local**: `http://localhost:8501`  
**URL Azure**: `http://172.161.94.218:8501`

### Tab "📡 Métricas IoT"

1. **Selecione período**: última hora, 6h, 24h, 7 dias
2. **Visualize gráficos**:
   - Time Series: Temperatura, Umidade, CO2
   - Gauge: Valores atuais
   - Bar Chart: Comparação entre sensores
3. **Auto-refresh**: atualização automática a cada 5 segundos

### Query Exemplo

```
SELECT
  JSON_EXTRACT(payloadJson, '$.location') as location,
  JSON_EXTRACT(payloadJson, '$.value') as value,
  timestamp
FROM metrics
WHERE
  metric_name = 'temperature'
  AND attributes['team'] = 'IOT'
ORDER BY timestamp DESC
LIMIT 100
```

---

## 🧪 Teste Rápido

### cURL - Enviar Métrica Temperatura

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

### cURL - Enviar Métrica CO2

```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-iot" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IOT",
    "timestamp": "2025-11-20T14:30:00Z",
    "payloadJson": "{\"metric\":\"co2_ppm\",\"value\":850,\"sensor\":\"MQ135\",\"location\":\"sala-2\"}"
  }'
```

### cURL - Listar Métricas

```bash
curl http://localhost:8080/export/metrics?teamTag=IOT&page=0&size=10 \
  -H "X-API-KEY: chave-iot"
```

---

## 📋 Checklist de Integração

- [ ] API Key configurada no dispositivo
- [ ] WiFi/Internet conectados
- [ ] Sensores testados localmente
- [ ] Primeira métrica enviada com sucesso
- [ ] Backend respondendo com HTTP 200/201
- [ ] Métricas aparecendo no dashboard (porta 8501)
- [ ] Dashboard criado e configurado
- [ ] Auto-inicialização configurada (systemd/cron)
- [ ] Alertas de offline configurados

---

## 📊 Métricas Recomendadas

| Sensor | Métrica | Range | Intervalo |
|--------|---------|-------|-----------|
| DHT22 | temperature | -40 a 80°C | 2s |
| DHT22 | humidity | 0-100% | 2s |
| MQ-135 | co2_ppm | 400-5000 | 30s |
| LDR | brightness_percent | 0-100% | 10s |
| PIR | motion_detected | 0-1 | 1s |
| Voltagem | battery_percent | 0-100% | 60s |

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| `401 Unauthorized` | Verifique `X-API-KEY: chave-iot` |
| `Connection timeout` | Verifique IP/porta do backend |
| `Invalid JSON` | Verifique formato do `payloadJson` |
| Sensor não responde | Verifique pinos, bibliotecas, alimentação |
| Dashboard não carrega | Verifique se backend está rodando (porta 8080) |
| WiFi desconecta | Adicione lógica de reconexão automática |

---

## 📞 Suporte

Contate: backend-team@humainze.ai

Repositório: https://github.com/viniruggeri/humainze

