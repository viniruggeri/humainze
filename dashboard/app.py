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

# CSS mínimo - removido para debug
st.markdown("""
<style>
    .stApp {
        background: #0f0f23;
    }
</style>
""", unsafe_allow_html=True)

# Constantes
JAVA_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")  # 8080 - Expo/React Native usa 8081
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
    """Busca métricas do collector FastAPI (porta 4318)"""
    try:
        # Busca do collector OTLP, não do backend Java
        response = requests.get(
            "http://localhost:4318/api/metrics",
            params={"role": role},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"🔍 DEBUG: Recebidas {len(data)} métricas do collector")
            if data:
                print(f"🔍 DEBUG: Primeira métrica: {data[0]}")
            return data
        else:
            print(f"🔍 DEBUG: Status {response.status_code} ao buscar métricas")
        return []
    except Exception as e:
        print(f"Erro ao buscar métricas: {e}")
        return []

def fetch_secure_traces(token, role):
    """Busca traces do collector FastAPI (porta 4318)"""
    try:
        # Busca do collector OTLP, não do backend Java
        response = requests.get(
            "http://localhost:4318/api/traces",
            params={"role": role},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Erro ao buscar traces: {e}")
        return []

def fetch_secure_logs(token, role):
    """Busca logs do collector FastAPI (porta 4318)"""
    try:
        # Busca do collector OTLP, não do backend Java
        response = requests.get(
            "http://localhost:4318/api/logs",
            params={"role": role},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
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

# Tabs Principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Métricas", "🔗 Traces & Spans", "📜 Logs", "🎯 Alertas"])

with tab1:
    if not metrics_data:
        st.warning("⚠️ Nenhuma métrica disponível no momento.")
    else:
        # O collector retorna dados já processados do SQLite
        # Formato: [{"timestamp": "...", "service_name": "...", "metric_name": "...", "value": 123, "unit": "...", "attributes": "{}"}]
        flat_metrics = []
        for item in metrics_data:
            try:
                # Parse attributes JSON
                attributes = json.loads(item.get('attributes', '{}'))
                team = attributes.get('team', 'UNKNOWN')
                
                flat_metrics.append({
                    'metric_name': item.get('metric_name'),
                    'service_name': item.get('service_name'),
                    'value': float(item.get('value', 0)),
                    'unit': item.get('unit', ''),
                    'timestamp': pd.to_datetime(item.get('timestamp')),
                    'teamTag': team
                })
            except Exception as e:
                print(f"🔍 DEBUG: Erro ao processar métrica: {e}")
                continue
        
        print(f"🔍 DEBUG: Total de flat_metrics processadas: {len(flat_metrics)}")
        if flat_metrics:
            print(f"🔍 DEBUG: Primeira flat_metric: {flat_metrics[0]}")
        
        if not flat_metrics:
            st.warning("⚠️ Nenhuma métrica válida encontrada.")
        else:
            df = pd.DataFrame(flat_metrics)
            st.success(f"✅ {len(df)} métricas carregadas")
            print(f"🔍 DEBUG: DataFrame criado com {len(df)} linhas")
            print(f"🔍 DEBUG: Colunas do DataFrame: {df.columns.tolist()}")
            if len(df) > 0:
                print(f"🔍 DEBUG: Primeira linha do DataFrame: {df.iloc[0].to_dict()}")
            
            # Pegar role do session state
            role = st.session_state.role
            
            # Visualizações específicas por Team
            if role == "ROLE_IOT":
                st.subheader("🌡️ Monitoramento de Sensores ESP32")
                
                # Definir métricas IoT com ícones e cores (aceita ambos formatos)
                iot_metrics = {
                    'temperature': {'icon': '🌡️', 'title': 'Temperatura', 'unit': '°C', 'color': '#FF6B6B'},
                    'humidity': {'icon': '💧', 'title': 'Umidade', 'unit': '%', 'color': '#4ECDC4'},
                    'air_quality_ppm': {'icon': '☁️', 'title': 'Qualidade do Ar (CO2)', 'unit': 'ppm', 'color': '#95E1D3'},
                    'luminosity_lux': {'icon': '💡', 'title': 'Luminosidade', 'unit': 'lux', 'color': '#FFE66D'}
                }
                
                print(f"🔍 DEBUG: Métricas únicas no DataFrame: {df['metric_name'].unique().tolist()}")
                
                for metric_key, config in iot_metrics.items():
                    metric_df = df[df['metric_name'] == metric_key]
                    
                    print(f"🔍 DEBUG: Procurando métrica '{metric_key}' - encontradas {len(metric_df)} linhas")
                    
                    if not metric_df.empty:
                        st.markdown(f"### {config['icon']} {config['title']}")
                        
                        print(f"🔍 DEBUG: Criando gráfico para '{metric_key}' com {len(metric_df)} pontos")
                        
                        fig = go.Figure()
                        for service in metric_df['service_name'].unique():
                            service_data = metric_df[metric_df['service_name'] == service].sort_values('timestamp')
                            print(f"🔍 DEBUG: Adicionando trace para sensor '{service}' com {len(service_data)} pontos")
                            fig.add_trace(go.Scatter(
                                x=service_data['timestamp'],
                                y=service_data['value'],
                                mode='lines+markers',
                                name=service,
                                line=dict(width=3, color=config['color']),
                                marker=dict(size=8),
                                hovertemplate=f'<b>{config["title"]}</b><br>' +
                                            f'Valor: %{{y:.2f}} {config["unit"]}<br>' +
                                            'Timestamp: %{x}<br>' +
                                            '<extra></extra>'
                            ))
                        
                        fig.update_layout(
                            title=dict(text=f"{config['title']} em Tempo Real", font=dict(size=20, color='#00d4ff')),
                            xaxis_title="Tempo",
                            yaxis_title=f"{config['title']} ({config['unit']})",
                            template="plotly_dark",
                            hovermode='x unified',
                            height=400,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0.3)',
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        
                        print(f"🔍 DEBUG: Renderizando gráfico com st.plotly_chart")
                        st.plotly_chart(fig, use_container_width=True, key=f"iot_{metric_key}")
                        print(f"🔍 DEBUG: Gráfico renderizado com sucesso")
                        
                        # Estatísticas rápidas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Média", f"{metric_df['value'].mean():.2f} {config['unit']}")
                        with col2:
                            st.metric("Mínimo", f"{metric_df['value'].min():.2f} {config['unit']}")
                        with col3:
                            st.metric("Máximo", f"{metric_df['value'].max():.2f} {config['unit']}")
                        
                        st.markdown("---")
            
            elif role == "ROLE_IA":
                st.subheader("🤖 Monitoramento de Modelos de IA")
                
                # Definir métricas IA
                ia_metrics = {
                    'ml.prediction.confidence': {'icon': '🎯', 'title': 'Confiança do Modelo', 'unit': '', 'color': '#A8E6CF'},
                    'ml.model.drift': {'icon': '📊', 'title': 'Model Drift', 'unit': '', 'color': '#FFD3B6'},
                    'ml.inference.duration': {'icon': '⚡', 'title': 'Tempo de Inferência', 'unit': 'ms', 'color': '#FFAAA5'}
                }
                
                for metric_key, config in ia_metrics.items():
                    metric_df = df[df['metric_name'] == metric_key]
                    if not metric_df.empty:
                        st.markdown(f"### {config['icon']} {config['title']}")
                        
                        fig = go.Figure()
                        for service in metric_df['service_name'].unique():
                            service_data = metric_df[metric_df['service_name'] == service].sort_values('timestamp')
                            fig.add_trace(go.Scatter(
                                x=service_data['timestamp'],
                                y=service_data['value'],
                                mode='lines+markers',
                                name=service,
                                line=dict(width=3, color=config['color']),
                                marker=dict(size=8),
                                hovertemplate=f'<b>{config["title"]}</b><br>' +
                                            f'Valor: %{{y:.2f}} {config["unit"]}<br>' +
                                            'Modelo: %{fullData.name}<br>' +
                                            'Timestamp: %{x}<br>' +
                                            '<extra></extra>'
                            ))
                        
                        fig.update_layout(
                            title=dict(text=f"{config['title']} - Modelos ML", font=dict(size=20, color='#00d4ff')),
                            xaxis_title="Tempo",
                            yaxis_title=f"{config['title']} ({config['unit']})",
                            template="plotly_dark",
                            hovermode='x unified',
                            height=400,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0.3)',
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        
                        st.plotly_chart(fig, width='stretch')
                        
                        # Estatísticas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Média", f"{metric_df['value'].mean():.2f} {config['unit']}")
                        with col2:
                            st.metric("Mínimo", f"{metric_df['value'].min():.2f} {config['unit']}")
                        with col3:
                            st.metric("Máximo", f"{metric_df['value'].max():.2f} {config['unit']}")
                        
                        st.markdown("---")
            
            elif role == "ROLE_ADMIN":
                st.subheader("👨‍💼 Visão Consolidada - Todos os Times")
                
                # Resumo geral
                col1, col2, col3 = st.columns(3)
                with col1:
                    iot_count = len(df[df['teamTag'] == 'IOT'])
                    st.metric("📊 Métricas IoT", iot_count)
                with col2:
                    ia_count = len(df[df['teamTag'] == 'IA'])
                    st.metric("🤖 Métricas IA", ia_count)
                with col3:
                    st.metric("📈 Total", len(df))
                
                st.markdown("---")
                
                # Tabs para separar IoT e IA
                tab_iot, tab_ia, tab_comparacao = st.tabs(["🔧 Sensores IoT", "🤖 Modelos IA", "📊 Comparação"])
                
                with tab_iot:
                    iot_data = df[df['teamTag'] == 'IOT']
                    if not iot_data.empty:
                        # Métricas IoT individuais (nomes reais do ESP32)
                        iot_metrics = {
                            'temperature': {'title': '🌡️ Temperatura', 'color': '#FF6B6B'},
                            'humidity': {'title': '💧 Umidade', 'color': '#4ECDC4'},
                            'air_quality_ppm': {'title': '☁️ Qualidade do Ar (CO2)', 'color': '#95E1D3'},
                            'luminosity_lux': {'title': '💡 Luminosidade', 'color': '#FFE66D'}
                        }
                        
                        for metric_name, config in iot_metrics.items():
                            metric_data = iot_data[iot_data['metric_name'] == metric_name]
                            if not metric_data.empty:
                                st.markdown(f"### {config['title']}")
                                fig = go.Figure()
                                for service in metric_data['service_name'].unique():
                                    service_data = metric_data[metric_data['service_name'] == service].sort_values('timestamp')
                                    fig.add_trace(go.Scatter(
                                        x=service_data['timestamp'],
                                        y=service_data['value'],
                                        mode='lines',
                                        name=service,
                                        line=dict(width=2, color=config['color'])
                                    ))
                                
                                fig.update_layout(
                                    xaxis_title="Tempo",
                                    yaxis_title="Valor",
                                    template="plotly_dark",
                                    height=350,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0.3)',
                                    showlegend=True
                                )
                                st.plotly_chart(fig, width='stretch')
                    else:
                        st.info("Nenhuma métrica IoT disponível")
                
                with tab_ia:
                    ia_data = df[df['teamTag'] == 'IA']
                    if not ia_data.empty:
                        # Métricas IA individuais (nomes reais enviados)
                        ia_metrics = {
                            'mobile_dashboard_views': {'title': '📱 Visualizações Dashboard', 'color': '#A8E6CF'},
                            'prediction_count': {'title': '🔮 Total de Predições', 'color': '#FFD3B6'},
                            'anomalies_detected': {'title': '⚠️ Anomalias Detectadas', 'color': '#FFAAA5'}
                        }
                        
                        for metric_name, config in ia_metrics.items():
                            metric_data = ia_data[ia_data['metric_name'] == metric_name]
                            if not metric_data.empty:
                                st.markdown(f"### {config['title']}")
                                fig = go.Figure()
                                for service in metric_data['service_name'].unique():
                                    service_data = metric_data[metric_data['service_name'] == service].sort_values('timestamp')
                                    fig.add_trace(go.Scatter(
                                        x=service_data['timestamp'],
                                        y=service_data['value'],
                                        mode='lines',
                                        name=service,
                                        line=dict(width=2, color=config['color'])
                                    ))
                                
                                fig.update_layout(
                                    xaxis_title="Tempo",
                                    yaxis_title="Valor",
                                    template="plotly_dark",
                                    height=350,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0.3)',
                                    showlegend=True
                                )
                                st.plotly_chart(fig, width='stretch')
                    else:
                        st.info("Nenhuma métrica IA disponível")
                
                with tab_comparacao:
                    st.markdown("### 📊 Visão Geral do Sistema")
                    
                    # Gráfico de pizza - distribuição por team
                    team_counts = df.groupby('teamTag').size()
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=team_counts.index,
                        values=team_counts.values,
                        marker=dict(colors=['#FF6B6B', '#4ECDC4'])
                    )])
                    fig_pie.update_layout(
                        title="Distribuição de Métricas por Time",
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_pie, width='stretch')
                    
                    # Timeline de todas as métricas
                    st.markdown("### ⏱️ Timeline Completa")
                    fig_timeline = go.Figure()
                    for team in df['teamTag'].unique():
                        team_data = df[df['teamTag'] == team]
                        fig_timeline.add_trace(go.Scatter(
                            x=team_data['timestamp'],
                            y=team_data['value'],
                            mode='markers',
                            name=team,
                            marker=dict(size=5)
                        ))
                    
                    fig_timeline.update_layout(
                        title="Todas as Métricas ao Longo do Tempo",
                        xaxis_title="Tempo",
                        yaxis_title="Valor",
                        template="plotly_dark",
                        height=500,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0.3)'
                    )
                    st.plotly_chart(fig_timeline, width='stretch')
            

