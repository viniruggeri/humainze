# 📚 Índice de Documentação - Humainze Backend

## 📖 Guias Principais

### [📋 Sumário Executivo](EXECUTIVE_SUMMARY.md)
Visão geral do projeto, objetivos, stack tecnológico e arquitetura.

### [🤖 Guia de Integração - IA](INTEGRATION_GUIDE_IA.md)
Como integrar módulos de IA Python com o backend:
- Código Python para envio de dados
- APIs de predição e treinamento
- Detecção de drift
- Queries SigNoz

### [🔌 Guia de Integração - IoT](INTEGRATION_GUIDE_IOT.md)
Como conectar sensores e dispositivos IoT:
- Código Arduino/ESP32/C++
- Protocolo HTTP
- Formato de payloads
- Troubleshooting

### [📡 Endpoints OpenTelemetry](OTEL_INGESTION_ENDPOINTS.md)
Documentação dos endpoints OTLP:
- `/otel/v1/metrics`
- `/otel/v1/traces`
- `/otel/v1/logs`

### [📦 Exemplos de Payloads](PAYLOAD_EXAMPLES.md)
Payloads JSON prontos para usar:
- Métricas IoT
- Traces distribuídos
- Logs estruturados

### [📊 Visualização com SigNoz](SIGNOZ_VISUALIZATION.md)
Como usar SigNoz para observabilidade:
- Dashboard de métricas
- Tracing distribuído
- Queries customizadas

### [🚨 Sistema de Alertas](ALERTS_SYSTEM.md)
Documentação completa do sistema de alertas cognitivos:
- Tipos de alertas (DRIFT, MODEL_ERROR, SERVICE_DOWN)
- Dashboard Streamlit em tempo real
- Banner de notificações
- Paginação e filtros
- Auto-refresh com polling

### [🚀 Deploy Azure VM](DEPLOY_AZURE.md)
Guia completo de deploy em Azure Virtual Machine:
- Provisionar VM no Azure
- Instalar Docker e Docker Compose
- Configurar variáveis de ambiente
- Deploy com dois containers (Backend + Dashboard)
- Monitoramento e troubleshooting

### [📘 Configurar GitHub Pages](GITHUB_PAGES_SETUP.md)
Como habilitar e configurar GitHub Pages para esta documentação.

## 📋 Documentação por Categoria
- Umidade (DHT22)
- CO2 (MQ-135)
- Luminosidade (LDR)
- Movimento (PIR)
- Bateria, Pressão, Altitude
- Umidade do solo, Ruído

---

### 3. **PAYLOAD_EXAMPLES.md**
**Copy & Paste - Exemplos de Payload JSON**

Contém:
- ✅ 10+ exemplos de métricas IoT prontos para usar
- ✅ 14+ exemplos de métricas IA prontos para usar
- ✅ 7+ exemplos de alertas com GPT-4
- ✅ Comandos cURL completos
- ✅ Queries SQL para SigNoz
- ✅ Template genérico para qualquer métrica

**Use este documento quando:**
- Precisa enviar uma métrica rapidamente
- Quer um exemplo de payload específico
- Está debugando formato JSON

---

### 4. **SIGNOZ_VISUALIZATION.md**
**Como visualizar métricas no SigNoz**

Contém:
- ✅ Instalação do SigNoz com Docker Compose
- ✅ Configuração do backend para exportar OTEL
- ✅ Passo-a-passo: criar dashboard IoT
- ✅ Passo-a-passo: criar dashboard IA
- ✅ Configurar alertas (Slack, Email, PagerDuty)
- ✅ 5+ queries SQL recomendadas
- ✅ Troubleshooting

**Dashboards abordados:**
- IoT: Temperatura, Umidade, CO2, Luminosidade
- IA: Acurácia, Drift, Latência, Métricas de classificação
- Alertas: Configuração e integração com Slack/Email

---

### 5. **ZERO_TRUST_AUTH.md**
**Autenticação Zero Trust com API Key → JWT**

Contém:
- ✅ Visão geral da arquitetura
- ✅ Componentes (ApiKeyService, Filter, Controller)
- ✅ Fluxo de uso (2 opções)
- ✅ Matriz de permissões
- ✅ Testes HTTP

