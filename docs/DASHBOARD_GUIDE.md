# 📊 Dashboard Streamlit - Guia Completo

## Visão Geral

O **Dashboard Humainze** é uma solução 100% open-source de visualização de métricas e alertas, construída com **Streamlit** e **Plotly**. Roda na porta **8501** e consome APIs REST do backend Java.

## 🎯 Principais Funcionalidades

### ✅ O que o Dashboard oferece

- **📈 Gráficos Interativos** - Plotly com zoom, pan, hover
- **⏱️ Métricas em Tempo Real** - IoT e IA atualizando ao vivo
- **🚨 Sistema de Alertas** - Banner + histórico completo
- **🔍 Filtros Avançados** - Por team, tipo, status, período
- **📄 Paginação** - Navegação eficiente em grandes volumes
- **🔄 Auto-Refresh** - Polling automático a cada 5 segundos
- **🎨 Totalmente Customizável** - Python puro, fácil de modificar

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Dashboard Streamlit                   │
│                     (Frontend)                           │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP REST
┌─────────────────────────────────────────────────────────┐
│              Backend Java (Spring Boot)                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  GET /export/metrics?team=IA&page=0&size=20       │  │
│  │  GET /export/traces?page=0&size=10                │  │
│  │  GET /alerts/unresolved/count?team=IA             │  │
│  │  PUT /alerts/{id}/resolve                         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│            Banco de Dados (Oracle/H2)                    │
│  • MetricRecord (timestamp, metric, value, teamTag)     │
│  • SpanRecord (traceId, spanId, operationName)          │
│  • Alert (type, message, resolved, timestamp)           │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Instalação e Configuração

### 1️⃣ Instalar Dependências

```bash
cd dashboard
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit==1.31.0
requests==2.31.0
pandas==2.1.4
plotly==5.18.0
```

### 2️⃣ Configurar Backend URL

Edite `app.py` se necessário:

```python
BACKEND_URL = "http://localhost:8080"  # URL do backend Java
```

### 3️⃣ Executar Dashboard

```bash
streamlit run app.py
```

**Acesse:** `http://localhost:8501`

## 📊 Funcionalidades Detalhadas

### 1. Métricas IoT

**Tab "📡 Métricas IoT"**

Visualiza métricas de sensores em tempo real:

**Tipos de gráficos:**
- **Time Series** - Temperatura, Umidade, CO2 ao longo do tempo
- **Gauge** - Valor atual com limites mín/máx
- **Bar Chart** - Comparação entre sensores/locais

**Filtros disponíveis:**
- Team (IA, IOT, ADMIN)
- Período (última hora, 6h, 24h, 7 dias)
- Tipo de métrica (temperatura, humidity, co2_ppm, etc.)
- Itens por página (10/20/50/100)

**Código exemplo:**

```python
import streamlit as st
import requests
import plotly.express as px

# Buscar métricas do backend
response = requests.get(
    f"{BACKEND_URL}/export/metrics",
    params={
        "teamTag": "IOT",
        "page": 0,
        "size": 100,
        "sort": "timestamp,desc"
    },
    headers={"Authorization": f"Bearer {token}"}
)

data = response.json()["content"]
df = pd.DataFrame(data)

# Gráfico de linha (temperatura)
fig = px.line(
    df[df["metric"] == "temperature"],
    x="timestamp",
    y="value",
    title="Temperatura ao Longo do Tempo",
    labels={"value": "°C", "timestamp": "Data/Hora"}
)

st.plotly_chart(fig, use_container_width=True)
```

### 2. Métricas de IA

**Tab "🤖 Métricas IA"**

Visualiza métricas de modelos de Machine Learning:

**Métricas suportadas:**
- `model_accuracy` - Acurácia do modelo (0-1)
- `model_loss` - Loss function
- `inference_latency_ms` - Latência de inferência
- `training_progress` - Progresso do treinamento (%)
- `drift_score` - Score de drift (0-1)

**Gráficos disponíveis:**
- **Line Chart** - Evolução de acurácia/loss
- **Gauge** - Acurácia atual vs. threshold
- **Scatter Plot** - Drift score vs. accuracy
- **Histogram** - Distribuição de latências

**Exemplo de uso:**

```python
# Buscar métricas de IA
response = requests.get(
    f"{BACKEND_URL}/export/metrics",
    params={"teamTag": "IA", "page": 0, "size": 50},
    headers={"Authorization": f"Bearer {token}"}
)

df = pd.DataFrame(response.json()["content"])

# Filtrar acurácia
accuracy_df = df[df["metric"] == "model_accuracy"]

# Gauge de acurácia
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=accuracy_df["value"].iloc[-1],
    title={"text": "Acurácia do Modelo"},
    delta={"reference": 0.90},
    gauge={
        "axis": {"range": [0, 1]},
        "bar": {"color": "darkblue"},
        "steps": [
            {"range": [0, 0.7], "color": "red"},
            {"range": [0.7, 0.9], "color": "yellow"},
            {"range": [0.9, 1], "color": "green"}
        ],
        "threshold": {
            "line": {"color": "red", "width": 4},
            "thickness": 0.75,
            "value": 0.90
        }
    }
))

st.plotly_chart(fig)
```