with tab2:
    if not traces_data:
        st.info("ℹ️ Nenhum trace capturado. Execute operações na aplicação.")
    else:
        # O collector retorna dados já processados do SQLite
        # Formato: [{"timestamp": "...", "trace_id": "...", "span_id": "...", "service_name": "...", "operation_name": "...", "duration_ms": 123, "attributes": "{}"}]
        
        # Agrupar por team extraindo dos attributes
        traces_by_team = {"IA": [], "IOT": [], "UNKNOWN": []}
        for trace in traces_data:
            try:
                attributes = json.loads(trace.get('attributes', '{}'))
                team = attributes.get('team', 'UNKNOWN')
                traces_by_team[team].append(trace)
            except:
                traces_by_team['UNKNOWN'].append(trace)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Traces", len(traces_data))
        with col2:
            st.metric("IA Traces", len(traces_by_team.get('IA', [])))
        with col3:
            st.metric("IOT Traces", len(traces_by_team.get('IOT', [])))
        
        # Mostrar tabela
        st.subheader("🔍 Traces Capturados")
        df_display = pd.DataFrame([
            {
                'Trace ID': t.get('trace_id', 'N/A')[:16] + '...',
                'Operação': t.get('operation_name', 'N/A'),
                'Serviço': t.get('service_name', 'N/A'),
                'Duração (ms)': f"{float(t.get('duration_ms', 0)):.2f}",
                'Timestamp': t.get('timestamp', 'N/A')[:19]
            }
            for t in traces_data[:50]
        ])
        st.dataframe(df_display, use_container_width=True)
        
        if show_raw_data:
            with st.expander("🔍 Dados Brutos - Traces"):
                for t in traces_data[:5]:
                    st.json(t)

