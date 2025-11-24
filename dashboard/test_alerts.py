#!/usr/bin/env python3
"""
Script de teste para criar alertas e visualizar no dashboard
"""

import requests
import time
from datetime import datetime

BACKEND_URL = "http://localhost:8080"

def login(api_key):
    """Autentica e retorna token"""
    response = requests.post(
        f"{BACKEND_URL}/auth/token",
        headers={"X-API-KEY": api_key}
    )
    if response.status_code == 200:
        return response.json()["token"]
    return None

def create_alert(token, team_tag, alert_type, message):
    """Cria um alerta"""
    response = requests.post(
        f"{BACKEND_URL}/alerts",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "teamTag": team_tag,
            "type": alert_type,
            "message": message
        }
    )
    return response.status_code == 201

def count_unresolved(token, team=None):
    """Conta alertas não resolvidos"""
    params = {"team": team} if team else {}
    response = requests.get(
        f"{BACKEND_URL}/alerts/unresolved/count",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )
    if response.status_code == 200:
        return response.json()
    return 0

def list_unresolved(token, team=None):
    """Lista alertas não resolvidos"""
    params = {"team": team, "size": 10} if team else {"size": 10}
    response = requests.get(
        f"{BACKEND_URL}/alerts/unresolved",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )
    if response.status_code == 200:
        return response.json()
    return {"content": [], "totalElements": 0}

def list_all_alerts(token, team=None, size=20):
    """Lista todos os alertas (incluindo resolvidos)"""
    params = {"size": size}
    if team:
        params["team"] = team
    
    response = requests.get(
        f"{BACKEND_URL}/alerts",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )
    if response.status_code == 200:
        return response.json()
    return {"content": [], "totalElements": 0}

def resolve_alert(token, alert_id):
    """Resolve um alerta"""
    response = requests.put(
        f"{BACKEND_URL}/alerts/{alert_id}/resolve",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.status_code == 200

def main():
    print("🧪 Teste de Sistema de Alertas")
    print("=" * 60)
    
    # Login como IA
    print("\n1️⃣ Autenticando como IA...")
    token = login("chave-ia")
    if not token:
        print("❌ Falha na autenticação")
        return
    print("✅ Token obtido")
    
    # Criar alguns alertas de teste
    print("\n2️⃣ Criando alertas de teste...")
    
    alerts_to_create = [
        ("IA", "DRIFT", "Detectado drift no modelo de predição - Acurácia caiu de 95% para 78%"),
        ("IA", "MODEL_ERROR", "Erro crítico no pipeline de inferência - Timeout em chamadas ao modelo"),
        ("IOT", "SERVICE_DOWN", "Serviço de coleta de dados IoT não está respondendo"),
        ("IA", "DRIFT", "Distribuição de features alterada significativamente nos últimos dados"),
    ]
    
    created = 0
    for team, alert_type, message in alerts_to_create:
        if create_alert(token, team, alert_type, message):
            print(f"   ✅ Alerta criado: {alert_type} - {team}")
            created += 1
        else:
            print(f"   ❌ Falha ao criar: {alert_type} - {team}")
        time.sleep(0.5)
    
    print(f"\n✅ {created}/{len(alerts_to_create)} alertas criados com sucesso")
    
    # Contar alertas não resolvidos
    print("\n3️⃣ Verificando alertas não resolvidos...")
    count_all = count_unresolved(token)
    count_ia = count_unresolved(token, "IA")
    count_iot = count_unresolved(token, "IOT")
    
    print(f"   📊 Total geral: {count_all} alerta(s)")
    print(f"   🟣 Team IA: {count_ia} alerta(s)")
    print(f"   🟢 Team IOT: {count_iot} alerta(s)")
    
    # Listar alertas da IA
    print("\n4️⃣ Listando alertas do Team IA...")
    alerts_data = list_unresolved(token, "IA")
    
    if alerts_data.get("content"):
        print(f"   Total: {alerts_data['totalElements']} alerta(s)")
        for alert in alerts_data["content"][:5]:  # Primeiros 5
            timestamp = alert.get('timestamp', 'N/A')
            print(f"   🔸 [{alert['type']}] {alert['message'][:60]}...")
    else:
        print("   ℹ️ Nenhum alerta encontrado")
    
    # Testar resolução de alerta
    print("\n5️⃣ Testando resolução de alerta...")
    if alerts_data.get("content") and len(alerts_data["content"]) > 0:
        alert_to_resolve = alerts_data["content"][0]
        alert_id = alert_to_resolve.get("id")
        
        print(f"   Resolvendo alerta ID {alert_id}...")
        if resolve_alert(token, alert_id):
            print(f"   ✅ Alerta {alert_id} resolvido com sucesso!")
        else:
            print(f"   ❌ Falha ao resolver alerta {alert_id}")
        
        # Verificar contagem após resolver
        time.sleep(0.5)
        new_count = count_unresolved(token, "IA")
        print(f"   📊 Nova contagem Team IA: {new_count} alerta(s)")
    else:
        print("   ⏩ Nenhum alerta para resolver")
    
    # Listar histórico completo
    print("\n6️⃣ Listando histórico completo...")
    all_alerts = list_all_alerts(token, size=50)
    
    if all_alerts.get("content"):
        resolved_count = sum(1 for a in all_alerts["content"] if a.get("resolved", False))
        active_count = sum(1 for a in all_alerts["content"] if not a.get("resolved", False))
        
        print(f"   📊 Total no histórico: {all_alerts['totalElements']} alerta(s)")
        print(f"   ✅ Resolvidos: {resolved_count}")
        print(f"   🔴 Ativos: {active_count}")
        
        # Contar por tipo
        types_count = {}
        for alert in all_alerts["content"]:
            alert_type = alert.get("type", "UNKNOWN")
            types_count[alert_type] = types_count.get(alert_type, 0) + 1
        
        print(f"   📈 Por tipo:")
        for alert_type, count in types_count.items():
            print(f"      • {alert_type}: {count}")
    else:
        print("   ℹ️ Nenhum alerta no histórico")
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
    print("\n📊 Agora você pode:")
    print("   1. Abrir o dashboard: http://localhost:8501")
    print("   2. Fazer login com 'chave-ia'")
    print("   3. Ver o banner vermelho com a contagem de alertas")
    print("   4. Clicar em 'Ver Alertas Detalhados' para expandir")
    print("   5. Ir na aba '🎯 Alertas' para gerenciar")
    print("   6. Na sub-aba '✅ Todos' ver o histórico completo com:")
    print("      • Filtros por status (Todos/Não Resolvidos/Resolvidos)")
    print("      • Filtros por tipo (DRIFT/MODEL_ERROR/SERVICE_DOWN)")
    print("      • Paginação com 10/20/50/100 itens por página")
    print("      • Navegação entre páginas (Primeira/Anterior/Próxima/Última)")
    print("   7. Ativar 'Auto-refresh' na sidebar para polling automático")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
