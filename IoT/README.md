# 🏢 Sistema IoT - Monitoramento de Ambiente de Trabalho

## 📋 Visão Geral

Sistema IoT para **monitoramento inteligente de ambientes de trabalho**, alinhado ao tema **"O Futuro do Trabalho"** da FIAP.

### Problema

Com o trabalho híbrido e preocupação crescente com bem-estar, é essencial monitorar:
- 🌡️ **Temperatura** - Conforto térmico
- 💧 **Umidade** - Qualidade do ar
- ☁️ **CO2/Qualidade do Ar** - Ventilação adequada
- 💡 **Luminosidade** - Iluminação apropriada

### Solução

Sistema IoT com **ESP32 + sensores** que:
1. Coleta dados ambientais a cada 30 segundos
2. Envia via **HTTP/JSON** para backend Java
3. Persiste em banco de dados (OracleDB/H2)
4. Visualiza em **Dashboard Streamlit** com alertas

## 🎯 Requisitos FIAP Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| **Sistema IoT** | ✅ | ESP32 + DHT22 + MQ-135 + LDR |
| **Hardware** | ✅ | ESP32 simulado no Wokwi |
| **Dashboard** | ✅ | Streamlit com Plotly (tempo real) |
| **Gateway** | ✅ | Backend Java (Spring Boot) |
| **Protocolo HTTP** | ✅ | POST /otel/v1/metrics (JSON) |
| **Protocolo MQTT** | ⚠️ | Implementável (opcional) |
| **Banco de Dados** | ✅ | OracleDB (prod) / H2 (dev) |
| **Tema "Futuro do Trabalho"** | ✅ | Monitoramento de bem-estar |

## 🔧 Hardware

### Componentes

- **1x ESP32** - Microcontrolador WiFi
- **1x DHT22** - Sensor de temperatura e umidade
- **1x MQ-135** - Sensor de qualidade do ar (CO2/gases)
- **1x LDR** - Sensor de luminosidade
- **Resistores** - 10kΩ para pull-up/divisor tensão

### Diagrama de Conexões

```
ESP32 DevKit v1
├── GPIO 4  → DHT22 (Data)
├── GPIO 34 → MQ-135 (Analog Out)
├── GPIO 35 → LDR (Analog)
├── 3.3V    → VCC sensores
└── GND     → GND sensores
```

## 📊 Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     ARQUITETURA IoT                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│   ESP32      │
│  + DHT22     │  ──► Coleta a cada 30s
│  + MQ-135    │
│  + LDR       │
└──────┬───────┘
       │ WiFi
       │ HTTP POST /otel/v1/metrics
       │ JSON: {"metric":"temperature","value":25.5}
       ▼
┌─────────────────────────────────────────────┐
│       Backend Java (Spring Boot)            │
│  • Recebe métricas                          │
│  • Valida JWT (team: IOT)                   │
│  • Persiste em OracleDB/H2                  │
│  • Expõe APIs REST (/export/metrics)        │
└─────────────────────────────────────────────┘
       │
       │ GET /export/metrics?teamTag=IOT
       │
       ▼
┌─────────────────────────────────────────────┐
│       Dashboard Streamlit                    │
│  • Gráficos Plotly (time series)            │
│  • Alertas (temp alta, CO2 crítico)         │
│  • Auto-refresh 5s                          │
└─────────────────────────────────────────────┘
```

## 🚀 Como Executar

### Opção 1: Simulação no Wokwi (Recomendado)

1. **Abrir projeto no Wokwi:**
   ```
   https://wokwi.com/projects/new/esp32
   ```

2. **Copiar código:**
   - `esp32_sensor_monitor.ino` → Editor Wokwi
   - `diagram.json` → Configuração de hardware

3. **Configurar WiFi:**
   ```cpp
   const char* ssid = "Wokwi-GUEST";
   const char* password = "";
   ```

4. **Configurar Backend:**
   ```cpp
   const char* BACKEND_HOST = "SEU-IP-PUBLICO";  // ngrok ou IP público
   const int BACKEND_PORT = 8080;
   ```

5. **Executar simulação:**
   - Clique em "Start Simulation"
   - Monitor Serial mostra logs
   - Backend recebe métricas

### Opção 2: PlatformIO + Wokwi Offline

1. **Instalar PlatformIO:**
   ```bash
   # VS Code Extension
   code --install-extension platformio.platformio-ide
   ```

2. **Criar projeto:**
   ```bash
   pio project init --board esp32dev
   cp esp32_sensor_monitor.ino src/main.cpp
   ```

3. **Instalar dependências:**
   ```ini
   # platformio.ini
   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps = 
       adafruit/DHT sensor library@^1.4.4
       bblanchon/ArduinoJson@^6.21.3
   ```

4. **Simular com Wokwi:**
   ```bash
   pio run --target wokwi
   ```

### Opção 3: Hardware Real

1. **Componentes físicos:**
   - ESP32 DevKit v1
   - DHT22, MQ-135, LDR
   - Protoboard + jumpers

2. **Upload via USB:**
   ```bash
   pio run --target upload
   pio device monitor
   ```

## 📡 Comunicação com Backend

### 1️⃣ Autenticação

```cpp
// Login para obter token JWT
HTTPClient http;
http.begin("http://backend:8080/auth/login");
http.addHeader("Content-Type", "application/json");