with tab3:
    if not logs_data:
        st.info("ℹ️ Nenhum log capturado. Verifique a configuração do logback.")
    else:
        # O collector retorna dados já processados do SQLite
        # Formato: [{"timestamp": "...", "service_name": "...", "severity_text": "INFO", "body": "...", "attributes": "{}"}]
        
        # Agrupar por team e severidade
        logs_by_team = {"IA": [], "IOT": [], "UNKNOWN": []}
        logs_by_severity = {"INFO": 0, "WARN": 0, "ERROR": 0}
        
        for log in logs_data:
            try:
                attributes = json.loads(log.get('attributes', '{}'))
                team = attributes.get('team', 'UNKNOWN')
                logs_by_team[team].append(log)
                
                severity = log.get('severity_text', 'INFO')
                if severity in logs_by_severity:
                    logs_by_severity[severity] += 1
            except:
                logs_by_team['UNKNOWN'].append(log)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Logs", len(logs_data))
        with col2:
            st.metric("🔵 INFO", logs_by_severity['INFO'])
        with col3:
            st.metric("🟡 WARN", logs_by_severity['WARN'])
        with col4:
            st.metric("🔴 ERROR", logs_by_severity['ERROR'])
        
        # Filtro de severidade
        severity_filter = st.multiselect(
            "Filtrar por Severidade",
            ["INFO", "WARN", "ERROR"],
            default=["INFO", "WARN", "ERROR"]
        )
        
        filtered_logs = [l for l in logs_data if l.get('severity_text') in severity_filter]
        
        # Mostrar logs com cores
        st.subheader("📄 Logs do Sistema")
        
        for log in filtered_logs[:100]:
            severity = log.get('severity_text', 'INFO')
            severity_colors = {
                'INFO': '#4ECDC4',
                'WARN': '#FFE66D',
                'ERROR': '#FF6B6B'
            }
            severity_icons = {
                'INFO': '🔵',
                'WARN': '🟡',
                'ERROR': '🔴'
            }
            
            color = severity_colors.get(severity, '#8b92a8')
            icon = severity_icons.get(severity, 'ℹ️')
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); 
                        border-left: 4px solid {color}; 
                        border-radius: 8px; 
                        padding: 0.8rem; 
                        margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem;">
                    <span>{icon}</span>
                    <strong style="color: {color};">{severity}</strong>
                    <span style="color: #8b92a8; margin-left: auto; font-size: 0.9rem;">
                        {log.get('service_name', 'N/A')} | {log.get('timestamp', 'N/A')[:19]}
                    </span>
                </div>
                <p style="margin: 0; color: white; font-family: monospace; font-size: 0.9rem;">
                    {log.get('body', 'Sem mensagem')}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if show_raw_data:
            with st.expander("🔍 Dados Brutos - Logs"):
                for l in filtered_logs[:10]:
                    st.json(l)

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
