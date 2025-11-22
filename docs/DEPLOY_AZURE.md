# 🚀 Deploy no Azure VM - Guia Completo

## Visão Geral

Este guia explica como fazer deploy do **Humainze Backend** e **Dashboard Streamlit** em uma Azure Virtual Machine usando Docker Compose.

## 📋 Pré-requisitos

- Conta Microsoft Azure ativa
- Azure CLI instalado localmente
- Git instalado
- Acesso SSH configurado

## 🏗️ Arquitetura de Deploy

```
┌─────────────────────────────────────────┐
│         Azure VM (Ubuntu 22.04)         │
│  ┌───────────────────────────────────┐  │
│  │   Docker Compose Stack            │  │
│  │                                   │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Backend Java:8080          │  │  │
│  │  │  Spring Boot 3.5            │  │  │
│  │  │  OpenTelemetry              │  │  │
│  │  └─────────────────────────────┘  │  │
│  │                                   │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Dashboard:8501             │  │  │
│  │  │  Streamlit Python           │  │  │
│  │  │  Auto-refresh               │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
         ↓                  ↓
   Oracle FIAP DB      Usuários Web
```

## 🔧 Passo 1: Provisionar VM no Azure

### Via Azure Portal

1. Acesse o [Azure Portal](https://portal.azure.com)
2. Vá em **Virtual Machines** → **Create**
3. Configure:
   - **Subscription:** Sua assinatura
   - **Resource Group:** `humainze-rg` (criar novo)
   - **VM Name:** `humainze-vm`
   - **Region:** Brazil South (ou mais próxima)
   - **Image:** Ubuntu Server 22.04 LTS
   - **Size:** Standard_B2s (2 vCPUs, 4GB RAM)
   - **Authentication:** SSH public key
   - **Username:** `azureuser`

4. Na aba **Networking**, configure:
   - **Public IP:** Enabled
   - **NIC network security group:** Advanced
   - Criar novo NSG e adicionar regras:
     - Port 22 (SSH)
     - Port 8080 (Backend)
     - Port 8501 (Dashboard)

5. Clique em **Review + Create** → **Create**

### Via Azure CLI

```bash
# Login no Azure
az login

# Criar Resource Group
az group create \
  --name humainze-rg \
  --location brazilsouth

# Criar VM
az vm create \
  --resource-group humainze-rg \
  --name humainze-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Abrir portas necessárias
az vm open-port \
  --port 8080 \
  --resource-group humainze-rg \
  --name humainze-vm \
  --priority 1001

az vm open-port \
  --port 8501 \
  --resource-group humainze-rg \
  --name humainze-vm \
  --priority 1002

# Obter IP público
az vm show \
  --resource-group humainze-rg \
  --name humainze-vm \
  --show-details \
  --query publicIps \
  --output tsv
```

**Salve o IP público retornado!**

## 🔐 Passo 2: Conectar via SSH

```bash
# Substituir <IP-PUBLICO> pelo IP obtido
ssh azureuser@<IP-PUBLICO>
```

## 📦 Passo 3: Instalar Docker e Docker Compose

```bash
# Atualizar pacotes
sudo apt update
sudo apt upgrade -y

# Instalar Docker
sudo apt install -y docker.io

# Iniciar e habilitar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version

# Fazer logout e login novamente para aplicar permissões
exit
ssh azureuser@<IP-PUBLICO>
```

## 📥 Passo 4: Clonar Repositório

```bash
# Clonar projeto
git clone https://github.com/viniruggeri/humainze-java.git
cd humainze-java
```

## ⚙️ Passo 5: Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

**Adicionar:**

```env
# Spring Profile
SPRING_PROFILES_ACTIVE=prod

# JWT Configuration
JWT_SECRET=seu-secret-super-seguro-com-minimo-256-bits-para-hs256-algorithm
JWT_ISSUER=humainze-dash
JWT_AUDIENCE=humainze-clients
JWT_EXPIRATION_MINUTES=120

# Database (Oracle FIAP)
SPRING_DATASOURCE_URL=jdbc:oracle:thin:@oracle.fiap.com.br:1521/orcl
SPRING_DATASOURCE_USERNAME=rm560593
SPRING_DATASOURCE_PASSWORD=100225

# JPA Settings
SPRING_JPA_HIBERNATE_DDL_AUTO=update
SPRING_JPA_SHOW_SQL=false

# Seed Data
SEED_ENABLED=true

# OpenTelemetry (opcional - se tiver SigNoz)
OTEL_EXPORTER_OTLP_ENDPOINT=http://signoz:4318
OTEL_SERVICE_NAME=humainze-backend

# Dashboard
DASHBOARD_BACKEND_URL=http://backend:8080
```

**Salvar:** Ctrl+O → Enter → Ctrl+X

## 🐳 Passo 6: Criar docker-compose.yml

```bash
nano docker-compose.yml
```

**Adicionar:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: humainze-backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=${SPRING_PROFILES_ACTIVE}
      - JWT_SECRET=${JWT_SECRET}
      - JWT_ISSUER=${JWT_ISSUER}
      - JWT_AUDIENCE=${JWT_AUDIENCE}
      - JWT_EXPIRATION_MINUTES=${JWT_EXPIRATION_MINUTES}
      - SPRING_DATASOURCE_URL=${SPRING_DATASOURCE_URL}
      - SPRING_DATASOURCE_USERNAME=${SPRING_DATASOURCE_USERNAME}
      - SPRING_DATASOURCE_PASSWORD=${SPRING_DATASOURCE_PASSWORD}
      - SPRING_JPA_HIBERNATE_DDL_AUTO=${SPRING_JPA_HIBERNATE_DDL_AUTO}
      - SPRING_JPA_SHOW_SQL=${SPRING_JPA_SHOW_SQL}
      - SEED_ENABLED=${SEED_ENABLED}
      - OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT}
      - OTEL_SERVICE_NAME=${OTEL_SERVICE_NAME}
    networks:
      - humainze-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  dashboard:
    build:
      context: ./dashboard
      dockerfile: Dockerfile
    container_name: humainze-dashboard
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8080
    depends_on:
      - backend
    networks:
      - humainze-network
    restart: unless-stopped