### 3. Sistema de Alertas

**Banner de Alertas**

Aparece no topo quando há alertas não resolvidos:

```
┌────────────────────────────────────────────────────────┐
│ 🚨 [5] Alerta(s) Cognitivo(s) Não Resolvido(s)       │
│ Alertas críticos detectados pelo sistema              │
│ ▼ Ver Alertas Detalhados                              │
└────────────────────────────────────────────────────────┘
```

**Features:**
- Contagem em tempo real
- Animação pulsante
- Expander para ver detalhes
- Botão "Resolver" inline

**Tab "🔴 Alertas Ativos"**

Lista todos os alertas não resolvidos:

```python
# Buscar alertas ativos
response = requests.get(
    f"{BACKEND_URL}/alerts/unresolved",
    params={"team": "IA"},
    headers={"Authorization": f"Bearer {token}"}
)

alerts = response.json()["content"]

for alert in alerts:
    with st.container():
        st.markdown(f"""
        <div style='border-left: 4px solid #ff9800; padding: 1rem; margin: 1rem 0;'>
            <strong>#{alert['id']} - {alert['type']}</strong><br>
            📅 {alert['timestamp']}<br>
            💬 {alert['message']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"✅ Resolver #{alert['id']}"):
            requests.put(
                f"{BACKEND_URL}/alerts/{alert['id']}/resolve",
                headers={"Authorization": f"Bearer {token}"}
            )
            st.rerun()
```

**Tab "✅ Histórico Completo"**

Histórico de todos os alertas com filtros:

- **Status:** Todos / Não Resolvidos / Resolvidos
- **Tipo:** Todos / DRIFT / MODEL_ERROR / SERVICE_DOWN
- **Paginação:** 10 / 20 / 50 / 100 itens por página

### 4. Auto-Refresh

**Checkbox na Sidebar:**

```python
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh", value=False)

if auto_refresh:
    import time
    time.sleep(5)  # 5 segundos
    st.rerun()
```

## 🎨 Customizações Comuns

### Mudar Tema de Cores

Edite `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Adicionar Novo Gráfico

```python
def plot_custom_metric(df, metric_name):
    """Plota métrica customizada"""
    filtered = df[df["metric"] == metric_name]
    
    fig = px.area(
        filtered,
        x="timestamp",
        y="value",
        title=f"{metric_name.title()} ao Longo do Tempo",
        color_discrete_sequence=["#667eea"]
    )
    
    fig.update_layout(
        xaxis_title="Data/Hora",
        yaxis_title="Valor",
        hovermode="x unified"
    )
    
    return fig

# Uso
st.plotly_chart(plot_custom_metric(df, "co2_ppm"))
```

### Adicionar Filtro de Data

```python
from datetime import datetime, timedelta

st.sidebar.subheader("📅 Filtro de Período")

periodo = st.sidebar.selectbox(
    "Período",
    ["Última hora", "Últimas 6 horas", "Últimas 24 horas", "Últimos 7 dias"]
)

# Calcular timestamps
now = datetime.now()
if periodo == "Última hora":
    start = now - timedelta(hours=1)
elif periodo == "Últimas 6 horas":
    start = now - timedelta(hours=6)
elif periodo == "Últimas 24 horas":
    start = now - timedelta(days=1)
else:
    start = now - timedelta(days=7)

# Filtrar DataFrame
df_filtered = df[df["timestamp"] >= start.isoformat()]
```

## 🔧 Troubleshooting

### Dashboard não conecta ao backend

**Problema:** `ConnectionError: [Errno 111] Connection refused`

**Solução:**
1. Verificar se backend está rodando: `curl http://localhost:8080/actuator/health`
2. Confirmar URL em `app.py`: `BACKEND_URL = "http://localhost:8080"`
3. Verificar firewall/portas

### Gráficos não aparecem

**Problema:** Gráfico vazio ou erro no Plotly

**Solução:**
1. Verificar se há dados: `st.write(df)` antes do gráfico
2. Confirmar formato de timestamp: deve ser ISO 8601
3. Verificar tipos de dados: `df.dtypes`

### Autenticação falha

**Problema:** `401 Unauthorized`

**Solução:**
1. Verificar token JWT válido
2. Confirmar que secret está correto
3. Testar login manual:
   ```python
   response = requests.post(
       f"{BACKEND_URL}/auth/login",
       json={"team": "IA", "secret": "ia-secret"}
   )
   print(response.json())
   ```

## 📈 Métricas do Dashboard

O dashboard expõe suas próprias métricas:

```python
# Contadores
dashboard_page_views = 1523
dashboard_api_calls = 8921
dashboard_errors = 12

# Latências (ms)
avg_load_time = 450
p95_load_time = 890
max_load_time = 1200
```

## 🚀 Deploy em Produção

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
dashboard:
  build: ./dashboard
  ports:
    - "8501:8501"
  environment:
    - BACKEND_URL=http://backend:8080
  depends_on:
    - backend
```

## 📚 Recursos Adicionais

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)

---

**Última atualização:** 21/11/2025  
**Versão:** 1.0.0  
**Autor:** Equipe Humainze (RM560431, RM560593, RM560039)
