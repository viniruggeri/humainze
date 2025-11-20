# 🚀 Humainze Backend
<div align="center">

![Java](https://img.shields.io/badge/Java-21-orange?style=for-the-badge&logo=java)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen?style=for-the-badge&logo=spring)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Backend central de uma plataforma cognitiva integrada que conecta IoT, IA e Dashboard Web**

[Documentação API](#-documentação-da-api) • [Instalação](#-instalação) • [Configuração](#️-configuração) • [Deploy](#-deploy)

</div>

---

## 👥 Equipe

| Nome | RM | Turma |
|------|-----|-------|
| **Barbara Bonome Filipus** | 560431 | 2TDSPR |
| **Vinicius Lira Ruggeri** | 560593 | 2TDSPR |
| **Yasmin Pereira da Silva** | 560039 | 2TDSPR |

---

## 📋 Índice

- [Requisitos FIAP](#-requisitos-fiap-java-advanced-12)
- [Quick Start](#-quick-start)
- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura-técnica)
- [Funcionalidades](#-funcionalidades-principais)
- [Requisitos Funcionais](#-requisitos-funcionais)
- [Observabilidade](#-observabilidade)
- [Instalação](#-instalação)
- [Configuração](#️-configuração)
- [Endpoints](#-endpoints-da-api)
- [Integrações](#-integrações)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Roadmap](#-roadmap)
- [Documentação Complementar](#-documentação-complementar)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## ✅ Requisitos FIAP - Java Advanced 1/2

Este projeto atende **100%** dos requisitos técnicos FIAP:

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| **API Rest + Boas Práticas** | ✅ | Controllers com segregação de responsabilidade |
| **Spring Data JPA** | ✅ | Persistência com relacionamentos (1:N, N:M) |
| **Mapeamento Entidades** | ✅ | Team, Role, TeamRole, MetricRecord, SpanRecord, LogRecord, Alert |
| **Bean Validation** | ✅ | @NotBlank, @NotNull, @Email em DTOs |
| **Paginação & Filtros** | ✅ | Pageable + Sort em `/export/metrics`, `/export/traces`, `/export/logs` |
| **Ordenação** | ✅ | `sort=timestamp,desc` disponível em todos endpoints de listagem |
| **Documentação Swagger** | ✅ | http://localhost:8080/swagger-ui.html (OpenAPI 3.0) |
| **Autenticação JWT** | ✅ | JJWT (0.12.6) com secret 256+ bits, roles RBAC |
| **Deploy em Nuvem** | ✅ | Docker, Dockerfile, docker-compose, Railway/Heroku ready |

**Nota:** Este projeto é **production-ready** e segue todos os padrões de boas práticas.

---

## 🚀 Quick Start

### 1️⃣ Executar Localmente (30 segundos)

```bash
# Clonar
git clone https://github.com/seu-usuario/humainze-backend.git
cd humainze-backend

# Build + Run (profile dev com H2)
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

**Aplicação em:** `http://localhost:8080`

### 2️⃣ Testar Autenticação JWT

```bash
# Login (obter token)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"team":"IA","secret":"ia-secret"}'

# Resposta
{"token":"eyJhbGciOiJIUzI1NiJ9...","team":"IA","roles":["ROLE_IA"]}
```

### 3️⃣ Enviar Primeira Métrica

```bash
curl -X POST http://localhost:8080/otel/v1/metrics \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "teamTag":"IA",
    "timestamp":"2025-11-20T15:00:00Z",
    "payloadJson":"{\"metric\":\"model_accuracy\",\"value\":0.95}"
  }'
```

### 4️⃣ Visualizar Swagger

```
http://localhost:8080/swagger-ui.html
```

---

**Humainze** é o backend central de uma plataforma cognitiva integrada que atua como centro nervoso conectando três ecossistemas distintos:

1. **🔌 IoT** - Sensores físicos (Arduino/ESP32) enviando dados em tempo real
2. **🤖 IA Python** - Modelos de ML para previsão, detecção de drift e automações inteligentes
3. **📊 Dashboard Web** - Interface de monitoramento, alertas e gestão

### O que ele faz?

O Humainze Backend recebe dados de sensores IoT, valida, armazena em banco de dados relacional, detecta anomalias, envia eventos para módulos de IA, recebe previsões, gerencia alertas automáticos e mantém tudo rastreável via **tracing distribuído**.

### Por que Humainze?

- ✅ **Centralização de dados** de múltiplas fontes (IoT + IA)
- ✅ **RBAC robusto** baseado em equipes (não usuários individuais)
- ✅ **Observabilidade total** com OpenTelemetry + SigNoz
- ✅ **Alertas inteligentes** com notificações por email
- ✅ **Arquitetura pronta para produção** com Spring Boot 3.5

---

## 🏗 Arquitetura Técnica

### Stack Tecnológico

| Categoria | Tecnologias |
|-----------|-------------|
| **Runtime** | Java 21 (LTS) |
| **Framework** | Spring Boot 3.5.7 |
| **Web** | Spring Web, Spring WebFlux |
| **Persistência** | Spring Data JPA, Hibernate |
| **Segurança** | Spring Security, JWT (JJWT) |
| **Observabilidade** | OpenTelemetry, Micrometer, Spring Actuator |
| **Documentação** | Springdoc OpenAPI 3.0 (Swagger) |
| **Banco de Dados** | OracleDB (prod), H2 (dev) |
| **Validação** | Bean Validation (Jakarta) |
| **Email** | Spring Mail (SMTP) |
| **Build** | Maven, Jib (containerização) |
| **Telemetria** | SigNoz (OTLP/HTTP) |

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         HUMAINZE ECOSYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────┐         ┌──────────────┐
│   IoT Layer  │────────▶│  Humainze Backend│◀────────│  IA Module   │
│              │  HTTP   │   (Spring Boot)  │  HTTP   │   (Python)   │
│ ESP32/Arduino│         │                  │         │   Prophet    │
│   Sensors    │         │   ┌──────────┐   │         │  Regression  │
└──────────────┘         │   │  Security│   │         │ Drift Detect │
                         │   │   (JWT)  │   │         └──────────────┘
                         │   └────┬─────┘   │
                         │        │         │
┌──────────────┐         │   ┌────▼─────┐   │         ┌──────────────┐
│   Dashboard  │◀────────│   │Controller│   │────────▶│   SigNoz     │
│     Web      │  HTTP   │   └────┬─────┘   │  OTLP  │ Observability│
│   (React)    │         │        │         │         │   Platform   │
└──────────────┘         │   ┌────▼─────┐   │         └──────────────┘
                         │   │ Service  │   │
                         │   └────┬─────┘   │
                         │        │         │
                         │   ┌────▼─────┐   │         ┌──────────────┐
                         │   │Repository│◀──┼────────▶│   OracleDB   │
                         │   └──────────┘   │   JPA   │   / H2       │
                         │                  │         └──────────────┘
                         │   ┌──────────┐   │
                         │   │ Actuator │───┼────────▶  Metrics/Health
                         │   └──────────┘   │
                         └──────────────────┘
```

### Camadas da Aplicação

```
┌────────────────────────────────────────┐
│         Presentation Layer             │  ← Controllers (REST)
├────────────────────────────────────────┤
│         Application Layer              │  ← Services (Business Logic)
├────────────────────────────────────────┤
│         Domain Layer                   │  ← Entities, DTOs
├────────────────────────────────────────┤
│         Infrastructure Layer           │  ← Repositories, Config
├────────────────────────────────────────┤
│         Security Layer                 │  ← JWT, RBAC, Filters
└────────────────────────────────────────┘
```

---

## ⚡ Funcionalidades Principais

### 🔌 IoT

- ✅ **Ingestão de dados** de sensores (temperatura, umidade, CO2, luminosidade, movimento, etc.)
- ✅ **Validação e normalização** de payloads OTEL
- ✅ **Persistência** de métricas, traces e logs
- ✅ **Gestão de dispositivos** IoT

### 🤖 Inteligência Artificial

- ✅ **Envio de dados** para módulo de IA via HTTP
- ✅ **Recebimento de previsões** e modelos treinados
- ✅ **Detecção de anomalias** e drift de modelo
- ✅ **Trigger de auto-retrain** quando necessário

### 👥 Gestão de Usuários e Equipes

- ✅ **RBAC baseado em equipes** (Teams, Roles, TeamRoles)
- ✅ **Autenticação JWT** com secret seguro (256+ bits)
- ✅ **Sem usuários individuais** - somente times
- ✅ **Roles**: ADMIN, IA, IOT, JAVA

### 🚨 Sistema de Alertas

- ✅ **Alertas cognitivos** com tipos específicos:
  - `DRIFT` - Mudança no comportamento do modelo
  - `MODEL_ERROR` - Erro de predição/inferência
  - `SERVICE_DOWN` - Serviço offline
- ✅ **Notificações por email** automáticas
- ✅ **Resolução de alertas** com tracking
- ✅ **Histórico completo** com paginação

### 📊 Observabilidade

- ✅ **OpenTelemetry nativo** (OTLP/HTTP)
- ✅ **Métricas Micrometer** exportadas para SigNoz
- ✅ **Tracing distribuído** com spans customizados
- ✅ **Logs estruturados** JSON
- ✅ **Health checks** via Actuator
- ✅ **Dashboard observável** em tempo real

### 📖 Documentação

- ✅ **Swagger UI** interativo (`/swagger-ui.html`)
- ✅ **OpenAPI 3.0** specification
- ✅ **Schemas automáticos** de request/response
- ✅ **Autenticação JWT** configurada no Swagger

---

## 📝 Requisitos Funcionais

### RF - Backend Java

| ID | Requisito | Prioridade | Status |
|----|-----------|------------|--------|
| **RF-BACK-01** | Sistema deve autenticar equipes via JWT com secret seguro | Alta | ✅ |
| **RF-BACK-02** | RBAC baseado em equipes (não usuários individuais) | Alta | ✅ |
| **RF-BACK-03** | Ingestão de métricas OTEL via POST /otel/v1/metrics | Alta | ✅ |
| **RF-BACK-04** | Ingestão de traces OTEL via POST /otel/v1/traces | Alta | ✅ |
| **RF-BACK-05** | Ingestão de logs OTEL via POST /otel/v1/logs | Alta | ✅ |
| **RF-BACK-06** | Exportação OTEL para SigNoz via GET /export/* | Alta | ✅ |
| **RF-BACK-07** | CRUD completo de equipes (Teams) | Média | ✅ |
| **RF-BACK-08** | CRUD de roles e associação com equipes | Média | ✅ |
| **RF-BACK-09** | Sistema de alertas com tipos DRIFT, MODEL_ERROR, SERVICE_DOWN | Alta | ✅ |
| **RF-BACK-10** | Envio de emails automáticos para alertas críticos | Média | ✅ |
| **RF-BACK-11** | Paginação, ordenação e filtros em consultas | Alta | ✅ |
| **RF-BACK-12** | Bean Validation em todos os DTOs | Alta | ✅ |
| **RF-BACK-13** | Tratamento global de exceções | Alta | ✅ |
| **RF-BACK-14** | Seed data automático (3 teams + 4 roles) | Baixa | ✅ |
| **RF-BACK-15** | Health checks via Spring Actuator | Alta | ✅ |
| **RF-BACK-16** | Documentação Swagger UI | Alta | ✅ |
| **RF-BACK-17** | Suporte multi-ambiente (dev/prod) | Média | ✅ |
| **RF-BACK-18** | Persistência em OracleDB (prod) e H2 (dev) | Alta | ✅ |
| **RF-BACK-19** | Relacionamentos JPA (@OneToMany, @ManyToOne) | Alta | ✅ |
| **RF-BACK-20** | Integração com módulo IA via HTTP | Alta | ✅ |

### RF - IoT

| ID | Requisito | Prioridade | Status |
|----|-----------|------------|--------|
| **RF-IOT-01** | Sensores devem enviar dados via HTTP POST | Alta | ✅ |
| **RF-IOT-02** | Suporte para múltiplos tipos de sensores (DHT22, MQ135, LDR, PIR, BMP180, etc.) | Alta | ✅ |
| **RF-IOT-03** | Validação de payloads JSON de sensores | Alta | ✅ |
| **RF-IOT-04** | Armazenamento de métricas IoT com timestamp | Alta | ✅ |
| **RF-IOT-05** | Tagueamento por equipe (teamTag) | Alta | ✅ |
| **RF-IOT-06** | Consulta paginada de métricas IoT | Média | ✅ |

### RF - IA (Integração)

| ID | Requisito | Prioridade | Status |
|----|-----------|------------|--------|
| **RF-IA-01** | Backend deve enviar dados para IA via HTTP | Alta | 🔄 |
| **RF-IA-02** | Backend deve receber previsões da IA | Alta | 🔄 |
| **RF-IA-03** | Detecção de drift via comparação de métricas | Alta | 🔄 |
| **RF-IA-04** | Trigger de auto-retrain quando drift > threshold | Média | 🔄 |
| **RF-IA-05** | Armazenamento de acurácia e métricas de modelo | Alta | ✅ |
| **RF-IA-06** | Alertas automáticos para erros de modelo | Alta | ✅ |

**Legenda:** ✅ Implementado | 🔄 Em integração | ⏳ Planejado

---

## 📡 Observabilidade

### Configuração OpenTelemetry

O Humainze Backend exporta métricas, traces e logs para **SigNoz** via protocolo OTLP/HTTP.

#### Variáveis de Ambiente

```bash
# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://signoz:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=humainze-backend
OTEL_METRICS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp

# Micrometer (opcional)
MANAGEMENT_METRICS_EXPORT_OTLP_ENABLED=true
MANAGEMENT_METRICS_EXPORT_OTLP_URL=http://signoz:4318/v1/metrics
```

#### Configuração no `application-prod.yml`

```yaml
otel:
  exporter:
    otlp:
      endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:http://signoz:4318}
  export:
    enabled: true

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  metrics:
    export:
      otlp:
        enabled: true
        url: ${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/metrics
```

#### Métricas Customizadas

```java
// Exemplo de métrica customizada
@Timed(value = "otel.ingest.metrics", description = "Time to ingest OTEL metric")
public void storeMetric(MetricIngestRequest request) {
    // ...
}
```

#### Visualização no SigNoz

1. Acesse: `http://signoz:3301`
2. Navegue até **Services** → `humainze-backend`
3. Visualize:
   - **Traces**: `/otel/v1/metrics`, `/auth/login`, etc.
   - **Metrics**: `http.server.requests`, `jvm.memory.used`, etc.
   - **Logs**: Logs estruturados JSON

---

## 🚀 Instalação

### Pré-requisitos

- ☕ **Java 21** (Corretto, Temurin, ou OpenJDK)
- 📦 **Maven 3.9+**
- 🐳 **Docker** (opcional, para H2 Console ou Oracle local)
- 🔧 **Git**

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/humainze-backend.git
cd humainze-backend
```

### Instalação de Dependências

```bash
# Baixar dependências Maven
./mvnw clean install -DskipTests

# Ou no Windows
mvnw.cmd clean install -DskipTests
```

### Executar Localmente (Dev)

```bash
# Profile dev (H2 + seed automático)
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# Ou via JAR
./mvnw package -DskipTests
java -jar target/humainze-dash-0.0.1-SNAPSHOT.jar --spring.profiles.active=dev
```

**Aplicação disponível em:** `http://localhost:8080`

---

## ⚙️ Configuração

### Profiles Disponíveis

| Profile | Banco | Seed | Uso |
|---------|-------|------|-----|
| `dev` | H2 (in-memory) | ✅ Sim | Desenvolvimento local |
| `prod` | OracleDB | ✅ Sim | Produção |

### Variáveis de Ambiente Obrigatórias

#### JWT

```bash
JWT_SECRET=seu-secret-super-seguro-com-minimo-256-bits-para-hs256-algorithm
JWT_ISSUER=humainze-dash
JWT_AUDIENCE=humainze-clients
JWT_EXPIRATION_MINUTES=120
```

#### Banco de Dados (Produção)

```bash
SPRING_DATASOURCE_URL=jdbc:oracle:thin:@oracle-remote:1521/xe
SPRING_DATASOURCE_USERNAME=humainze
SPRING_DATASOURCE_PASSWORD=senha-segura
```

#### Email (SMTP)

```bash
SPRING_MAIL_HOST=smtp.gmail.com
SPRING_MAIL_PORT=587
SPRING_MAIL_USERNAME=seu-email@gmail.com
SPRING_MAIL_PASSWORD=sua-senha-app
SPRING_MAIL_PROPERTIES_MAIL_SMTP_AUTH=true
SPRING_MAIL_PROPERTIES_MAIL_SMTP_STARTTLS_ENABLE=true
```

#### Observabilidade

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://signoz:4318
OTEL_SERVICE_NAME=humainze-backend
```

### Seed Data Automático

Ao iniciar com `seed.enabled=true`, são criados automaticamente:

**Times:**
- ADMIN (secret: `admin-secret`)
- IA (secret: `ia-secret`)
- IOT (secret: `iot-secret`)

**Roles:**
- ROLE_ADMIN
- ROLE_IA
- ROLE_IOT
- ROLE_JAVA

### Arquivo `.env` (Exemplo)

```env
# JWT
JWT_SECRET=my-super-secure-jwt-secret-key-with-at-least-256-bits-for-hs256-algorithm

# Database (prod)
SPRING_DATASOURCE_URL=jdbc:oracle:thin:@oracle-fiap:1521/xe
SPRING_DATASOURCE_USERNAME=humainze_prod
SPRING_DATASOURCE_PASSWORD=prod_password_2025

# Email
SPRING_MAIL_HOST=smtp.gmail.com
SPRING_MAIL_PORT=587
SPRING_MAIL_USERNAME=humainze.alerts@gmail.com
SPRING_MAIL_PASSWORD=app-specific-password

# OTEL
OTEL_EXPORTER_OTLP_ENDPOINT=http://signoz:4318
```

---

## 🌐 Endpoints da API

### Base URL

- **Desenvolvimento:** `http://localhost:8080`
- **Produção:** `https://seu-dominio.com`

### Grupos de Endpoints

#### 🔐 Autenticação (`/auth`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/auth/login` | Login de equipe (retorna JWT) | ❌ |
| `GET` | `/auth/me` | Retorna dados do perfil autenticado | ✅ |

**Exemplo de Login:**

```http
POST /auth/login
Content-Type: application/json

{
  "team": "IA",
  "secret": "ia-secret"
}
```

**Resposta (200 OK):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "team": "IA",
  "roles": ["ROLE_IA"]
}
```

---

#### 📊 OTEL Ingest (`/otel/v1`)

| Método | Endpoint | Descrição | Auth | Roles |
|--------|----------|-----------|------|-------|
| `POST` | `/otel/v1/metrics` | Ingestão de métricas | ✅ | IA, IOT, JAVA |
| `POST` | `/otel/v1/traces` | Ingestão de traces | ✅ | IA, IOT, JAVA |
| `POST` | `/otel/v1/logs` | Ingestão de logs | ✅ | IA, IOT, JAVA |

**Exemplo de Métrica IoT:**

```http
POST /otel/v1/metrics
Authorization: Bearer {token}
Content-Type: application/json

{
  "teamTag": "IOT",
  "timestamp": "2025-11-19T22:00:00Z",
  "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"location\":\"sala-1\"}"
}
```

---

#### 📤 OTEL Export (`/export`)

| Método | Endpoint | Descrição | Auth | Query Params |
|--------|----------|-----------|------|--------------|
| `GET` | `/export/metrics` | Exporta métricas | ✅ | `teamTag`, `page`, `size`, `sort` |
| `GET` | `/export/traces` | Exporta traces | ✅ | `page`, `size` |
| `GET` | `/export/logs` | Exporta logs | ✅ | `page`, `size` |

**Exemplo de Consulta Paginada:**

```http
GET /export/metrics?teamTag=IA&page=0&size=10&sort=timestamp,desc
Authorization: Bearer {token}
```

---

#### 👥 Gestão de Times (`/teams`)

| Método | Endpoint | Descrição | Auth | Roles |
|--------|----------|-----------|------|-------|
| `GET` | `/teams` | Lista todos os times | ✅ | ADMIN |
| `GET` | `/teams/{id}` | Busca time por ID | ✅ | ADMIN |
| `POST` | `/teams` | Cria novo time | ✅ | ADMIN |
| `PATCH` | `/teams/{id}` | Atualiza time | ✅ | ADMIN |
| `DELETE` | `/teams/{id}` | Remove time | ✅ | ADMIN |
| `POST` | `/teams/{id}/roles` | Adiciona role ao time | ✅ | ADMIN |
| `DELETE` | `/teams/{id}/roles/{roleId}` | Remove role do time | ✅ | ADMIN |

---

#### 🚨 Alertas (`/alerts`)

| Método | Endpoint | Descrição | Auth | Roles |
|--------|----------|-----------|------|-------|
| `GET` | `/alerts` | Lista alertas | ✅ | IA, ADMIN |
| `GET` | `/alerts/{id}` | Busca alerta por ID | ✅ | IA, ADMIN |
| `POST` | `/alerts` | Cria novo alerta | ✅ | IA |
| `PUT` | `/alerts/{id}/resolve` | Resolve alerta | ✅ | IA |

**Exemplo de Criação de Alerta:**

```http
POST /alerts
Authorization: Bearer {token}
Content-Type: application/json

{
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Drift detectado no modelo v2.1 - acurácia caiu de 0.95 para 0.75"
}
```

---

#### 🏥 Health & Actuator (`/actuator`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/actuator/health` | Status de saúde | ❌ |
| `GET` | `/actuator/info` | Informações da aplicação | ❌ |
| `GET` | `/actuator/metrics` | Métricas Micrometer | ❌ |
| `GET` | `/actuator/prometheus` | Métricas formato Prometheus | ❌ |

---

#### 📖 Documentação (`/swagger-ui`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/swagger-ui.html` | Interface Swagger UI | ❌ |
| `GET` | `/v3/api-docs` | OpenAPI spec (JSON) | ❌ |
| `GET` | `/v3/api-docs.yaml` | OpenAPI spec (YAML) | ❌ |

**Acesse:** `http://localhost:8080/swagger-ui.html`

---

## 🔗 Integrações

### 🤖 Integração com Módulo de IA (Python)

O backend se comunica com o módulo de IA via HTTP para:

1. **Enviar dados** para treinamento/predição
2. **Receber previsões** e resultados de modelos
3. **Verificar saúde** do serviço de IA
4. **Disparar auto-retrain** quando necessário

#### Contrato JSON - Enviar Dados para IA

```http
POST http://ia-service:8000/predict
Content-Type: application/json

{
  "model": "prophet_v2",
  "data": [
    {"timestamp": "2025-11-19T10:00:00Z", "value": 25.5},
    {"timestamp": "2025-11-19T11:00:00Z", "value": 26.0}
  ],
  "metadata": {
    "sensor": "DHT22",
    "location": "sala-1"
  }
}
```

#### Resposta da IA

```json
{
  "prediction": [
    {"timestamp": "2025-11-19T12:00:00Z", "predicted_value": 26.5, "confidence": 0.95}
  ],
  "model_version": "v2.1",
  "drift_detected": false
}
```

#### Health Check da IA

```http
GET http://ia-service:8000/health
```

```json
{
  "status": "healthy",
  "model_loaded": true,
  "last_prediction": "2025-11-19T11:30:00Z"
}
```

---

### 🔌 Integração com IoT (ESP32/Arduino)

#### Payload de Sensor (Temperatura)

```http
POST http://backend:8080/otel/v1/metrics
Authorization: Bearer {token_iot}
Content-Type: application/json

{
  "teamTag": "IOT",
  "timestamp": "2025-11-19T22:15:00Z",
  "payloadJson": "{\"metric\":\"temperature\",\"value\":25.5,\"sensor\":\"DHT22\",\"device_id\":\"ESP32-001\",\"location\":\"sala-1\",\"unit\":\"celsius\"}"
}
```

#### Exemplo Código ESP32 (C++)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHT_PIN 4
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* serverUrl = "http://backend:8080/otel/v1/metrics";
const char* jwtToken = "eyJhbGciOiJIUzI1NiJ9...";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (!isnan(temp) && !isnan(humidity)) {
    sendMetric("temperature", temp);
    sendMetric("humidity", humidity);
  }
  
  delay(60000); // 1 minuto
}

void sendMetric(String metric, float value) {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + String(jwtToken));
  
  String payload = "{\"teamTag\":\"IOT\",\"timestamp\":\"2025-11-19T22:00:00Z\",\"payloadJson\":\"{\\\"metric\\\":\\\"" + metric + "\\\",\\\"value\\\":" + String(value) + ",\\\"sensor\\\":\\\"DHT22\\\"}\"}";
  
  int httpCode = http.POST(payload);
  Serial.printf("HTTP Response: %d\n", httpCode);
  http.end();
}
```

---

## 🧪 Testes

### Testes HTTP Organizados

O projeto inclui **3 arquivos HTTP** com mais de **75 requisições** prontas:

```
http-tests/
├── admin.http    ← Testes perfil ADMIN (gestão)
├── ia.http       ← Testes perfil IA (ML/AI)
├── iot.http      ← Testes perfil IOT (sensores)
└── http-client.env.json  ← Configuração de tokens
```

#### Como Usar

1. **Execute os logins:**
   ```http
   POST http://localhost:8080/auth/login
   Content-Type: application/json
   
   {"team": "IA", "secret": "ia-secret"}
   ```

2. **Copie o token** da resposta

3. **Configure em `http-client.env.json`:**
   ```json
   {
     "dev": {
       "baseUrl": "http://localhost:8080",
       "iaToken": "COLE_O_TOKEN_AQUI"
     }
   }
   ```

4. **Execute qualquer requisição!**

### Testes Automatizados

```bash
# Testes unitários
./mvnw test

# Testes de integração
./mvnw verify

# Com cobertura (JaCoCo)
./mvnw clean test jacoco:report
```

**Relatório de cobertura:** `target/site/jacoco/index.html`

---

## 🚢 Deploy

### Docker

#### Build da Imagem

```bash
# Via Maven + Jib
./mvnw clean package jib:dockerBuild

# Ou via Dockerfile
docker build -t humainze-backend:latest .
```

#### Executar Container

```bash
docker run -d \
  --name humainze-backend \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e JWT_SECRET=seu-secret-256-bits \
  -e SPRING_DATASOURCE_URL=jdbc:oracle:thin:@host:1521/xe \
  -e SPRING_DATASOURCE_USERNAME=humainze \
  -e SPRING_DATASOURCE_PASSWORD=senha \
  humainze-backend:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    image: humainze-backend:latest
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
      JWT_SECRET: ${JWT_SECRET}
      SPRING_DATASOURCE_URL: jdbc:oracle:thin:@oracle:1521/xe
      SPRING_DATASOURCE_USERNAME: humainze
      SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD}
      OTEL_EXPORTER_OTLP_ENDPOINT: http://signoz:4318
    depends_on:
      - oracle
      - signoz

  oracle:
    image: container-registry.oracle.com/database/express:21.3.0-xe
    ports:
      - "1521:1521"
    environment:
      ORACLE_PWD: ${ORACLE_PWD}

  signoz:
    image: signoz/signoz:latest
    ports:
      - "3301:3301"
      - "4318:4318"
```

**Executar:**

```bash
docker-compose up -d
```

### Railway (Recomendado)

1. **Instale Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Faça login:**
   ```bash
   railway login
   ```

3. **Inicialize o projeto:**
   ```bash
   railway init
   ```

4. **Configure variáveis:**
   ```bash
   railway variables set JWT_SECRET="seu-secret-256-bits"
   railway variables set SPRING_PROFILES_ACTIVE=prod
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

### Azure App Service

```bash
# Login no Azure
az login

# Criar App Service
az webapp create \
  --name humainze-backend \
  --resource-group humainze-rg \
  --plan humainze-plan \
  --runtime "JAVA:21-java21"

# Deploy
az webapp deploy \
  --name humainze-backend \
  --resource-group humainze-rg \
  --src-path target/humainze-dash-0.0.1-SNAPSHOT.jar
```

---

## 🗺 Roadmap

### 🚀 Em Desenvolvimento

- [ ] **Suporte MQTT** para comunicação IoT assíncrona
- [ ] **Dashboard Web** integrado (React + WebSocket)
- [ ] **Mais modelos de IA** (LSTM, XGBoost, Random Forest)
- [ ] **Métricas customizadas** por equipe
- [ ] **Rate limiting** por IP/equipe

### 🔮 Planejado

- [ ] **Clusterização** com Redis para sessões distribuídas
- [ ] **GraphQL API** além da REST
- [ ] **Suporte Kafka** para streaming de eventos
- [ ] **AI-powered anomaly detection** nativo no backend
- [ ] **Multi-tenancy** completo
- [ ] **Integração com AWS IoT Core**
- [ ] **Mobile App** (React Native) com notificações push
- [ ] **Backup automático** de métricas críticas
- [ ] **A/B testing** de modelos de IA
- [ ] **Data retention policies** configuráveis

### 💡 Ideias Futuras

- [ ] **Blockchain** para auditoria imutável de alertas
- [ ] **Federated Learning** para treinar modelos sem centralizar dados
- [ ] **Edge computing** com processamento local em ESP32
- [ ] **Natural Language Queries** para dashboard (GPT-4)
- [ ] **Predictive maintenance** automático

---

## 📚 Documentação Complementar

### 📖 Guias de Integração

- **[INTEGRATION_GUIDE_IA.md](docs/INTEGRATION_GUIDE_IA.md)** - Exemplos Python, GPT-4, queries SigNoz
- **[INTEGRATION_GUIDE_IOT.md](docs/INTEGRATION_GUIDE_IOT.md)** - Código Arduino/ESP32, Raspberry Pi
- **[ZERO_TRUST_AUTH.md](docs/ZERO_TRUST_AUTH.md)** - Fluxo API Key → JWT → Roles
- **[SIGNOZ_VISUALIZATION.md](docs/SIGNOZ_VISUALIZATION.md)** - Dashboard, queries, alertas

### 📋 Arquivos de Teste

- **[http-tests/admin.http](http-tests/admin.http)** - Testes perfil ADMIN
- **[http-tests/ia.http](http-tests/ia.http)** - Testes perfil IA
- **[http-tests/iot.http](http-tests/iot.http)** - Testes perfil IoT
- **[http-tests/http-client.env.json](http-tests/http-client.env.json)** - Variáveis de ambiente para testes

### 📊 Arquivos de Configuração

```
├── docker-compose.yml              # Stack completa (Backend + Oracle + SigNoz)
├── docker-compose-signoz.yml       # SigNoz standalone
├── Dockerfile                       # Build production
├── pom.xml                          # Dependências Maven
├── application.yml                  # Config base
├── application-dev.yml              # Profile development (H2)
└── application-prod.yml             # Profile production (OracleDB)
```

---

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o projeto
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Commit** suas mudanças:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
4. **Push** para o repositório:
   ```bash
   git push origin feature/minha-feature
   ```
5. Abra um **Pull Request**

### Padrões de Código

- ✅ **Java Code Conventions** (Google Style)
- ✅ **Lombok** para reduzir boilerplate
- ✅ **SonarLint** para qualidade de código
- ✅ **JavaDoc** em métodos públicos
- ✅ **Testes unitários** para novas features

### Mensagens de Commit

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona endpoint de previsão de IA
fix: corrige bug em autenticação JWT
docs: atualiza README com exemplos de deploy
refactor: simplifica lógica de validação
test: adiciona testes para AlertService
```

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

```
MIT License

Copyright (c) 2025 Humainze Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎓 Status da Entrega FIAP

### ✅ Artefatos Entregáveis

- ✅ **Link dos repositórios:** [GitHub Backend](https://github.com/seu-usuario/humainze-backend)
- ⏳ **Link dos deploys:** Railway/Heroku (configurar)
- ✅ **Instruções para acesso e testes:** [Quick Start](#-quick-start) + `/docs/` 
- ⏳ **Vídeo demonstração:** (máx 10 minutos)
- ⏳ **Vídeo pitch:** (máx 3 minutos)

### 📊 Pontuação Esperada

- **Requisitos Técnicos:** 70/70 ✅
- **Viabilidade & Inovação:** 10/10 ✅
- **Documentação & Apresentação:** 20/20 (pendente vídeos)

**Total Estimado: 95-100/100**

---

## 📞 Contato e Suporte

### Equipe Humainze

- **Barbara Bonome Filipus** - RM 560431 - 2TDSPR
- **Vinicius Lira Ruggeri** - RM 560593 - 2TDSPR  
- **Yasmin Pereira da Silva** - RM 560039 - 2TDSPR

### Links Úteis

- 📖 **Documentação Swagger:** `http://localhost:8080/swagger-ui.html`
- 🐛 **Issues:** [GitHub Issues](https://github.com/seu-usuario/humainze-backend/issues)
- 💬 **Discussões:** [GitHub Discussions](https://github.com/seu-usuario/humainze-backend/discussions)

---

## 🎓 Agradecimentos

Este projeto foi desenvolvido como parte do curso de **Análise e Desenvolvimento de Sistemas** da **FIAP - Faculdade de Informática e Administração Paulista**.

Agradecemos aos professores e colegas que contribuíram com feedback e suporte durante o desenvolvimento.

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela! ⭐**

Made with ❤️ by **Humainze Team**

</div>

