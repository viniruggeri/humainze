#!/usr/bin/env python3
"""
Script MASTER para popular todo o banco de dados
Executa IoT e IA em paralelo para velocidade máxima
"""

import subprocess
import sys
import time
from datetime import datetime

print("=" * 80)
print("HUMAINZE - POPULATE DATABASE")
print("=" * 80)
print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Verificar se os scripts existem
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
iot_script = os.path.join(script_dir, "populate_iot_data.py")
ia_script = os.path.join(script_dir, "populate_ia_data.py")

if not os.path.exists(iot_script):
    print(f"[ERRO] Script IoT nao encontrado: {iot_script}")
    sys.exit(1)

if not os.path.exists(ia_script):
    print(f"[ERRO] Script IA nao encontrado: {ia_script}")
    sys.exit(1)

print("Executando scripts de populacao de dados...")
print()

# Executar IoT em paralelo
print("Iniciando populacao IoT (250 metricas)...")
iot_process = subprocess.Popen(
    [sys.executable, iot_script],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Pequeno delay para não iniciar exatamente ao mesmo tempo
time.sleep(1)

# Executar IA em paralelo
print("Iniciando populacao IA (250 predicoes)...")
ia_process = subprocess.Popen(
    [sys.executable, ia_script],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

print()
print("Aguardando conclusao (aprox. 30-60 segundos)...")
print()

# Aguardar conclusão e capturar saída
iot_output, _ = iot_process.communicate()
ia_output, _ = ia_process.communicate()

# Exibir resultados
print("=" * 80)
print("RESULTADOS - IoT")
print("=" * 80)
for line in iot_output.split('\n'):
    if line.strip():
        print(line)

print()
print("=" * 80)
print("RESULTADOS - IA")
print("=" * 80)
for line in ia_output.split('\n'):
    if line.strip():
        print(line)

print()
print("=" * 80)
print("POPULACAO COMPLETA")
print("=" * 80)
print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Códigos de saída
iot_code = iot_process.returncode
ia_code = ia_process.returncode

if iot_code == 0 and ia_code == 0:
    print("Todos os dados foram inseridos com sucesso!")
    print()
    print("Proximos passos:")
    print("   1. Acesse o dashboard: http://172.161.94.218:8501")
    print("   2. Faca login com: chave-iot ou chave-ia")
    print("   3. Visualize as metricas em tempo real")
    sys.exit(0)
else:
    print("Alguns erros ocorreram durante a populacao")
    print(f"   IoT exit code: {iot_code}")
    print(f"   IA exit code: {ia_code}")
    sys.exit(1)
