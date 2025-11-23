import streamlit as st
import pandas as pd
import requests
import json
import time
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Humainze | Zero Trust Observatory",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para UI moderna
st.markdown("""
<style>
    /* Tema Dark Profissional */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    /* Cards modernos */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #8b92a8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Sidebar elegante */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid #00d4ff33;
    }
    
    /* Botões modernos */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
    }
    
    /* Tabs estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: #1a1a2e;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background: transparent;
        color: #8b92a8;
        font-weight: 600;
        border-radius: 8px;
        padding: 0 2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        color: white;
    }
    
    /* Badge de role */
    .role-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .role-admin {
        background: linear-gradient(90deg, #ff0844 0%, #ff6b6b 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(255, 8, 68, 0.4);
    }
    
    .role-ia {
        background: linear-gradient(90deg, #4158d0 0%, #c850c0 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(65, 88, 208, 0.4);
    }
    
    .role-iot {
        background: linear-gradient(90deg, #0ba360 0%, #3cba92 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(11, 163, 96, 0.4);
    }
    
    /* Cards com glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Títulos com gradiente */
    .gradient-title {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        animation: gradient-shift 3s ease infinite;
        background-size: 200% auto;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Status indicators */
    .status-online {
        color: #0ba360;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .status-online::before {
        content: "●";
        font-size: 1.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Constantes
JAVA_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8081")
PYTHON_COLLECTOR_URL = os.getenv("COLLECTOR_URL", "http://collector:4318")

# ========== SESSÃO ==========
if 'token' not in st.session_state:
    st.session_state.token = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# ========== FUNÇÕES ==========

def login(api_key):
    """Autentica no Java Backend"""
    try:
        response = requests.post(
            f"{JAVA_BACKEND_URL}/auth/token",
            headers={"X-API-KEY": api_key},
            timeout=5
        )
        
        if response.status_code == 200:
            token = response.json().get("token")
            
            # Decode JWT
            try:
                payload_part = token.split('.')[1]
                payload_part += '=' * (-len(payload_part) % 4)
                payload = json.loads(base64.b64decode(payload_part).decode('utf-8'))
                
                roles = payload.get("roles", [])
                role = roles[0] if isinstance(roles, list) and len(roles) > 0 else "UNKNOWN"
                sub = payload.get("sub", "unknown")
                
                return token, role, sub
            except Exception as e:
                st.error(f"❌ Erro ao decodificar token: {e}")
                return None, None, None
        else:
            return None, None, None
    except Exception as e:
        st.error(f"❌ Erro de conexão: {e}")
        return None, None, None

def fetch_secure_metrics(token, role):
    """Busca métricas do backend Java"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{JAVA_BACKEND_URL}/export/metrics",
            headers=headers,
            params={"page": 0, "size": 500},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("content", [])
        return []
    except Exception as e:
        print(f"Erro ao buscar métricas: {e}")
        return []

def fetch_secure_traces(token, role):
    """Busca traces do backend Java"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{JAVA_BACKEND_URL}/export/traces",
            headers=headers,
            params={"page": 0, "size": 500},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("content", [])
        return []
    except Exception as e:
        print(f"Erro ao buscar traces: {e}")
        return []

def fetch_secure_logs(token, role):
    """Busca logs do backend Java"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{JAVA_BACKEND_URL}/export/logs",
            headers=headers,
            params={"page": 0, "size": 500},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("content", [])
        return []
    except Exception as e:
        print(f"Erro ao buscar logs: {e}")
        return []

def fetch_alerts_count(token, role):
    """Busca contagem de alertas não resolvidos"""
    try:
        team = None
        if role == "ROLE_IA":
            team = "IA"
        elif role == "ROLE_IOT":
            team = "IOT"
        
        params = {"team": team} if team else {}
        
        response = requests.get(
            f"{JAVA_BACKEND_URL}/alerts/unresolved/count",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=5
        )
        return response.json() if response.status_code == 200 else 0
    except:
        return 0

def fetch_alerts(token, role, page=0, size=5):
    """Busca alertas não resolvidos"""
    try:
        team = None
        if role == "ROLE_IA":
            team = "IA"
        elif role == "ROLE_IOT":
            team = "IOT"
        
        params = {"page": page, "size": size}
        if team:
            params["team"] = team
        
        response = requests.get(
            f"{JAVA_BACKEND_URL}/alerts/unresolved",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=5
        )
        return response.json() if response.status_code == 200 else {"content": [], "totalElements": 0}
    except:
        return {"content": [], "totalElements": 0}

def fetch_all_alerts(token, role, page=0, size=20):
    """Busca todos os alertas (resolvidos e não resolvidos)"""
    try:
        team = None
        if role == "ROLE_IA":
            team = "IA"
        elif role == "ROLE_IOT":
            team = "IOT"
        
        params = {"page": page, "size": size}
        if team:
            params["team"] = team
        
        response = requests.get(
            f"{JAVA_BACKEND_URL}/alerts",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=5
        )
        return response.json() if response.status_code == 200 else {"content": [], "totalElements": 0}
    except:
        return {"content": [], "totalElements": 0}

def resolve_alert(token, alert_id):
    """Marca alerta como resolvido"""
    try:
        response = requests.put(
            f"{JAVA_BACKEND_URL}/alerts/{alert_id}/resolve",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

# ========== TELA DE LOGIN ==========

if not st.session_state.token:
    # Header com logo e título
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="gradient-title" style="text-align: center;">🛡️ HUMAINZE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #8b92a8; font-size: 1.2rem; margin-top: -1rem;">Zero Trust Observatory</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Autenticação Segura")
        st.markdown("Informe sua **API Key** para acessar o sistema")
        
        api_key = st.text_input("API Key", type="password", label_visibility="collapsed", placeholder="Digite sua API Key...")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 ENTRAR", use_container_width=True):
                with st.spinner("Autenticando..."):
                    token, role, user = login(api_key)
                    if token:
                        st.session_state.token = token
                        st.session_state.role = role
                        st.session_state.username = user
                        st.success(f"✅ Bem-vindo, **{user}**!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # API Keys de demonstração
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **API Keys de Demonstração:**\n\n🔴 `chave-admin` → ROLE_ADMIN\n\n🟣 `chave-ia` → ROLE_IA\n\n🟢 `chave-iot` → ROLE_IOT")
    
    st.stop()

# ========== DASHBOARD PRINCIPAL ==========

# Sidebar
with st.sidebar:
    st.markdown(f'<h2 style="color: #00d4ff; text-align: center;">👤 {st.session_state.username}</h2>', unsafe_allow_html=True)
    
    # Badge de role com estilo
    role_class = f"role-{st.session_state.role.lower().replace('role_', '')}"
    st.markdown(f'<div class="role-badge {role_class}">{st.session_state.role}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status do sistema
    st.markdown('<p class="status-online">Sistema Online</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Controles
    st.markdown("### ⚙️ Configurações")
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=False, help="Atualiza a cada 5 segundos")
    show_raw_data = st.checkbox("📊 Mostrar dados brutos", value=False)
    
    st.markdown("---")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    time_range = st.selectbox("Período", ["Últimos 5 min", "Últimos 15 min", "Última 1 hora", "Últimas 24 horas"])
    hide_system_metrics = st.checkbox("Ocultar métricas JVM", value=True)
    
    st.markdown("---")
    
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

# Header do Dashboard
st.markdown('<h1 class="gradient-title">Zero Trust Observatory</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="color: #8b92a8; font-size: 1.1rem;">Monitoramento em tempo real | Última atualização: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

# ========== BANNER DE ALERTAS ==========
alerts_count = fetch_alerts_count(st.session_state.token, st.session_state.role)

if alerts_count > 0:
    st.markdown("""
    <style>
        .alert-banner {
            background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%);
            border-radius: 15px;
            padding: 1.5rem 2rem;
            margin: 1.5rem 0;
            border-left: 5px solid #ff0844;
            box-shadow: 0 4px 20px rgba(255, 8, 68, 0.4);
            animation: pulse-alert 2s ease-in-out infinite;
        }
        
        @keyframes pulse-alert {
            0%, 100% { box-shadow: 0 4px 20px rgba(255, 8, 68, 0.4); }
            50% { box-shadow: 0 6px 30px rgba(255, 8, 68, 0.7); }
        }
        
        .alert-title {
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .alert-count {
            background: white;
            color: #ff0844;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 900;
            font-size: 1.2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div class="alert-banner">
            <div class="alert-title">
                🚨 <span class="alert-count">{alerts_count}</span> Alerta(s) Cognitivo(s) Não Resolvido(s)
            </div>
            <p style="color: white; margin: 0; font-size: 1rem;">
                Alertas críticos detectados pelo sistema de monitoramento. Verifique abaixo para detalhes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar alertas em expander
        with st.expander("🔍 Ver Alertas Detalhados", expanded=False):
            alerts_data = fetch_alerts(st.session_state.token, st.session_state.role, page=0, size=10)
            
            if alerts_data.get("content"):
                for alert in alerts_data["content"]:
                    alert_type = alert.get("type", "UNKNOWN")
                    alert_icon = {
                        "DRIFT": "📉",
                        "MODEL_ERROR": "⚠️",
                        "SERVICE_DOWN": "🔴"
                    }.get(alert_type, "❓")
                    
                    col_alert1, col_alert2 = st.columns([5, 1])
                    
                    with col_alert1:
                        st.markdown(f"""
                        **{alert_icon} {alert_type}** - Team: `{alert.get('teamTag', 'N/A')}`  
                        {alert.get('message', 'Sem descrição')}  
                        📅 {datetime.fromisoformat(alert.get('timestamp', '').replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')}
                        """)
                    
                    with col_alert2:
                        if st.button("✅ Resolver", key=f"resolve_{alert['id']}", use_container_width=True):
                            if resolve_alert(st.session_state.token, alert['id']):
                                st.success("✅ Resolvido!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("❌ Erro ao resolver")
                    
                    st.divider()
            else:
                st.info("Nenhum alerta não resolvido encontrado.")

# Buscar dados
with st.spinner("🔍 Carregando telemetria..."):
    metrics_data = fetch_secure_metrics(st.session_state.token, st.session_state.role)
    traces_data = fetch_secure_traces(st.session_state.token, st.session_state.role)
    logs_data = fetch_secure_logs(st.session_state.token, st.session_state.role)

# KPIs Principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Métricas",
        value=len(metrics_data),
        delta=f"+{len(metrics_data) % 10}" if metrics_data else "0"
    )

with col2:
    st.metric(
        label="🔗 Traces",
        value=len(traces_data),
        delta=f"+{len(traces_data) % 5}" if traces_data else "0"
    )

with col3:
    st.metric(
        label="📜 Logs",
        value=len(logs_data),
        delta=f"+{len(logs_data) % 8}" if logs_data else "0"
    )

with col4:
    st.metric(
        label="⚡ Latência Média",
        value="12ms",
        delta="-3ms"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Tabs Principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Métricas", "🔗 Traces & Spans", "📜 Logs", "🎯 Alertas"])

with tab1:
    if not metrics_data:
        st.warning("⚠️ Nenhuma métrica disponível no momento.")
    else:
        # Parse payloadJson para extrair métricas
        parsed_metrics = []
        for item in metrics_data:
            try:
                payload = json.loads(item['payloadJson'])
                # Extrair dados básicos
                parsed_metrics.append({
                    'id': item['id'],
                    'teamTag': item['teamTag'],
                    'timestamp': item['timestamp'],
                    'payload': payload
                })
            except:
                continue
        
        if not parsed_metrics:
            st.warning("⚠️ Nenhuma métrica válida encontrada.")
        else:
            st.success(f"✅ {len(parsed_metrics)} métricas carregadas")
            
            # Mostrar métricas em cards
            cols = st.columns(3)
            for idx, metric in enumerate(parsed_metrics[:6]):
                with cols[idx % 3]:
                    st.metric(
                        label=f"{metric['teamTag']} Metric #{metric['id']}",
                        value=metric['timestamp'][:19],
                        delta=None
                    )
            
            # Mostrar tabela com últimas métricas
            st.subheader("📊 Últimas Métricas")
            df_display = pd.DataFrame([
                {
                    'ID': m['id'],
                    'Team': m['teamTag'],
                    'Timestamp': m['timestamp'][:19]
                }
                for m in parsed_metrics
            ])
            st.dataframe(df_display, use_container_width=True)
            
            if show_raw_data:
                with st.expander("🔍 Dados Brutos - Payload JSON"):
                    for m in parsed_metrics[:5]:
                        st.json(m['payload'])

with tab2:
    if not traces_data:
        st.info("ℹ️ Nenhum trace capturado. Execute operações na aplicação.")
    else:
        # Parse traces
        parsed_traces = []
        for item in traces_data:
            try:
                payload = json.loads(item['payloadJson'])
                parsed_traces.append({
                    'id': item['id'],
                    'teamTag': item['teamTag'],
                    'timestamp': item['timestamp'],
                    'payload': payload
                })
            except:
                continue
        
        if not parsed_traces:
            st.warning("⚠️ Nenhum trace válido encontrado.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Traces", len(parsed_traces))
            with col2:
                st.metric("IA Traces", len([t for t in parsed_traces if t['teamTag'] == 'IA']))
            with col3:
                st.metric("IOT Traces", len([t for t in parsed_traces if t['teamTag'] == 'IOT']))
            
            # Mostrar tabela
            st.subheader("🔍 Traces Capturados")
            df_display = pd.DataFrame([
                {
                    'ID': t['id'],
                    'Team': t['teamTag'],
                    'Timestamp': t['timestamp'][:19]
                }
                for t in parsed_traces
            ])
            st.dataframe(df_display, use_container_width=True)
            
            if show_raw_data:
                with st.expander("🔍 Dados Brutos - Traces JSON"):
                    for t in parsed_traces[:5]:
                        st.json(t['payload'])

with tab3:
    if not logs_data:
        st.info("ℹ️ Nenhum log capturado. Verifique a configuração do logback.")
    else:
        # Parse logs
        parsed_logs = []
        for item in logs_data:
            try:
                payload = json.loads(item['payloadJson'])
                parsed_logs.append({
                    'id': item['id'],
                    'teamTag': item['teamTag'],
                    'timestamp': item['timestamp'],
                    'payload': payload
                })
            except:
                continue
        
        if not parsed_logs:
            st.warning("⚠️ Nenhum log válido encontrado.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Logs", len(parsed_logs))
            with col2:
                st.metric("IA Logs", len([l for l in parsed_logs if l['teamTag'] == 'IA']))
            with col3:
                st.metric("IOT Logs", len([l for l in parsed_logs if l['teamTag'] == 'IOT']))
            
            # Mostrar tabela
            st.subheader("📄 Logs Capturados")
            df_display = pd.DataFrame([
                {
                    'ID': l['id'],
                    'Team': l['teamTag'],
                    'Timestamp': l['timestamp'][:19]
                }
                for l in parsed_logs
            ])
            st.dataframe(df_display, use_container_width=True)
            
            if show_raw_data:
                with st.expander("🔍 Dados Brutos - Logs JSON"):
                    for l in parsed_logs[:5]:
                        st.json(l['payload'])

with tab4:
    st.markdown("### 🎯 Central de Alertas Cognitivos")
    
    # Tabs para filtrar alertas
    alert_tab1, alert_tab2 = st.tabs(["🔴 Não Resolvidos", "✅ Todos"])
    
    with alert_tab1:
        st.markdown("#### Alertas Ativos Aguardando Resolução")
        
        alerts_data = fetch_alerts(st.session_state.token, st.session_state.role, page=0, size=20)
        
        if alerts_data.get("content"):
            st.info(f"📊 Total de {alerts_data['totalElements']} alerta(s) não resolvido(s)")
            
            for alert in alerts_data["content"]:
                alert_type = alert.get("type", "UNKNOWN")
                alert_icon = {
                    "DRIFT": "📉",
                    "MODEL_ERROR": "⚠️",
                    "SERVICE_DOWN": "🔴"
                }.get(alert_type, "❓")
                
                alert_color = {
                    "DRIFT": "#ff9800",
                    "MODEL_ERROR": "#f44336",
                    "SERVICE_DOWN": "#ff0844"
                }.get(alert_type, "#9e9e9e")
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, {alert_color}22 0%, {alert_color}11 100%);
                                border-left: 4px solid {alert_color};
                                border-radius: 10px;
                                padding: 1rem;
                                margin: 0.5rem 0;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.5rem;">{alert_icon}</span>
                            <strong style="color: {alert_color}; font-size: 1.1rem;">{alert_type}</strong>
                            <span style="color: #8b92a8; margin-left: auto;">Team: {alert.get('teamTag', 'N/A')}</span>
                        </div>
                        <p style="margin: 0.5rem 0; color: white;">{alert.get('message', 'Sem descrição')}</p>
                        <small style="color: #8b92a8;">📅 {datetime.fromisoformat(alert.get('timestamp', '').replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([6, 2, 2])
                    with col3:
                        if st.button("✅ Marcar como Resolvido", key=f"resolve_tab_{alert['id']}", use_container_width=True):
                            with st.spinner("Resolvendo..."):
                                if resolve_alert(st.session_state.token, alert['id']):
                                    st.success("✅ Alerta resolvido com sucesso!")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao resolver alerta")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.success("🎉 Nenhum alerta ativo! Sistema operando normalmente.")
    
    with alert_tab2:
        st.markdown("#### Histórico Completo de Alertas")
        
        # Filtros
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            filter_status = st.selectbox(
                "Status",
                ["Todos", "Não Resolvidos", "Resolvidos"],
                key="history_status_filter"
            )
        
        with col2:
            filter_type = st.selectbox(
                "Tipo",
                ["Todos", "DRIFT", "MODEL_ERROR", "SERVICE_DOWN"],
                key="history_type_filter"
            )
        
        with col3:
            page_size = st.selectbox(
                "Itens por página",
                [10, 20, 50, 100],
                index=1,
                key="history_page_size"
            )
        
        # Paginação
        if 'history_page' not in st.session_state:
            st.session_state.history_page = 0
        
        # Buscar dados
        all_alerts_data = fetch_all_alerts(
            st.session_state.token, 
            st.session_state.role, 
            page=st.session_state.history_page,
            size=page_size
        )
        
        if all_alerts_data.get("content"):
            alerts_to_display = all_alerts_data["content"]
            
            # Aplicar filtros locais
            if filter_status == "Não Resolvidos":
                alerts_to_display = [a for a in alerts_to_display if not a.get("resolved", False)]
            elif filter_status == "Resolvidos":
                alerts_to_display = [a for a in alerts_to_display if a.get("resolved", False)]
            
            if filter_type != "Todos":
                alerts_to_display = [a for a in alerts_to_display if a.get("type") == filter_type]
            
            # Informações de paginação
            total_elements = all_alerts_data.get("totalElements", 0)
            total_pages = all_alerts_data.get("totalPages", 1)
            current_page = st.session_state.history_page
            
            st.info(f"📊 Mostrando {len(alerts_to_display)} de {total_elements} alerta(s) | Página {current_page + 1} de {total_pages}")
            
            # Tabela de alertas
            if alerts_to_display:
                for idx, alert in enumerate(alerts_to_display):
                    alert_type = alert.get("type", "UNKNOWN")
                    is_resolved = alert.get("resolved", False)
                    
                    alert_icon = {
                        "DRIFT": "📉",
                        "MODEL_ERROR": "⚠️",
                        "SERVICE_DOWN": "🔴"
                    }.get(alert_type, "❓")
                    
                    alert_color = {
                        "DRIFT": "#ff9800",
                        "MODEL_ERROR": "#f44336",
                        "SERVICE_DOWN": "#ff0844"
                    }.get(alert_type, "#9e9e9e")
                    
                    status_badge = "✅ RESOLVIDO" if is_resolved else "🔴 ATIVO"
                    status_color = "#4caf50" if is_resolved else "#ff0844"
                    
                    with st.container():
                        st.markdown(f"""
                        <div style="background: linear-gradient(90deg, {alert_color}22 0%, {alert_color}11 100%);
                                    border-left: 4px solid {alert_color};
                                    border-radius: 10px;
                                    padding: 1rem;
                                    margin: 0.5rem 0;
                                    opacity: {'0.6' if is_resolved else '1'};">
                            <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                                <span style="font-size: 1.5rem;">{alert_icon}</span>
                                <strong style="color: {alert_color}; font-size: 1.1rem;">{alert_type}</strong>
                                <span style="background: {status_color}; color: white; padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.8rem; font-weight: 700;">{status_badge}</span>
                                <span style="color: #8b92a8; margin-left: auto;">ID: {alert.get('id', 'N/A')} | Team: {alert.get('teamTag', 'N/A')}</span>
                            </div>
                            <p style="margin: 0.5rem 0; color: white;">{alert.get('message', 'Sem descrição')}</p>
                            <small style="color: #8b92a8;">📅 {datetime.fromisoformat(alert.get('timestamp', '').replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botão de resolver apenas para alertas ativos
                        if not is_resolved:
                            col1, col2, col3 = st.columns([6, 2, 2])
                            with col3:
                                if st.button("✅ Resolver", key=f"resolve_history_{alert['id']}", use_container_width=True):
                                    with st.spinner("Resolvendo..."):
                                        if resolve_alert(st.session_state.token, alert['id']):
                                            st.success("✅ Resolvido!")
                                            time.sleep(0.5)
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao resolver")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                
                # Controles de paginação
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                
                with col2:
                    if st.button("⏮️ Primeira", disabled=(current_page == 0), use_container_width=True):
                        st.session_state.history_page = 0
                        st.rerun()
                
                with col3:
                    if st.button("◀️ Anterior", disabled=(current_page == 0), use_container_width=True):
                        st.session_state.history_page = max(0, current_page - 1)
                        st.rerun()
                
                with col4:
                    if st.button("Próxima ▶️", disabled=(current_page >= total_pages - 1), use_container_width=True):
                        st.session_state.history_page = min(total_pages - 1, current_page + 1)
                        st.rerun()
                
                with col5:
                    if st.button("Última ⏭️", disabled=(current_page >= total_pages - 1), use_container_width=True):
                        st.session_state.history_page = total_pages - 1
                        st.rerun()
            else:
                st.warning("⚠️ Nenhum alerta encontrado com os filtros aplicados.")
        else:
            st.info("ℹ️ Nenhum alerta registrado no sistema ainda.")

# Auto-refresh
if auto_refresh:
    time.sleep(5)
    st.rerun()