**Leia este quando:**
- Quer entender como funciona a autenticação
- Precisa debugar problemas de acesso
- Está integrando um novo cliente

---

## 🔐 Credenciais

### API Keys por Time

| Time | API Key | Endpoint | Role |
|------|---------|----------|------|
| IA | `chave-ia` | `/otel/v1/**`, `/alerts/**` | ROLE_IA |
| IoT | `chave-iot` | `/otel/v1/**` | ROLE_IOT |
| Admin | `chave-admin` | `/admin/**` | ROLE_ADMIN |

### Usar nos Headers

```bash
# Opção 1: API Key diretamente
curl -H "X-API-KEY: chave-ia" http://localhost:8080/otel/v1/metrics

# Opção 2: JWT
curl -H "Authorization: Bearer <token>" http://localhost:8080/otel/v1/metrics
```

---

## 📊 Fluxo Geral

```
[IA/IoT/Java]
       ↓
   X-API-KEY (ou JWT)
       ↓
[Humainze Backend - Java 21/Spring Boot 3]
       ↓
   POST /otel/v1/metrics
       ↓
[Banco de Dados - Oracle/H2]
   + [OTEL Exporter - HTTP/OTLP]
       ↓
   ┌───────────────┬───────────────┐
   ↓               ↓               ↓
[SigNoz]      [Get /export]   [Alertas]
[Dashboard]   [JSON Response] [Email/Slack]
```

---

## 🚀 Quick Start

### Apenas 3 Passos para Começar

#### 1. Autenticar e Obter JWT
```bash
curl -X POST http://localhost:8080/auth/token \
  -H "X-API-KEY: chave-ia"
```

#### 2. Enviar Primeira Métrica
```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "X-API-KEY: chave-ia" \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag": "IA",
    "timestamp": "2025-11-20T15:00:00Z",
    "payloadJson": "{\"metric\":\"model_accuracy\",\"value\":0.95}"
  }'
```

#### 3. Visualizar no SigNoz
```
http://localhost:3301/dashboard
```

---

## 📂 Estrutura de Diretórios

```
humainze-dash/
├── docs/
│   ├── INTEGRATION_GUIDE_IA.md        ← Team IA lê isso
│   ├── INTEGRATION_GUIDE_IOT.md       ← Team IoT lê isso
│   ├── PAYLOAD_EXAMPLES.md            ← Exemplos prontos
│   ├── SIGNOZ_VISUALIZATION.md        ← Dashboard
│   ├── INDEX.md                       ← Você está aqui
│   └── README.md                      ← Visão geral do projeto
├── http-tests/
│   ├── integration-tests.http         ← Suite de testes HTTP
│   ├── zero-trust-tests.http          ← Testes de auth
│   └── quick-tests.http               ← Testes rápidos
├── src/
│   ├── main/java/com/backend/humainzedash/
│   │   ├── controller/              ← REST controllers
│   │   ├── service/                 ← Lógica de negócio
│   │   ├── domain/entity/           ← Entidades JPA
│   │   ├── repository/              ← Repositórios
│   │   ├── security/                ← Auth & JWT
│   │   ├── config/                  ← Configurações
│   │   └── HumainzeDashApplication.java
│   └── resources/
│       ├── application.yml
│       ├── application-dev.yml      ← Dev com H2
│       └── application-prod.yml     ← Prod com Oracle
└── pom.xml
```

---

## 🔧 Configuração Rápida

### Dev (H2 em Memória)

```bash
mvn clean install
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=dev"
```

### Prod (Oracle Remoto)

```bash
export DB_URL=jdbc:oracle:thin:@seu-oracle:1521:xe
export DB_USER=seu_usuario
export DB_PASSWORD=sua_senha
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=prod"
```

### Docker

```bash
docker build -t humainze-backend .
docker run -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e DB_URL=jdbc:oracle:thin:@oracle:1521:xe \
  humainze-backend
```

---

## 🧪 Testes Disponíveis

### Suite de Testes HTTP

Arquivo: `http-tests/integration-tests.http`