String loginPayload = "{\"team\":\"IOT\",\"secret\":\"iot-secret\"}";
int httpCode = http.POST(loginPayload);

if (httpCode == 200) {
  String response = http.getString();
  // Extrair token do JSON
  jwtToken = extractToken(response);
}
```

### 2️⃣ Enviar Métrica

```cpp
void enviarMetrica(String metric, float value) {
  HTTPClient http;
  http.begin("http://backend:8080/otel/v1/metrics");
  http.addHeader("Authorization", "Bearer " + jwtToken);
  http.addHeader("Content-Type", "application/json");

  // Construir payload
  String timestamp = getISOTimestamp();
  String payloadJson = String("{\"metric\":\"") + metric + 
                       "\",\"value\":" + String(value, 2) + 
                       ",\"location\":\"sala-1\",\"sensor\":\"DHT22\"}";
  
  String requestBody = "{\"teamTag\":\"IOT\",\"timestamp\":\"" + 
                       timestamp + "\",\"payloadJson\":\"" + 
                       escapeJson(payloadJson) + "\"}";

  int httpCode = http.POST(requestBody);
  
  Serial.print("Métrica enviada: ");
  Serial.print(metric);
  Serial.print(" = ");
  Serial.print(value);
  Serial.print(" | Status: ");
  Serial.println(httpCode);
}
```

## 📊 Métricas Coletadas

| Métrica | Sensor | Unidade | Intervalo Normal | Alerta |
|---------|--------|---------|------------------|--------|
| `temperature` | DHT22 | °C | 20-26°C | >28°C ou <18°C |
| `humidity` | DHT22 | % | 40-60% | >70% ou <30% |
| `air_quality_ppm` | MQ-135 | ppm | <1000 | >1500 |
| `luminosity_lux` | LDR | lux | 300-500 | <200 ou >800 |

## 🎨 Dashboard

### Visualizações Disponíveis

1. **Time Series (Temperatura)**
   - Linha temporal últimas 6 horas
   - Threshold de conforto (20-26°C)

2. **Gauge (Qualidade do Ar)**
   - Indicador CO2
   - Cores: Verde (<1000), Amarelo (1000-1500), Vermelho (>1500)

3. **Bar Chart (Comparação)**
   - Temperatura, Umidade, Luminosidade por sala

4. **Alertas**
   - Banner vermelho quando valores críticos
   - Histórico de alertas resolvidos

## 🧪 Testes

⚠️ **IMPORTANTE:** Veja o guia completo de testes em [`GUIA_TESTES.md`](./GUIA_TESTES.md)

### Testes Disponíveis

| # | Arquivo | Objetivo |
|---|---------|----------|
| 1 | `test_conectividade.ino` | Validar WiFi + NTP |
| 2 | `test_sensores.ino` | Validar DHT22 + MQ135 + LDR |
| 3 | `test_backend.ino` | Validar login JWT + POST métricas |
| 4 | `esp32_sensor_monitor.ino` | Sistema completo end-to-end |

### Teste Rápido 1: Conectividade

```bash
# Copiar teste para src/main.cpp
Copy-Item IoT\testes\test_conectividade.ino src\main.cpp