networks:
  humainze-network:
    driver: bridge
```

**Salvar:** Ctrl+O → Enter → Ctrl+X

## 🏗️ Passo 7: Criar Dockerfiles

### Backend Dockerfile

```bash
nano Dockerfile
```

**Adicionar:**

```dockerfile
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Dashboard Dockerfile

```bash
mkdir -p dashboard
nano dashboard/Dockerfile
```

**Adicionar:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Criar requirements.txt:**

```bash
nano dashboard/requirements.txt
```

**Adicionar:**

```
streamlit==1.31.0
requests==2.31.0
pandas==2.1.4
plotly==5.18.0
```

## 🔨 Passo 8: Build Local (antes de subir na VM)

**⚠️ Este passo deve ser feito na sua máquina local, não na VM!**

```bash
# Na sua máquina local, dentro do diretório do projeto
./mvnw clean package -DskipTests

# Verificar se o JAR foi gerado
ls -lh target/*.jar
```

**Agora copie o JAR para a VM:**

```bash
# Na sua máquina local
scp target/humainze-dash-0.0.1-SNAPSHOT.jar azureuser@<IP-PUBLICO>:/home/azureuser/humainze-java/target/
```

## 🚀 Passo 9: Subir os Containers

```bash
# Na VM, dentro do diretório humainze-java
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f backend
docker-compose logs -f dashboard
```

**Aguarde ~2-3 minutos para o backend inicializar completamente.**

## ✅ Passo 10: Verificar Deploy

### Testar Backend

```bash
# Health check
curl http://localhost:8080/actuator/health

# Swagger UI (abra no navegador)
http://<IP-PUBLICO>:8080/swagger-ui.html
```