Contém:
- ✅ Testes de autenticação
- ✅ Envio de métricas IoT (10+ exemplos)
- ✅ Envio de métricas IA (14+ exemplos)
- ✅ Envio de alertas (7+ exemplos)
- ✅ Listagem e filtros
- ✅ Batch de testes

**Como usar no IntelliJ:**
1. Abra `http-tests/integration-tests.http`
2. Clique no play verde antes de cada request
3. Veja a resposta no painel direito

---

## 🚨 Alertas Suportados

### Tipos de Alerta

- `DRIFT` - Detecção de data drift no modelo
- `MODEL_ERROR` - Erro em predição
- `SERVICE_DOWN` - Serviço offline
- `CUSTOM` - Alerta customizado com GPT-4

### Exemplo de Alerta Inteligente com GPT-4

```python
# Team IA envia para o backend
POST /alerts
{
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Drift detectado no modelo v2.1 - mensagem gerada por GPT-4"
}
```

**O que o backend faz:**
1. Salva o alerta no banco
2. Envia email para o time
3. Dispara webhook para Slack (se configurado)
4. Retorna o alerta com ID

---

## 📞 Suporte & Links

### Documentação Externa

- [Spring Boot 3 Docs](https://spring.io/projects/spring-boot)
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
- [SigNoz Docs](https://signoz.io/docs/)
- [ArduinoJson](https://arduinojson.org/)
- [Requests Python](https://docs.python-requests.org/)

### Repositórios

- Backend: https://github.com/humanize/humainze-dash
- IA Service: https://github.com/humanize/humainze-ia
- IoT Firmware: https://github.com/humanize/humainze-iot

### Contatos

- Backend Team: backend-team@humainze.ai
- DevOps: devops@humainze.ai
- Support: support@humainze.ai

---

## 🎓 Exemplo Completo: De Zero ao Dashboard

### Cenário: Team IoT quer enviar temperatura

**Passo 1: Ler documentação**
```
Abrir: INTEGRATION_GUIDE_IOT.md → Seção "Enviar Métricas de Sensores"
```

**Passo 2: Copiar código Python**
```python
# De INTEGRATION_GUIDE_IOT.md
import requests
import json
from datetime import datetime, timezone

client = HumainzeIoTClient("chave-iot", "http://localhost:8080")
client.send_metric("temperature", 25.5, {"sensor": "DHT22", "location": "sala-1"})
```

**Passo 3: Testar com cURL**
```bash
# De PAYLOAD_EXAMPLES.md → Seção "Temperatura (DHT22)"
curl -X POST http://localhost:8080/otel/v1/metrics ...
```

**Passo 4: Visualizar no SigNoz**
```
Seguir: SIGNOZ_VISUALIZATION.md → "Criar Dashboard para IoT"
```

**Resultado:**
- ✅ Dados sendo enviados
- ✅ Armazenados no banco
- ✅ Visíveis no SigNoz em tempo real
- ✅ Dashboard criado e funcionando

---

## ✅ Checklist de Integração

- [ ] Li o guia apropriado (IA ou IoT)
- [ ] Copiei a API Key correta
- [ ] Enviei primeira métrica com sucesso (HTTP 200/201)
- [ ] Métrica aparece em `/export/metrics`
- [ ] SigNoz está rodando
- [ ] Dashboard criado
- [ ] Widgets adicionados
- [ ] Alertas configurados
- [ ] Team notificado

---

## 🎯 Próximos Passos

1. **Integração Básica**: Começar com um sensor/métrica
2. **Batching**: Enviar múltiplas métricas em paralelo
3. **Alertas**: Implementar alertas com GPT-4
4. **Dashboard**: Criar dashboard customizado
5. **Auto-retrain**: Disparar retrain automaticamente via alertas
6. **Escalabilidade**: Configurar para produção (Oracle, SigNoz remoto)

---

## 📝 Notas Finais

- **HTTP Only**: Nenhum gRPC, tudo é HTTP/REST
- **Zero Trust**: Sem autenticação = sem acesso
- **Stateless**: JWT/API Key são suficientes
- **Escalável**: Pronto para múltiplos times e sensores
- **Observable**: Tudo rastreável via SigNoz

**Bom trabalho! 🚀**

---

Documento atualizado em: 2025-11-20
Versão: 1.0

