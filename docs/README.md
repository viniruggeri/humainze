# 📚 Documentação Técnica - Humainze Backend

Bem-vindo à documentação completa do **Humainze Backend**, uma plataforma cognitiva integrada que conecta IoT, IA e Dashboard Web.

## 🎯 Visão Geral

Humainze é uma **plataforma completa de observabilidade open-source** que:
- 🔌 Recebe dados de sensores IoT (Arduino/ESP32) via HTTP
- 🤖 Integra com módulos de IA Python para predições
- 📊 Persiste métricas/traces/logs em banco relacional (Oracle/H2)
- 📈 Dashboard Streamlit customizado com gráficos Plotly
- 🚨 Sistema de alertas cognitivos em tempo real
- ✅ **100% open-source** - sem dependências de SigNoz, Grafana ou Datadog

## 📖 Documentação Disponível

### [📋 Sumário Executivo](EXECUTIVE_SUMMARY.md)
Visão geral do projeto, objetivos, arquitetura e stack tecnológico.

### [🤖 Guia de Integração - IA](INTEGRATION_GUIDE_IA.md)
Como integrar módulos de IA Python com o backend:
- Exemplos de código Python
- APIs de predição e treinamento
- Detecção de drift
- Queries SigNoz

### [🔌 Guia de Integração - IoT](INTEGRATION_GUIDE_IOT.md)
Como conectar sensores e dispositivos IoT:
- Código Arduino/ESP32
- Protocolo HTTP/MQTT
- Formato de payloads
- Troubleshooting

### [📡 Endpoints OpenTelemetry](OTEL_INGESTION_ENDPOINTS.md)
Documentação completa dos endpoints OTLP:
- `/otel/v1/metrics` - Ingestão de métricas
- `/otel/v1/traces` - Ingestão de traces
- `/otel/v1/logs` - Ingestão de logs

### [📦 Exemplos de Payloads](PAYLOAD_EXAMPLES.md)
Payloads JSON prontos para usar:
- Métricas IoT (temperatura, umidade, CO2)
- Traces distribuídos
- Logs estruturados
- Alertas cognitivos

### [📊 Dashboard Customizado](DASHBOARD_GUIDE.md)
Como usar o dashboard Streamlit para observabilidade:
- Gráficos interativos com Plotly
- Métricas em tempo real (IoT + IA)
- Sistema de alertas com banner
- Filtros, paginação e auto-refresh

### [🗂️ Índice Completo](INDEX.md)
Índice navegável de toda a documentação com links rápidos.

## 🚀 Quick Links

- **[README Principal](../README.md)** - Documentação completa do projeto
- **[Swagger UI](http://localhost:8080/swagger-ui.html)** - Documentação interativa da API
- **[GitHub Repository](https://github.com/viniruggeri/humainze-java)** - Código fonte
- **[Dashboard Streamlit](http://localhost:8501)** - Interface de monitoramento

## 👥 Equipe

| Nome | RM | Turma |
|------|-----|-------|
| **Barbara Bonome Filipus** | 560431 | 2TDSPR |
| **Vinicius Lira Ruggeri** | 560593 | 2TDSPR |
| **Yasmin Pereira da Silva** | 560039 | 2TDSPR |

## 📋 Requisitos FIAP Atendidos

✅ **API Rest + Boas Práticas**  
✅ **Spring Data JPA**  
✅ **Relacionamentos entre Entidades**  
✅ **Bean Validation**  
✅ **Paginação, Ordenação e Filtros**  
✅ **Documentação Swagger**  
✅ **Autenticação JWT**  
✅ **Deploy em Nuvem (Azure VM)**

**Nota:** 100/100 pontos nos requisitos técnicos FIAP.

## 🏗️ Arquitetura

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   IoT Layer │────────▶│  Humainze Backend│◀────────│  IA Module  │
│             │  HTTP   │   (Spring Boot)  │  HTTP   │   (Python)  │
│ ESP32/Arduino│        │                  │         │   Prophet   │
└─────────────┘         │   Port: 8080     │         │ Drift Detect│
                        └──────────────────┘         └─────────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │    Dashboard     │
                        │   (Streamlit)    │
                        │   Port: 8501     │
                        └──────────────────┘
```

## 🛠️ Stack Tecnológico

- **Backend:** Java 21, Spring Boot 3.5.7
- **Persistência:** Spring Data JPA, OracleDB (prod), H2 (dev)
- **Segurança:** Spring Security, JWT (JJWT 0.12.6)
- **Observabilidade:** Backend Java (servidor OTLP customizado)
- **Dashboard:** Python 3.11, Streamlit, Plotly, Pandas
- **Deploy:** Docker, Docker Compose, Azure VM

## 📞 Contato

Para dúvidas ou sugestões, entre em contato com a equipe via GitHub Issues.

---

**Última atualização:** 21/11/2025  
**Versão:** 1.0.0  
**Status:** ✅ Production Ready
