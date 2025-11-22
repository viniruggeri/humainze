#!/usr/bin/env python3
"""
Script de teste para injetar telemetria no backend Java
Gera traces, logs e métricas chamando os endpoints REST
"""

import requests
import time
import json
from datetime import datetime

# Configurações
JAVA_BASE_URL = "http://localhost:8081"
API_KEYS = {
    "admin": "chave-admin",
    "ia": "chave-ia", 
    "iot": "chave-iot"
}

class JavaTester:
    def __init__(self):
        self.tokens = {}
        self.session = requests.Session()
        
    def authenticate(self, role="ia"):
        """Gera token JWT via API Key"""
        print(f"\n🔐 Autenticando como {role.upper()}...")
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": API_KEYS[role]}
            )
            response.raise_for_status()
            token = response.json()["token"]
            self.tokens[role] = token
            print(f"✅ Token obtido: {token[:30]}...")
            return token
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return None
    
    def test_teams_endpoints(self):
        """Testa endpoints de Teams (requer autenticação Admin)"""
        print("\n📋 Testando endpoints de Teams...")
        
        # Autenticar com admin
        token = self.tokens.get("admin") or self.authenticate("admin")
        if not token:
            print("⚠️  Pulando testes de teams (sem autenticação)")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Criar time
        team_data = {
            "name": f"Team Teste {datetime.now().strftime('%H:%M:%S')}",
            "teamTag": f"TEST_{int(time.time())}",
            "description": "Time criado para teste de telemetria"
        }
        
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/teams",
                json=team_data,
                headers=headers
            )
            response.raise_for_status()
            team = response.json()
            team_id = team["id"]
            print(f"✅ Time criado - ID: {team_id}, Tag: {team['teamTag']}")
            
            # Listar times
            response = self.session.get(f"{JAVA_BASE_URL}/teams", headers=headers)
            teams = response.json()
            print(f"✅ Listados {len(teams)} times")
            
            # Buscar time específico
            response = self.session.get(f"{JAVA_BASE_URL}/teams/{team_id}", headers=headers)
            team_detail = response.json()
            print(f"✅ Detalhes do time: {team_detail['name']}")
            
            # Adicionar role
            response = self.session.post(
                f"{JAVA_BASE_URL}/teams/{team_id}/roles",
                json={"roleName": "ROLE_IA"},
                headers=headers
            )
            print(f"✅ Role adicionada ao time")
            
            # Atualizar time
            update_data = {
                "name": team_data["name"] + " (Atualizado)",
                "teamTag": team_data["teamTag"],
                "description": "Descrição atualizada"
            }
            response = self.session.patch(
                f"{JAVA_BASE_URL}/teams/{team_id}",
                json=update_data,
                headers=headers
            )
            print(f"✅ Time atualizado")
            
            # Deletar time
            response = self.session.delete(f"{JAVA_BASE_URL}/teams/{team_id}", headers=headers)
            print(f"✅ Time removido")
            
        except Exception as e:
            print(f"❌ Erro nos testes de Teams: {e}")
    
    def test_alerts_endpoints(self):
        """Testa endpoints de Alertas"""
        print("\n🚨 Testando endpoints de Alertas...")
        
        # Autenticar com admin
        token = self.tokens.get("admin") or self.authenticate("admin")
        if not token:
            print("⚠️  Pulando testes de alertas (sem autenticação)")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Criar alerta
        alert_data = {
            "team": "TEAM_IA",
            "message": f"Teste de alerta cognitivo - {datetime.now().isoformat()}",
            "severity": "HIGH",
            "source": "teste_automatizado"
        }
        
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/alerts",
                json=alert_data,
                headers=headers
            )
            response.raise_for_status()
            alert = response.json()
            alert_id = alert["id"]
            print(f"✅ Alerta criado - ID: {alert_id}, Severity: {alert['severity']}")
            
            # Listar alertas
            response = self.session.get(
                f"{JAVA_BASE_URL}/alerts",
                headers=headers
            )
            alerts = response.json()
            print(f"✅ Listados alertas: {alerts.get('totalElements', 0)} no total")
            
            # Resolver alerta
            response = self.session.put(
                f"{JAVA_BASE_URL}/alerts/{alert_id}/resolve",
                headers=headers
            )
            resolved = response.json()
            print(f"✅ Alerta resolvido - Status: {resolved.get('status', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Erro nos testes de Alertas: {e}")
    
    def test_multiple_authentications(self):
        """Gera múltiplas autenticações para criar traces"""
        print("\n🔄 Gerando múltiplas autenticações...")
        
        for i in range(5):
            for role in ["admin", "ia", "iot"]:
                self.authenticate(role)
                time.sleep(0.5)  # Pausa entre requisições
        
        print("✅ Autenticações múltiplas concluídas")
    
    def test_error_scenarios(self):
        """Testa cenários de erro para gerar logs"""
        print("\n⚠️  Testando cenários de erro...")
        
        # API Key inválida
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": "chave-invalida"}
            )
            print(f"✅ Erro 401 esperado: {response.status_code}")
        except:
            pass
        
        # Team inexistente
        try:
            response = self.session.get(f"{JAVA_BASE_URL}/teams/99999")
            print(f"✅ Erro 404 esperado: {response.status_code}")
        except:
            pass
        
        # Criar team com dados inválidos
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/teams",
                json={"name": ""}  # Nome vazio
            )
            print(f"✅ Erro de validação esperado: {response.status_code}")
        except:
            pass
    
    def run_full_test(self):
        """Executa bateria completa de testes"""
        print("=" * 60)
        print("🚀 INICIANDO TESTES DE TELEMETRIA")
        print("=" * 60)
        
        # 1. Autenticações
        self.authenticate("admin")
        self.authenticate("ia")
        self.authenticate("iot")
        
        # 2. Testes de Teams
        self.test_teams_endpoints()
        
        # 3. Testes de Alerts
        self.test_alerts_endpoints()
        
        # 4. Múltiplas autenticações
        self.test_multiple_authentications()
        
        # 5. Cenários de erro
        self.test_error_scenarios()
        
        print("\n" + "=" * 60)
        print("✅ TESTES CONCLUÍDOS")
        print("=" * 60)
        print("\n📊 Verifique a dashboard em http://localhost:8501")
        print("   - Aba Metrics: Métricas HTTP, JVM, etc")
        print("   - Aba Traces: Spans de 'generate-jwt-token', operações CRUD")
        print("   - Aba Logs: Logs de autenticação, erros, operações")


if __name__ == "__main__":
    tester = JavaTester()
    
    print("\n⏳ Aguardando backend Java estar disponível...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{JAVA_BASE_URL}/actuator/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend Java está online!")
                break
        except:
            pass
        
        if i == max_retries - 1:
            print("❌ Backend Java não está respondendo. Inicie com: ./mvnw spring-boot:run")
            exit(1)
        
        print(f"   Tentativa {i+1}/{max_retries}...")
        time.sleep(2)
    
    tester.run_full_test()