### Testar Dashboard

```bash
# Abra no navegador
http://<IP-PUBLICO>:8501
```

### Testar Autenticação

```bash
# Login como IA
curl -X POST http://<IP-PUBLICO>:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"team":"IA","secret":"ia-secret"}'
```

**Resposta esperada:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "team": "IA",
  "roles": ["ROLE_IA"]
}
```

## 📊 Monitoramento

### Ver Logs em Tempo Real

```bash
# Backend
docker-compose logs -f backend

# Dashboard
docker-compose logs -f dashboard

# Ambos
docker-compose logs -f
```

### Estatísticas de Containers

```bash
docker stats
```

### Reiniciar Containers

```bash
# Reiniciar tudo
docker-compose restart

# Reiniciar apenas backend
docker-compose restart backend

# Reiniciar apenas dashboard
docker-compose restart dashboard
```

## 🔄 Atualizar Aplicação

```bash
# 1. Fazer pull das alterações
git pull origin main

# 2. Rebuild local (sua máquina) e copiar JAR
./mvnw clean package -DskipTests
scp target/*.jar azureuser@<IP-PUBLICO>:/home/azureuser/humainze-java/target/

# 3. Na VM, recriar containers
docker-compose down
docker-compose up -d --build

# 4. Verificar logs
docker-compose logs -f
```

## 🛑 Parar e Remover

```bash
# Parar containers
docker-compose stop

# Parar e remover
docker-compose down

# Remover tudo incluindo volumes
docker-compose down -v
```

## 🔧 Troubleshooting

### Problema: Backend não inicia

```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar variáveis de ambiente
docker-compose config

# Testar conexão com Oracle
docker exec -it humainze-backend bash
nc -zv oracle.fiap.com.br 1521
```

### Problema: Dashboard não conecta ao backend

```bash
# Verificar se backend está acessível
docker exec -it humainze-dashboard curl http://backend:8080/actuator/health

# Ver logs do dashboard
docker-compose logs dashboard
```

### Problema: Portas não acessíveis externamente

```bash
# Verificar firewall do Azure NSG
az network nsg rule list \
  --resource-group humainze-rg \
  --nsg-name humainze-vmNSG \
  --output table

# Adicionar regra se necessário
az network nsg rule create \
  --resource-group humainze-rg \
  --nsg-name humainze-vmNSG \
  --name AllowBackend \
  --priority 1001 \
  --destination-port-ranges 8080 \
  --access Allow \
  --protocol Tcp
```

### Problema: Falta de memória

```bash
# Verificar uso de recursos
free -h
df -h

# Limpar imagens antigas
docker system prune -a
```

## 💰 Custos Estimados

**Azure VM Standard_B2s (Brazil South):**

- **Compute:** ~$35/mês (730 horas)
- **Storage:** ~$3/mês (30GB SSD)
- **Networking:** ~$2/mês (tráfego)

**Total estimado:** ~$40/mês

**💡 Dica:** Use Azure Student para créditos gratuitos ($100).

## 🔐 Segurança

### Recomendações

1. **Trocar secrets padrão:**
   - Gerar novo JWT_SECRET: `openssl rand -base64 32`
   - Atualizar em `.env`

2. **Habilitar HTTPS:**
   - Usar Nginx como reverse proxy
   - Certificado SSL gratuito com Let's Encrypt

3. **Restringir SSH:**
   - Permitir apenas seu IP no NSG
   - Usar chave SSH forte

4. **Backup regular:**
   - Exportar dados do OracleDB
   - Snapshot da VM

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs: `docker-compose logs -f`
2. Consultar [README.md](../README.md)
3. Abrir issue no [GitHub](https://github.com/viniruggeri/humainze-java/issues)

---

**Última atualização:** 21/11/2025  
**Versão:** 1.0.0  
**Autor:** Equipe Humainze (RM560431, RM560593, RM560039)
