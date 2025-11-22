# 📝 Changelog - Documentação Atualizada

**Data:** 21/11/2025  
**Versão:** 2.0.0

---

## 🔄 Mudanças Principais

### ❌ Removido

- **SigNoz** - Removida dependência de ferramenta externa de observabilidade
- **OpenTelemetry Exporter** - Não mais necessário exportar para SigNoz
- **Micrometer para SigNoz** - Backend agora é o próprio servidor de telemetria
- **Grafana** - Dashboard customizado Streamlit substitui Grafana
- **Datadog** - Solução 100% open-source

### ✅ Adicionado

- **Backend Java como Servidor OTLP** - Endpoints `/otel/v1/metrics`, `/otel/v1/traces`, `/otel/v1/logs`
- **Persistência em Banco SQL** - OracleDB (prod) e H2 (dev)
- **APIs REST de Consulta** - `/export/metrics`, `/export/traces`, `/export/logs` com paginação
- **Dashboard Streamlit Customizado** - Visualizações Plotly, alertas em tempo real
- **Sistema de Alertas Completo** - DRIFT, MODEL_ERROR, SERVICE_DOWN com banner e histórico
- **Documentação DASHBOARD_GUIDE.md** - Guia completo do dashboard

### 🔧 Atualizado

- **INTEGRATION_GUIDE_IOT.md** - Autenticação via JWT (não mais API Key simples)
- **INTEGRATION_GUIDE_IA.md** - Fluxo de login e envio de métricas para backend Java
- **README.md** - Destacando solução open-source completa
- **EXECUTIVE_SUMMARY.md** - Foco em observabilidade sem dependências externas
- **docs/README.md** - Links para novo guia do dashboard

---

## 📊 Arquitetura Antes vs. Depois

### Antes (com SigNoz)

```
IoT/IA → Backend Java → SigNoz (Docker) → Dashboard SigNoz Web
                ↓
           OracleDB/H2
```

**Problemas:**
- Dependência de ferramenta externa (SigNoz)
- Complexidade de setup (mais containers Docker)
- Difícil de customizar visualizações
- Necessita OpenTelemetry Exporter

### Depois (Backend + Dashboard Custom)

```
IoT/IA → Backend Java (servidor OTLP) → OracleDB/H2
              ↓
         APIs REST (/export/*)
              ↓
      Dashboard Streamlit (Plotly)
```

**Vantagens:**
- ✅ **100% open-source** - sem dependências proprietárias
- ✅ **Persistência SQL nativa** - queries diretas no banco
- ✅ **Dashboard customizável** - Python + Streamlit, fácil de modificar
- ✅ **Menos containers** - apenas backend + dashboard
- ✅ **Simples e eficaz** - sem complexidade de observability tools

---

## 🗂️ Arquivos Modificados

### Documentação Principal

- ✏️ `README.md` - Atualizado stack, removido SigNoz
- ✏️ `docs/README.md` - Novo link para DASHBOARD_GUIDE.md
- ✏️ `docs/EXECUTIVE_SUMMARY.md` - Foco em solução open-source
- ✏️ `docs/INDEX.md` - Atualizado links
- ➕ `docs/DASHBOARD_GUIDE.md` - **NOVO** guia completo do dashboard

### Guias de Integração

- ✏️ `docs/INTEGRATION_GUIDE_IOT.md` - Autenticação JWT, sem API Key
- ✏️ `docs/INTEGRATION_GUIDE_IA.md` - Fluxo atualizado, sem SigNoz
- ✏️ `docs/OTEL_INGESTION_ENDPOINTS.md` - Endpoints servidos pelo backend Java
- ✏️ `docs/PAYLOAD_EXAMPLES.md` - Exemplos ajustados

### Sistema de Alertas

- ✏️ `docs/ALERTS_SYSTEM.md` - Dashboard Streamlit em tempo real
- ✏️ `dashboard/app.py` - Auto-refresh, banner, paginação

### Deploy

