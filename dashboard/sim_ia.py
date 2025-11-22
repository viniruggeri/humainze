#!/usr/bin/env python3
"""
Simulador de Sistema IA - ROLE_IA
Testa RBAC e gera telemetria específica de IA
"""

import requests
import time
import random
from datetime import datetime

JAVA_BASE_URL = "http://localhost:8081"
API_KEY_IA = "chave-ia"

class IASimulator:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        
    def authenticate(self):
        """Autentica como ROLE_IA"""
        print("\n🤖 [IA] Autenticando sistema IA...")
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": API_KEY_IA}
            )
            response.raise_for_status()
            self.token = response.json()["token"]
            print(f"✅ [IA] Token obtido com sucesso")
            print(f"   Token: {self.token[:40]}...")
            return True
        except Exception as e:
            print(f"❌ [IA] Erro na autenticação: {e}")
            return False
    
    def test_rbac_allowed(self):
        """Testa endpoints permitidos para ROLE_IA"""
        print("\n✅ [IA] Testando endpoints PERMITIDOS para ROLE_IA...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. Listar alertas (PERMITIDO)
        try:
            response = self.session.get(
                f"{JAVA_BASE_URL}/alerts",
                headers=headers
            )
            response.raise_for_status()
            print(f"   ✅ GET /alerts - Status {response.status_code} (PERMITIDO)")
        except Exception as e:
            print(f"   ❌ GET /alerts - ERRO: {e}")
        
        # 2. Criar alerta cognitivo (PERMITIDO)
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/alerts",
                json={
                    "teamTag": "IA",
                    "type": "ANOMALY_DETECTED",
                    "message": f"Anomalia detectada no modelo de IA - {datetime.now().isoformat()}"
                },
                headers=headers
            )
            response.raise_for_status()
            alert = response.json()
            print(f"   ✅ POST /alerts - Alerta criado ID: {alert.get('id')} (PERMITIDO)")
            
            # 3. Resolver alerta (PERMITIDO)
            alert_id = alert.get('id')
            response = self.session.put(
                f"{JAVA_BASE_URL}/alerts/{alert_id}/resolve",
                headers=headers
            )
            response.raise_for_status()
            print(f"   ✅ PUT /alerts/{alert_id}/resolve - Status {response.status_code} (PERMITIDO)")
            
        except Exception as e:
            print(f"   ❌ POST /alerts - ERRO: {e}")
    
    def test_rbac_denied(self):
        """Testa endpoints NEGADOS para ROLE_IA"""
        print("\n🚫 [IA] Testando endpoints NEGADOS para ROLE_IA...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. Criar team (NEGADO - precisa ADMIN)
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/teams",
                json={
                    "name": "Tentativa IA",
                    "teamTag": "TESTE_IA",
                    "description": "Deve ser negado"
                },
                headers=headers
            )
            if response.status_code == 403:
                print(f"   ✅ POST /teams - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ POST /teams - Status {response.status_code} (DEVERIA SER 403)")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"   ✅ POST /teams - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ POST /teams - ERRO: {e}")
        
        # 2. Admin endpoints (NEGADO)
        try:
            response = self.session.get(
                f"{JAVA_BASE_URL}/admin/stats",
                headers=headers
            )
            if response.status_code == 403:
                print(f"   ✅ GET /admin/stats - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ GET /admin/stats - Status {response.status_code} (DEVERIA SER 403)")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"   ✅ GET /admin/stats - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ ERRO: {e}")
    
    def generate_ia_telemetry(self):
        """Gera telemetria específica de sistemas IA"""
        print("\n📊 [IA] Gerando telemetria de sistemas IA...")
        
        ia_scenarios = [
            {"team": "IA", "type": "MODEL_DRIFT", "message": "Drift detectado no modelo de previsão de churn - acurácia caiu 5%"},
            {"team": "IA", "type": "ANOMALY_DETECTED", "message": "Padrão anômalo identificado em 127 registros - possível data leak"},
            {"team": "IA", "type": "PERFORMANCE_DEGRADATION", "message": "Latência de inferência aumentou 40ms - verificar GPU"},
            {"team": "IA", "type": "BIAS_DETECTED", "message": "Viés algorítmico detectado em previsões demográficas"},
            {"team": "IA", "type": "TRAINING_COMPLETED", "message": "Treinamento epoch 50/50 concluído - Loss: 0.023"},
        ]
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        for i, scenario in enumerate(ia_scenarios):
            try:
                response = self.session.post(
                    f"{JAVA_BASE_URL}/alerts",
                    json=scenario,
                    headers=headers
                )
                response.raise_for_status()
                alert = response.json()
                print(f"   ✅ Alerta IA #{i+1} criado - Type: {scenario['type']}")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Erro ao criar alerta: {e}")
    
    def simulate_ia_operations(self, duration_seconds=30):
        """Simula operações contínuas de IA"""
        print(f"\n🔄 [IA] Simulando operações de IA por {duration_seconds} segundos...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        start_time = time.time()
        operation_count = 0
        
        while (time.time() - start_time) < duration_seconds:
            operation_type = random.choice([
                "Model Inference",
                "Data Validation",
                "Feature Engineering",
                "Hyperparameter Tuning",
                "Model Evaluation"
            ])
            
            accuracy = round(random.uniform(0.85, 0.99), 3)
            latency_ms = round(random.uniform(10, 150), 2)
            
            message = f"{operation_type} - Accuracy: {accuracy}, Latency: {latency_ms}ms"
            
            try:
                self.session.post(
                    f"{JAVA_BASE_URL}/alerts",
                    json={
                        "teamTag": "IA",
                        "type": "TRAINING_COMPLETED",
                        "message": message
                    },
                    headers=headers
                )
                operation_count += 1
                print(f"   [{operation_count}] {operation_type} - Acc: {accuracy}")
                time.sleep(random.uniform(1, 3))
            except:
                pass
        
        print(f"✅ [IA] {operation_count} operações de IA simuladas")
    
    def run_full_simulation(self):
        """Executa simulação completa do sistema IA"""
        print("=" * 70)
        print("🤖 SIMULADOR DE SISTEMA IA - ROLE_IA")
        print("=" * 70)
        
        if not self.authenticate():
            print("\n❌ Falha na autenticação. Encerrando simulação.")
            return
        
        # 1. Testar RBAC - Endpoints permitidos
        self.test_rbac_allowed()
        
        # 2. Testar RBAC - Endpoints negados
        self.test_rbac_denied()
        
        # 3. Gerar telemetria específica de IA
        self.generate_ia_telemetry()
        
        # 4. Simular operações contínuas
        self.simulate_ia_operations(duration_seconds=20)
        
        print("\n" + "=" * 70)
        print("✅ SIMULAÇÃO IA CONCLUÍDA")
        print("=" * 70)
        print("\n📊 Verifique a dashboard em http://localhost:8501")
        print("   - Filtrar por ROLE_IA para ver dados específicos")
        print("   - Alertas de Model Drift, Anomalias, Bias Detection")
        print("   - Logs de autenticação e operações do sistema IA")


if __name__ == "__main__":
    simulator = IASimulator()
    
    print("\n⏳ Verificando backend Java...")
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{JAVA_BASE_URL}/actuator/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend Java online!")
                break
        except:
            pass
        
        if i == max_retries - 1:
            print("❌ Backend Java offline. Inicie com: ./mvnw spring-boot:run")
            exit(1)
        
        time.sleep(2)
    
    simulator.run_full_simulation()