# Compilar e upload
pio run --target upload

# Monitor serial
pio device monitor --baud 115200
```

**Saída esperada:**
```
✓ WiFi conectado! IP: 192.168.1.42
✓ NTP sincronizado!
  Timestamp ISO: 2025-11-22T18:30:00Z
```

### Teste Rápido 2: Sensores

```powershell
# Usar Wokwi para simular sensores
# Copiar test_sensores.ino para editor Wokwi
# Saída esperada:
```

```text
🌡️  Temperatura: 23.5°C
💧 Umidade: 55.2%
☁️  CO2: 800 ppm
💡 Luminosidade: 500 lux
✓ Todos os valores válidos
```

### Teste Rápido 3: Backend

```powershell
# 1. Iniciar backend
docker-compose up -d backend

# 2. Ajustar IP no test_backend.ino (linha 29)
# const char* BACKEND_HOST = "SEU_IP_AQUI";

# 3. Upload e monitor
pio run --target upload; pio device monitor
```

**Saída esperada:**

```text
✓ Login bem-sucedido! Token: eyJhbGc...
✓ Métrica enviada com sucesso!
  HTTP Code: 201
```

### Documentação Completa de Testes

📖 **Veja o guia completo:** [`GUIA_TESTES.md`](./GUIA_TESTES.md)

O guia contém:
- 4 testes detalhados com pré-requisitos
- Troubleshooting completo
- Critérios de aprovação
- Checklist FIAP
- Roteiro para vídeo de 3 minutos

## 📁 Estrutura de Arquivos

```
IoT/
├── README.md                      ← Este arquivo
├── requisitos-fiap.txt            ← Requisitos originais FIAP
├── esp32_sensor_monitor.ino      ← Código principal ESP32
├── diagram.json                   ← Diagrama Wokwi
├── platformio.ini                 ← Configuração PlatformIO
├── wokwi.toml                     ← Configuração Wokwi offline
└── testes/
    ├── test_conectividade.ino     ← Teste WiFi
    ├── test_sensores.ino          ← Teste leitura
    └── test_backend.ino           ← Teste HTTP
```

## 🎓 Alinhamento com "Futuro do Trabalho"

### Problema Real

Ambientes de trabalho mal monitorados afetam:
- **Produtividade** - Temperatura inadequada reduz performance em 10-15%
- **Saúde** - CO2 alto causa fadiga, dores de cabeça
- **Bem-estar** - Umidade incorreta aumenta doenças respiratórias

### Solução Proposta

Sistema IoT automatiza monitoramento e **previne problemas antes que ocorram**:

1. **Alerta Proativo** - Notifica gestor quando CO2 > 1500 ppm
2. **Histórico** - Identifica padrões (ex: sala X sempre muito quente às 15h)
3. **Ação Automática** - Integração futura com ar-condicionado (atuadores)
4. **Compliance** - NR-17 exige temperatura 20-23°C em escritórios

### Benefícios

- ✅ **Redução de custos** - Energia otimizada
- ✅ **Aumento de produtividade** - Ambiente ideal
- ✅ **Conformidade legal** - NR-17, ISO 45001
- ✅ **Sustentabilidade** - Menos desperdício energético

## 🚀 Roadmap Futuro

### Fase 2 (Opcional)

- [ ] **MQTT** - Adicionar broker Mosquitto
- [ ] **Atuadores** - Controlar ar-condicionado/ventilação
- [ ] **Node-RED** - Fluxo visual de automação
- [ ] **Machine Learning** - Predição de desconforto
- [ ] **Múltiplas Salas** - Escalabilidade para prédio inteiro
- [ ] **Integração Slack** - Alertas via mensagem

## 📞 Suporte

Para dúvidas:
1. Consulte [../docs/INTEGRATION_GUIDE_IOT.md](../docs/INTEGRATION_GUIDE_IOT.md)
2. Teste com `testes/test_*.ino`
3. Abra issue no [GitHub](https://github.com/viniruggeri/humainze-java/issues)

---

**Equipe:**
- Barbara Bonome Filipus (RM560431)
- Vinicius Lira Ruggeri (RM560593)
- Yasmin Pereira da Silva (RM560039)

**Turma:** 2TDSPR  
**Data:** 22/11/2025  
**Disciplina:** DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA
