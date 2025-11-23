# Guia de Testes - ESP32 IoT System
**FIAP 2TDSPR - O Futuro do Trabalho**

## 📋 Visão Geral

Este guia documenta os 4 testes principais do sistema IoT de monitoramento de ambientes de trabalho.

**Equipe:**
- Barbara Bonome Filipus (RM560431)
- Vinicius Lira Ruggeri (RM560593)
- Yasmin Pereira da Silva (RM560039)

---

## ✅ Checklist de Testes

| # | Teste | Arquivo | Objetivo | Status |
|---|-------|---------|----------|--------|
| 1 | Conectividade WiFi e NTP | `test_conectividade.ino` | Validar conexão WiFi e sincronização de horário | ⬜ |
| 2 | Leitura de Sensores | `test_sensores.ino` | Validar leitura de DHT22, MQ-135, LDR | ⬜ |
| 3 | Comunicação Backend | `test_backend.ino` | Validar JWT login e envio de métricas | ⬜ |
| 4 | Sistema Completo | `esp32_sensor_monitor.ino` | Validar sistema integrado end-to-end | ⬜ |

---

## 🧪 Teste 1: Conectividade WiFi e NTP

### Objetivo
Verificar se o ESP32 consegue conectar ao WiFi e sincronizar horário via NTP.

### Pré-requisitos
- ESP32 conectado via USB (ou simulador Wokwi)
- Rede WiFi disponível (para Wokwi: "Wokwi-GUEST")

### Executar Teste

**Wokwi Online:**
```bash
1. Abra https://wokwi.com/
2. Crie novo projeto ESP32
3. Cole código de testes/test_conectividade.ino
4. Clique em "Start Simulation"
```

**PlatformIO + Wokwi Offline:**
```powershell
# 1. Copiar código de teste para src/main.cpp
Copy-Item IoT\testes\test_conectividade.ino src\main.cpp

# 2. Compilar
pio run

# 3. Simular com Wokwi
wokwi-cli IoT/diagram.json
```

**Hardware Real:**
```powershell
# 1. Ajustar WiFi SSID e PASSWORD no código
# 2. Copiar para src/main.cpp
# 3. Upload
pio run --target upload

# 4. Monitor serial
pio device monitor --baud 115200
```

### Resultado Esperado

```
╔════════════════════════════════════════════╗
║   TESTE 1: Conectividade WiFi e NTP       ║
╚════════════════════════════════════════════╝

[TESTE 1.1] Conectando WiFi...
✓ WiFi conectado!
  IP: 192.168.1.42
  RSSI: -45 dBm

[TESTE 1.2] Configurando NTP...
✓ NTP sincronizado!
  Timestamp ISO: 2025-11-22T18:30:00Z

════════════════════════════════════════════
Teste 1 concluído!
════════════════════════════════════════════

[2025-11-22T18:30:05Z] Sistema ativo
[2025-11-22T18:30:10Z] Sistema ativo
```

### Critérios de Aprovação
- ✅ WiFi conectado com IP válido
- ✅ RSSI > -70 dBm
- ✅ Timestamp ISO 8601 válido (formato correto)
- ✅ Ano >= 2025 (prova que NTP sincronizou)

---

## 🧪 Teste 2: Leitura de Sensores

### Objetivo
Verificar se todos os sensores estão funcionando e retornando valores válidos.

### Pré-requisitos
- DHT22 conectado ao GPIO 4
- MQ-135 conectado ao GPIO 34 (ADC)
- LDR conectado ao GPIO 35 (ADC)
- Wokwi: `diagram.json` configurado

### Executar Teste

**Wokwi (Recomendado):**
```bash
1. Use arquivo diagram.json
2. Copie código de test_sensores.ino
3. Simule e interaja com os sensores virtuais
```

**Hardware Real:**
```powershell
pio run --target upload
pio device monitor
```

### Resultado Esperado

```
╔════════════════════════════════════════════╗
║   TESTE 2: Leitura de Sensores            ║
╚════════════════════════════════════════════╝

✓ Sensores inicializados

┌─────────────────────────────────────┐
│  Nova Leitura                       │
└─────────────────────────────────────┘

[TESTE 2.1] DHT22 (Temperatura e Umidade)
  🌡️  Temperatura: 23.5°C
  💧 Umidade: 55.2%
  ✓ Temperatura dentro do esperado
  ✓ Umidade dentro do esperado
  🟢 Qualidade do ar: EXCELENTE

[TESTE 2.2] MQ-135 (Qualidade do Ar)
  ☁️  ADC: 1024
  ☁️  CO2: 800 ppm
  ✓ CO2 dentro do esperado
  🟢 Qualidade do ar: EXCELENTE

[TESTE 2.3] LDR (Luminosidade)
  💡 ADC: 2048
  💡 Luminosidade: 500 lux
  ✓ Luminosidade dentro do esperado
  🟢 Luminosidade IDEAL

─────────────────────────────────────

✓ Leitura concluída!
Próxima leitura em 10 segundos...
```

### Critérios de Aprovação
- ✅ DHT22: Temperatura 15-40°C, Umidade 20-95%
- ✅ MQ-135: CO2 400-2000 ppm
- ✅ LDR: Luminosidade 0-1000 lux
- ✅ Nenhum erro de leitura (não NaN)
- ✅ Alertas funcionando corretamente

### Tabela de Alertas

| Sensor | Métrica | Ideal | Alerta Baixo | Alerta Alto |
|--------|---------|-------|--------------|-------------|
| DHT22 | Temperatura | 20-26°C | < 18°C | > 28°C |
| DHT22 | Umidade | 40-60% | < 30% | > 70% |
| MQ-135 | CO2 | < 800 ppm | - | > 1500 ppm |
| LDR | Luminosidade | 300-750 lux | < 200 lux | > 750 lux |

---

## 🧪 Teste 3: Comunicação com Backend

### Objetivo
Validar autenticação JWT e envio de métricas ao backend Java.

### Pré-requisitos
- Backend Java rodando (http://localhost:8080 ou IP na rede)
- Team IOT cadastrado com secret "iot-secret"
- WiFi ESP32 na mesma rede do backend

### Configurar Backend

**1. Iniciar Backend:**
```powershell
# Via Docker Compose
docker-compose up -d backend

# Via Maven
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

**2. Verificar Backend:**
```powershell
curl http://localhost:8080/actuator/health
# Esperado: {"status":"UP"}
```

**3. Ajustar IP no Código:**
```cpp
// Em test_backend.ino, linha 29:
const char* BACKEND_HOST = "192.168.1.100";  // SEU IP LOCAL

// Descobrir IP:
# Windows: ipconfig
# Linux/Mac: ifconfig
```

### Executar Teste

**Wokwi Online:**
- ⚠️ **LIMITAÇÃO**: Wokwi online não acessa redes locais
- Use ngrok ou backend na nuvem

**PlatformIO + Hardware:**
```powershell
# Upload do teste
pio run --target upload

# Monitor serial
pio device monitor
```

### Resultado Esperado

```
╔════════════════════════════════════════════╗
║   TESTE 3: Comunicação com Backend        ║
╚════════════════════════════════════════════╝

[TESTE 3.1] Conectando WiFi...
✓ WiFi conectado!
  IP: 192.168.1.42

[TESTE 3.2] Login no backend...
  Backend: http://192.168.1.100:8080
  Team: IOT
  URL: http://192.168.1.100:8080/auth/login
  Payload: {"team":"IOT","secret":"iot-secret"}
  HTTP Code: 200
  Response: {"token":"eyJhbGciOiJIUzI1NiJ9...","team":"IOT"}
✓ Login bem-sucedido!
  Token: eyJhbGciOiJIUzI1NiJ9.eyJzdW...

[TESTE 3.3] Enviando métrica de teste...
  URL: http://192.168.1.100:8080/otel/v1/metrics
  Body: {"teamTag":"IOT","timestamp":"2025-11-22T18:30:00Z","payloadJson":"{...}"}
  HTTP Code: 201
  Response: {"id":123,"teamTag":"IOT",...}
✓ Métrica enviada com sucesso!

════════════════════════════════════════════
Teste 3 concluído!
════════════════════════════════════════════
```

### Critérios de Aprovação
- ✅ Login retorna HTTP 200 com token JWT
- ✅ Token JWT válido (não vazio, formato correto)
- ✅ Envio métrica retorna HTTP 201 Created
- ✅ Response contém ID da métrica salva
- ✅ Métrica aparece no banco de dados Oracle/H2

### Troubleshooting

**Erro: "Failed to connect"**
```
Causas:
1. Backend não está rodando
2. Firewall bloqueando porta 8080
3. IP incorreto no código

Solução:
curl http://SEU_IP:8080/actuator/health
```

**Erro: HTTP 403 Forbidden**
```
Causas:
1. Team IOT não cadastrado
2. Secret incorreto

Solução:
POST http://localhost:8080/auth/register
Body: {"team":"IOT","secret":"iot-secret"}
```

**Erro: HTTP 401 Unauthorized**
```
Causas:
1. Token JWT expirado
2. Token malformado

Solução:
- Token renova automaticamente a cada 1 hora
- Aguarde próximo login
```

---

## 🧪 Teste 4: Sistema Completo (End-to-End)

### Objetivo
Validar sistema integrado com leitura de sensores + envio ao backend + visualização no dashboard.

### Pré-requisitos
- Backend Java rodando (porta 8080)
- Dashboard Streamlit rodando (porta 8501)
- ESP32 conectado e programado
- Sensores conectados (ou simulados no Wokwi)

### Arquitetura do Teste

```
ESP32 (Sensores)
    ↓ HTTP/JSON (30s)
Backend Java (OTLP Server)
    ↓ SQL INSERT
OracleDB / H2
    ↓ REST API
Dashboard Streamlit
    ↓ Browser (auto-refresh 5s)
Usuário visualiza métricas
```

### Executar Teste Completo

**1. Iniciar Backend:**
```powershell
docker-compose up -d backend
```

**2. Iniciar Dashboard:**
```powershell
docker-compose up -d dashboard
```

**3. Upload ESP32:**
```powershell
# Ajustar IP em esp32_sensor_monitor.ino linha 24
# Ajustar LOCATION se necessário (linha 29)

pio run --target upload
pio device monitor
```

**4. Abrir Dashboard:**
```
http://localhost:8501
```

### Fluxo de Validação

**✅ Fase 1: ESP32 Inicializa (0-10s)**
```
[Serial Monitor]
✓ Sensores inicializados
✓ WiFi conectado (IP: 192.168.1.42)
✓ NTP configurado (GMT-3)
✓ Autenticação bem-sucedida
Sistema pronto! Iniciando monitoramento...
```

**✅ Fase 2: Primeira Leitura (10-40s)**
```
[Serial Monitor]
┌─────────────────────────────────────┐
│  Leitura de Sensores                │
└─────────────────────────────────────┘
🌡️  Temperatura: 23.5°C
💧 Umidade: 55.2%
☁️  Qualidade Ar: 800 ppm
💡 Luminosidade: 500 lux

  ✓ temperature = 23.5 enviado
  ✓ humidity = 55.2 enviado
  ✓ air_quality_ppm = 800.0 enviado
  ✓ luminosity_lux = 500.0 enviado

✓ Leitura concluída com sucesso
```

**✅ Fase 3: Backend Recebe (verificar logs)**
```powershell
docker logs humainze-backend

# Esperado:
2025-11-22 18:30:00 INFO  [http-nio-8080-exec-1] c.h.c.OtelController - Receiving metric
2025-11-22 18:30:00 INFO  [http-nio-8080-exec-1] c.h.s.OtelService - Saving metric: temperature = 23.5
2025-11-22 18:30:01 INFO  [http-nio-8080-exec-2] c.h.s.OtelService - Saving metric: humidity = 55.2
```

**✅ Fase 4: Dashboard Visualiza (40-50s)**
```
1. Acessar http://localhost:8501
2. Clicar aba "📊 Métricas IoT"
3. Selecionar filtros:
   - Team: IOT
   - Location: sala-1
   - Período: Última 1 hora
4. Verificar gráficos:
   - 🌡️ Temperatura (linha do tempo)
   - 💧 Umidade (linha do tempo)
   - ☁️ Qualidade Ar (bar chart)
   - 💡 Luminosidade (gauge)
5. Verificar última atualização: "Última atualização: 18:30:00"
```

**✅ Fase 5: Alertas (se métricas fora do ideal)**
```
[Serial Monitor]
⚠️  ALERTA: Temperatura alta!

[Dashboard - Aba "🚨 Alertas"]
┌───────────────────────────────────────┐
│ 🔴 Temperatura Alta                   │
│ Valor: 29.5°C (limite: 28°C)          │
│ Local: sala-1                         │
│ Timestamp: 2025-11-22 18:31:00        │
└───────────────────────────────────────┘
```

### Resultado Esperado Completo

**Console ESP32:**
- Leitura a cada 30 segundos
- 4 métricas enviadas por ciclo
- 0 erros de envio HTTP

**Backend Logs:**
- 4 métricas recebidas por ciclo (POST /otel/v1/metrics)
- HTTP 201 Created
- INSERT bem-sucedido no banco

**Dashboard:**
- Gráficos atualizando em tempo real
- Dados aparecem em até 35 segundos (30s leitura + 5s refresh)
- Sem erros de conexão

**Banco de Dados:**
```sql
-- Verificar métricas salvas
SELECT * FROM otel_metrics 
WHERE team_tag = 'IOT' 
ORDER BY timestamp DESC 
LIMIT 10;

-- Esperado: 10 linhas com métricas recentes
```

### Critérios de Aprovação Final

| Item | Esperado | Status |
|------|----------|--------|
| ESP32 conecta WiFi | < 10s | ⬜ |
| Login JWT sucesso | HTTP 200 | ⬜ |
| Sensores leem valores válidos | 4/4 sensores OK | ⬜ |
| Métricas enviadas | 4/4 por ciclo | ⬜ |
| Backend persiste | 100% no banco | ⬜ |
| Dashboard visualiza | < 35s latência | ⬜ |
| Alertas disparam | Se condições atendidas | ⬜ |
| Sistema estável | > 10 ciclos sem erro | ⬜ |

---

## 📊 Métricas de Performance

### Latências Esperadas

| Operação | Tempo | Aceitável |
|----------|-------|-----------|
| Conexão WiFi | 2-5s | < 10s |
| Login JWT | 100-500ms | < 2s |
| Leitura DHT22 | 250ms | < 1s |
| Leitura ADC (MQ135/LDR) | 10ms | < 100ms |
| POST métrica | 200-800ms | < 2s |
| Ciclo completo | 30-32s | < 35s |
| Dashboard refresh | 5s | 5s fixo |

### Consumo de Recursos

**ESP32:**
- CPU: ~20% (durante POST HTTP)
- RAM: ~40KB de 520KB
- WiFi: ~60mA médio

**Backend Java:**
- CPU: < 5% idle, ~30% durante POST
- RAM: ~512MB JVM heap
- Disco: ~10MB/dia (1440 métricas/dia × 7KB)

**Dashboard Streamlit:**
- CPU: < 10% idle, ~40% durante render
- RAM: ~150MB Python process
- Rede: ~5KB/s polling

---

## 🐛 Troubleshooting Geral

### ESP32 não conecta WiFi

**Sintomas:**
```
Conectando WiFi....................
✗ FALHOU: WiFi não conectou
```

**Causas e Soluções:**
1. **SSID/senha incorretos**: Verificar `WIFI_SSID` e `WIFI_PASSWORD`
2. **WiFi 5GHz**: ESP32 só suporta 2.4GHz - trocar rede
3. **Wokwi offline**: Usar `"Wokwi-GUEST"` com senha vazia
4. **Alcance fraco**: Aproximar ESP32 do roteador (RSSI > -70dBm)

### Backend não recebe métricas

**Sintomas:**
```
✗ Erro HTTP 0: Failed to connect
```

**Causas e Soluções:**
1. **Backend offline**: `docker-compose ps` ou `curl localhost:8080/actuator/health`
2. **IP incorreto**: Verificar `ipconfig` e ajustar `BACKEND_HOST`
3. **Firewall**: Abrir porta 8080 no Windows Defender
4. **Rede diferente**: ESP32 e backend na mesma subnet

### Token JWT inválido

**Sintomas:**
```
✗ HTTP 401: Unauthorized
```

**Causas e Soluções:**
1. **Token expirado**: Aguardar renovação automática (1h)
2. **Secret incorreto**: Verificar `TEAM_SECRET = "iot-secret"`
3. **Team não existe**: Registrar via `POST /auth/register`

### Dashboard não mostra dados

**Sintomas:**
- Gráficos vazios mesmo com métricas enviadas

**Causas e Soluções:**
1. **Filtros muito restritivos**: Aumentar período (ex: últimas 24h)
2. **Location diferente**: Verificar `LOCATION` no código ESP32 vs filtro dashboard
3. **Banco vazio**: Verificar `SELECT * FROM otel_metrics`
4. **Cache do Streamlit**: Forçar refresh com `Ctrl+R` no navegador

---

## 📹 Gravação de Vídeo (3 minutos)

Para atender requisito FIAP de vídeo demonstrativo:

### Roteiro Sugerido

**0:00 - 0:30 | Introdução (30s)**
- Apresentar equipe e tema "Futuro do Trabalho"
- Mostrar arquitetura: ESP32 → Backend Java → Dashboard

**0:30 - 1:00 | Hardware/Simulação (30s)**
- Wokwi: Mostrar diagram.json com sensores conectados
- Iniciar simulação
- Mostrar serial monitor com logs

**1:00 - 1:30 | Backend (30s)**
- Mostrar logs do backend recebendo métricas
- Consultar banco de dados (SQL SELECT)
- Mostrar API REST (/otel/v1/metrics)

**1:30 - 2:30 | Dashboard (60s)**
- Abrir dashboard Streamlit
- Mostrar gráficos de temperatura, umidade, CO2, luminosidade
- Interagir com filtros (período, location)
- Mostrar aba de alertas
- Demonstrar auto-refresh (aguardar nova métrica chegar)

**2:30 - 3:00 | Conclusão (30s)**
- Resumir benefícios: monitoramento em tempo real, alertas proativos
- Alinhamento NR-17 (conforto térmico, iluminação, qualidade do ar)
- Futuro do Trabalho: ambientes saudáveis = produtividade

### Ferramentas de Gravação

- **Tela:** OBS Studio, Camtasia, ou gravador do Windows (Win+G)
- **Narração:** Microfone ou áudio do sistema
- **Edição:** DaVinci Resolve (grátis), OpenShot, ou iMovie
- **Upload:** YouTube (não listado), Vimeo, ou Google Drive

---

## 📦 Entregáveis FIAP

### Checklist Final

- [ ] **Código Fonte** (GitHub)
  - [ ] `esp32_sensor_monitor.ino`
  - [ ] `diagram.json` (Wokwi)
  - [ ] `platformio.ini`
  - [ ] Testes (test_*.ino)
  - [ ] README.md

- [ ] **Documentação** (GitHub Pages)
  - [ ] INTEGRATION_GUIDE_IOT.md
  - [ ] DASHBOARD_GUIDE.md
  - [ ] GUIA_TESTES.md (este arquivo)

- [ ] **Vídeo** (YouTube)
  - [ ] 3 minutos demonstrando sistema funcionando
  - [ ] Link público ou não listado
  - [ ] Legenda com nomes e RMs

- [ ] **Arquivo de Entrega** (delivery.txt)
  - [ ] Nomes completos e RMs
  - [ ] Link GitHub
  - [ ] Link YouTube

### Formato delivery.txt

```
FIAP - Pós-Tech - Fase 4
Sistema de Monitoramento IoT para Futuro do Trabalho

Equipe:
- Barbara Bonome Filipus (RM560431)
- Vinicius Lira Ruggeri (RM560593)
- Yasmin Pereira da Silva (RM560039)

Turma: 2TDSPR

Links:
- Repositório GitHub: https://github.com/seu-usuario/humainze-dash
- GitHub Pages: https://seu-usuario.github.io/humainze-dash/
- Vídeo Demonstração: https://youtube.com/watch?v=...

Tema: O Futuro do Trabalho - Monitoramento Inteligente de Ambientes Corporativos

Tecnologias:
- IoT: ESP32 + DHT22 + MQ-135 + LDR
- Backend: Spring Boot 3.5.7 + Java 21 + OracleDB
- Dashboard: Streamlit + Plotly + Pandas
- Simulação: Wokwi + PlatformIO
```

---

## 🎓 Alinhamento com Requisitos FIAP

### Requisitos IoT (FIAP)

| Requisito | Implementação | Status |
|-----------|---------------|--------|
| ✅ Microcontrolador (Arduino/ESP32) | ESP32 DevKit v1 | OK |
| ✅ Sensores (≥2) | DHT22, MQ-135, LDR (3 sensores) | OK |
| ✅ Dashboard visualização | Streamlit + Plotly | OK |
| ✅ Gateway processamento | Backend Java (Spring Boot) | OK |
| ✅ Protocolo HTTP | POST /otel/v1/metrics | OK |
| ⚠️ Protocolo MQTT (opcional) | Não implementado (roadmap Phase 2) | Opcional |
| ✅ Documentação completa | README + guides + testes | OK |
| ✅ Vídeo demonstrativo (3 min) | Roteiro definido | Pendente |

### Alinhamento Tema "Futuro do Trabalho"

**Problema identificado:**
- Ambientes de trabalho com condições inadequadas (temperatura, umidade, CO2, luz)
- Impacto na produtividade, saúde e bem-estar

**Solução proposta:**
- Monitoramento contínuo em tempo real
- Alertas proativos antes de problemas graves
- Conformidade NR-17 (Ergonomia)
- Dashboard para tomada de decisão

**Benefícios:**
- 📈 Aumento de produtividade (ambiente ideal)
- 🏥 Redução de afastamentos (doenças respiratórias, fadiga)
- ⚖️ Compliance regulatório (NR-17)
- 📊 Dados para melhoria contínua

---

## 📧 Suporte

**Dúvidas ou problemas?**

1. Verificar este guia de testes
2. Consultar `IoT/README.md`
3. Verificar issues no GitHub
4. Contatar equipe via email institucional FIAP

---

**Última atualização:** 22/11/2025  
**Versão:** 1.0.0  
**Licença:** MIT
