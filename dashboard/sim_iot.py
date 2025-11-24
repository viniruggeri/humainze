#!/usr/bin/env python3
"""
Simulador de Dispositivos IoT - ROLE_IOT
Testa RBAC e gera telemetria de sensores IoT
"""

import requests
import time
import random
import json
from datetime import datetime, timezone

JAVA_BASE_URL = "http://localhost:8080"
API_KEY_IOT = "chave-iot"

class IOTSimulator:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        self.devices = ["SENSOR_001", "SENSOR_002", "SENSOR_003", "GATEWAY_A", "GATEWAY_B"]
        
    def authenticate(self):
        """Autentica como ROLE_IOT"""
        print("\n📡 [IOT] Autenticando dispositivos IoT...")
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/auth/token",
                headers={"X-API-KEY": API_KEY_IOT}
            )
            response.raise_for_status()
            self.token = response.json()["token"]
            print(f"✅ [IOT] Token obtido com sucesso")
            print(f"   Token: {self.token[:40]}...")
            return True
        except Exception as e:
            print(f"❌ [IOT] Erro na autenticação: {e}")
            return False
    
    def test_rbac_denied(self):
        """Testa endpoints NEGADOS para ROLE_IOT"""
        print("\n🚫 [IOT] Testando endpoints NEGADOS para ROLE_IOT...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. Criar alerta (NEGADO - apenas IA e ADMIN)
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/alerts",
                json={
                    "teamTag": "IOT",
                    "type": "ANOMALY_DETECTED",
                    "message": "Tentativa IOT"
                },
                headers=headers
            )
            if response.status_code == 403:
                print(f"   ✅ POST /alerts - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ POST /alerts - Status {response.status_code} (DEVERIA SER 403)")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"   ✅ POST /alerts - Status 403 (NEGADO corretamente)")
            else:
                print(f"   ❌ ERRO: {e}")
        
        # 2. Criar team (NEGADO)
        try:
            response = self.session.post(
                f"{JAVA_BASE_URL}/teams",
                json={
                    "name": "Tentativa IOT",
                    "teamTag": "TESTE_IOT",
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
                print(f"   ❌ ERRO: {e}")
        
        # 3. Admin endpoints (NEGADO)
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
    
    def send_sensor_telemetry(self, device_id, sensor_type, value, unit):
        """Envia telemetria de sensor IoT via OTLP"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Mapear sensor_type para metric_name esperado
        metric_map = {
            "Temperature": "temperature",
            "Humidity": "humidity",
            "Pressure": "air_quality_ppm",
            "Light": "luminosity_lux"
        }
        
        metric_name = metric_map.get(sensor_type, sensor_type.lower())
        
        # Formato esperado pelo dashboard
        metrics = [{
            "key": metric_name,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "originModule": "IOT",
            "metadata": {"sensor": device_id, "unit": unit}
        }]
        
        payload = {
            "teamTag": "IOT",
            "timestamp": datetime.utcnow().isoformat(),
            "payloadJson": json.dumps(metrics)
        }
        
        try:
            self.session.post(
                f"{JAVA_BASE_URL}/otel/v1/metrics",
                json=payload,
                headers=headers
            )
            print(f"   📊 {device_id} - {sensor_type}: {value}{unit} [ENVIADO]")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        time.sleep(0.3)
    
    def simulate_temperature_sensors(self):
        """Simula sensores de temperatura"""
        print("\n🌡️  [IOT] Simulando sensores de temperatura...")
        
        for device in self.devices[:3]:  # Primeiros 3 devices são sensores
            temp = round(random.uniform(18.0, 28.0), 2)
            humidity = round(random.uniform(40.0, 70.0), 2)
            
            self.send_sensor_telemetry(device, "Temperature", temp, "°C")
            self.send_sensor_telemetry(device, "Humidity", humidity, "%")
    
    def simulate_gateway_health(self):
        """Simula health check de gateways"""
        print("\n🔌 [IOT] Simulando health check de gateways...")
        
        for gateway in self.devices[3:]:  # Últimos 2 devices são gateways
            uptime_hours = random.randint(1, 720)
            memory_usage = round(random.uniform(30.0, 80.0), 1)
            packet_loss = round(random.uniform(0.0, 2.5), 2)
            
            print(f"   ✅ {gateway} - Uptime: {uptime_hours}h, Memory: {memory_usage}%, PacketLoss: {packet_loss}%")
            time.sleep(0.3)
    
    def simulate_device_alerts(self):
        """Simula alertas de dispositivos IoT"""
        print("\n⚠️  [IOT] Simulando alertas de dispositivos...")
        
        iot_alerts = [
            {"device": "SENSOR_001", "alert": "Bateria baixa - 15% restante"},
            {"device": "SENSOR_002", "alert": "Temperatura acima do limite - 32°C"},
            {"device": "GATEWAY_A", "alert": "Packet loss alto - 5.2%"},
            {"device": "SENSOR_003", "alert": "Conexão instável - 3 reconexões em 5min"},
            {"device": "GATEWAY_B", "alert": "Memória crítica - 95% utilizada"},
        ]
        
        for alert in iot_alerts:
            print(f"   🔴 {alert['device']}: {alert['alert']}")
            time.sleep(0.5)
    
    def simulate_iot_operations(self, duration_seconds=30):
        """Simula operações contínuas de IoT"""
        print(f"\n🔄 [IOT] Simulando operações IoT por {duration_seconds} segundos...")
        
        start_time = time.time()
        reading_count = 0
        
        while (time.time() - start_time) < duration_seconds:
            device = random.choice(self.devices)
            
            if "SENSOR" in device:
                sensor_type = random.choice(["Temperature", "Humidity", "Pressure", "Light"])
                if sensor_type == "Temperature":
                    value = round(random.uniform(15.0, 30.0), 2)
                    unit = "°C"
                elif sensor_type == "Humidity":
                    value = round(random.uniform(30.0, 80.0), 2)
                    unit = "%"
                elif sensor_type == "Pressure":
                    value = round(random.uniform(980.0, 1020.0), 2)
                    unit = "hPa"
                else:  # Light
                    value = round(random.uniform(100.0, 1000.0), 2)
                    unit = "lux"
                
                reading_count += 1
                print(f"   [{reading_count}] {device} - {sensor_type}: {value}{unit}")
            else:  # Gateway
                cpu = round(random.uniform(10.0, 60.0), 1)
                memory = round(random.uniform(30.0, 80.0), 1)
                reading_count += 1
                print(f"   [{reading_count}] {device} - CPU: {cpu}%, Memory: {memory}%")
            
            time.sleep(random.uniform(1, 2.5))
        
        print(f"✅ [IOT] {reading_count} leituras de sensores simuladas")
    
    def run_full_simulation(self):
        """Executa simulação completa do sistema IoT"""
        print("=" * 70)
        print("📡 SIMULADOR DE DISPOSITIVOS IOT - ROLE_IOT")
        print("=" * 70)
        
        if not self.authenticate():
            print("\n❌ Falha na autenticação. Encerrando simulação.")
            return
        
        # 1. Testar RBAC - Endpoints negados
        self.test_rbac_denied()
        
        # 2. Simular sensores de temperatura
        self.simulate_temperature_sensors()
        
        # 3. Simular health de gateways
        self.simulate_gateway_health()
        
        # 4. Simular alertas de dispositivos
        self.simulate_device_alerts()
        
        # 5. Simular operações contínuas
        self.simulate_iot_operations(duration_seconds=25)
        
        print("\n" + "=" * 70)
        print("✅ SIMULAÇÃO IOT CONCLUÍDA")
        print("=" * 70)
        print("\n📊 Verifique a dashboard em http://localhost:8501")
        print("   - Filtrar por ROLE_IOT para ver dados de sensores")
        print("   - Métricas de temperatura, umidade, pressão, luz")
        print("   - Logs de autenticação e operações dos dispositivos")
        print("   - Health checks de gateways IoT")


if __name__ == "__main__":
    simulator = IOTSimulator()
    
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