- ✏️ `docs/DEPLOY_AZURE.md` - Docker Compose com 2 containers (backend + dashboard)
- ✏️ `docker-compose.yml` - Removido container SigNoz

---

## 🚀 Como Usar a Nova Arquitetura

### 1️⃣ Subir Backend Java

```bash
cd humainze-java
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

**Backend em:** `http://localhost:8080`

### 2️⃣ Subir Dashboard Streamlit

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

**Dashboard em:** `http://localhost:8501`

### 3️⃣ IoT/IA Enviam Métricas

```python
import requests

# Login
response = requests.post(
    "http://localhost:8080/auth/login",
    json={"team": "IA", "secret": "ia-secret"}
)
token = response.json()["token"]

# Enviar métrica
requests.post(
    "http://localhost:8080/otel/v1/metrics",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "teamTag": "IA",
        "timestamp": "2025-11-21T10:00:00Z",
        "payloadJson": '{"metric":"model_accuracy","value":0.95}'
    }
)
```

### 4️⃣ Visualizar no Dashboard

- Abra `http://localhost:8501`
- Tab "🤖 Métricas IA" mostra gráficos Plotly
- Tab "🔴 Alertas" mostra alertas em tempo real
- Auto-refresh atualiza a cada 5 segundos

---

## 📚 Nova Estrutura de Documentação

```
docs/
├── README.md                    ← Introdução atualizada
├── INDEX.md                     ← Índice completo
├── EXECUTIVE_SUMMARY.md         ← Sumário executivo
├── INTEGRATION_GUIDE_IA.md      ← Guia IA (atualizado)
├── INTEGRATION_GUIDE_IOT.md     ← Guia IoT (atualizado)
├── OTEL_INGESTION_ENDPOINTS.md  ← Endpoints backend Java
├── PAYLOAD_EXAMPLES.md          ← Exemplos de JSON
├── DASHBOARD_GUIDE.md           ← **NOVO** Guia do dashboard
├── ALERTS_SYSTEM.md             ← Sistema de alertas
├── DEPLOY_AZURE.md              ← Deploy Azure VM
├── GITHUB_PAGES_SETUP.md        ← Configurar GitHub Pages
├── _config.yml                  ← Jekyll config
└── index.html                   ← Landing page
```

---

## ✅ Checklist de Migração

Se você estava usando SigNoz antes:

- [ ] Remover container SigNoz do `docker-compose.yml`
- [ ] Remover variáveis `OTEL_EXPORTER_OTLP_ENDPOINT` do `.env`
- [ ] Atualizar código IoT/IA para usar JWT (login em `/auth/login`)
- [ ] Instalar dependências do dashboard: `pip install -r requirements.txt`
- [ ] Subir dashboard: `streamlit run app.py`
- [ ] Testar visualizações em `http://localhost:8501`

---

## 🎓 Requisitos FIAP

**Status:** ✅ 100/100 pontos mantidos

A mudança para solução open-source **não afeta** os requisitos FIAP:

- ✅ API Rest + Boas Práticas
- ✅ Spring Data JPA
- ✅ Relacionamentos (@ManyToOne, @OneToMany)
- ✅ Bean Validation
- ✅ Paginação/Ordenação/Filtros
- ✅ Swagger/OpenAPI
- ✅ JWT
- ✅ Deploy (Azure VM com Docker Compose)

**Bônus:** A solução open-source demonstra **ainda mais inovação** e **viabilidade técnica**.

---

## 📞 Suporte

Para dúvidas sobre as mudanças:

1. Consulte [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)
2. Veja [INTEGRATION_GUIDE_IA.md](INTEGRATION_GUIDE_IA.md) e [INTEGRATION_GUIDE_IOT.md](INTEGRATION_GUIDE_IOT.md)
3. Abra issue no [GitHub](https://github.com/viniruggeri/humainze-java/issues)

---

**Equipe Humainze:**
- Barbara Bonome Filipus (RM560431)
- Vinicius Lira Ruggeri (RM560593)
- Yasmin Pereira da Silva (RM560039)

**Turma:** 2TDSPR  
**Data:** 21/11/2025
