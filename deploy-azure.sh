#!/bin/bash
# Script de deploy automático para Azure (Suíça/Itália)
# Para Azure Student Plan

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
RESOURCE_GROUP="humainze-rg"
LOCATION="switzerlandnorth"  # ou "italynorth" ou "westeurope"
VM_NAME="humainze-vm"
VM_SIZE="Standard_B2s"  # Student: 2 vCPUs, 4GB RAM
VM_IMAGE="Ubuntu2204"
ADMIN_USERNAME="azureuser"
NSG_NAME="humainze-nsg"
PUBLIC_IP_NAME="humainze-ip"
GITHUB_REPO="https://github.com/viniruggeri/humainze-java.git"
GITHUB_BRANCH="IoT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Humainze - Deploy Automático Azure  ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Verifica se Azure CLI está instalado
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI não encontrado!${NC}"
    echo -e "${YELLOW}Instale: https://docs.microsoft.com/cli/azure/install-azure-cli${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Azure CLI encontrado${NC}\n"

# Login no Azure
echo -e "${YELLOW}🔐 Fazendo login no Azure...${NC}"
az login --use-device-code

# Verifica assinatura
echo -e "\n${YELLOW}📋 Assinaturas disponíveis:${NC}"
az account list --output table

# Define assinatura (se tiver mais de uma)
echo -e "\n${YELLOW}🎯 Definindo assinatura...${NC}"
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo -e "${GREEN}✓ Usando assinatura: $SUBSCRIPTION_ID${NC}"

# Cria Resource Group
echo -e "\n${YELLOW}📦 Criando Resource Group...${NC}"
if az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output none; then
    echo -e "${GREEN}✓ Resource Group criado: $RESOURCE_GROUP em $LOCATION${NC}"
else
    echo -e "${YELLOW}⚠ Resource Group já existe (continuando...)${NC}"
fi

# Cria Network Security Group com regras
echo -e "\n${YELLOW}🔒 Configurando Network Security Group...${NC}"
az network nsg create \
    --resource-group $RESOURCE_GROUP \
    --name $NSG_NAME \
    --location $LOCATION \
    --output none

# Regras NSG
echo -e "${YELLOW}🔐 Adicionando regras de firewall...${NC}"

# SSH (22)
az network nsg rule create \
    --resource-group $RESOURCE_GROUP \
    --nsg-name $NSG_NAME \
    --name AllowSSH \
    --priority 1000 \
    --source-address-prefixes '*' \
    --destination-port-ranges 22 \
    --protocol Tcp \
    --access Allow \
    --output none

# HTTP (80) - para redirect HTTPS
az network nsg rule create \
    --resource-group $RESOURCE_GROUP \
    --nsg-name $NSG_NAME \
    --name AllowHTTP \
    --priority 1001 \
    --source-address-prefixes '*' \
    --destination-port-ranges 80 \
    --protocol Tcp \
    --access Allow \
    --output none

# Backend (8081)
az network nsg rule create \
    --resource-group $RESOURCE_GROUP \
    --nsg-name $NSG_NAME \
    --name AllowBackend \
    --priority 1002 \
    --source-address-prefixes '*' \
    --destination-port-ranges 8081 \
    --protocol Tcp \
    --access Allow \
    --output none

# Dashboard (8501)
az network nsg rule create \
    --resource-group $RESOURCE_GROUP \
    --nsg-name $NSG_NAME \
    --name AllowDashboard \
    --priority 1003 \
    --source-address-prefixes '*' \
    --destination-port-ranges 8501 \
    --protocol Tcp \
    --access Allow \
    --output none

echo -e "${GREEN}✓ Regras de firewall configuradas${NC}"

# Cria IP Público
echo -e "\n${YELLOW}🌐 Criando IP Público...${NC}"
az network public-ip create \
    --resource-group $RESOURCE_GROUP \
    --name $PUBLIC_IP_NAME \
    --allocation-method Static \
    --sku Standard \
    --location $LOCATION \
    --output none
echo -e "${GREEN}✓ IP Público criado${NC}"

# Gera chave SSH se não existir
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "\n${YELLOW}🔑 Gerando chave SSH...${NC}"
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
    echo -e "${GREEN}✓ Chave SSH gerada${NC}"
fi

# Cria VM
echo -e "\n${YELLOW}🖥️  Criando Máquina Virtual (isso pode demorar 3-5 minutos)...${NC}"
az vm create \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --location $LOCATION \
    --size $VM_SIZE \
    --image $VM_IMAGE \
    --admin-username $ADMIN_USERNAME \
    --ssh-key-values ~/.ssh/id_rsa.pub \
    --public-ip-address $PUBLIC_IP_NAME \
    --nsg $NSG_NAME \
    --priority Spot \
    --max-price -1 \
    --eviction-policy Deallocate \
    --output none

echo -e "${GREEN}✓ VM criada com sucesso!${NC}"

# Obtém IP público
PUBLIC_IP=$(az network public-ip show \
    --resource-group $RESOURCE_GROUP \
    --name $PUBLIC_IP_NAME \
    --query ipAddress \
    --output tsv)

echo -e "\n${GREEN}✓ IP Público: $PUBLIC_IP${NC}"

# Script de setup na VM
echo -e "\n${YELLOW}⚙️  Configurando VM (instalando Docker, clonando repo...)${NC}"

SETUP_SCRIPT=$(cat <<'EOF'
#!/bin/bash
set -e

# Atualiza sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instala Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instala Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clona repositório
cd ~
git clone -b IoT https://github.com/viniruggeri/humainze-java.git
cd humainze-java

# Cria arquivo .env (você precisará editar com suas credenciais)
cat > .env << 'ENVFILE'
# Database
DB_USERNAME=rm560593
DB_PASSWORD=SUA_SENHA_AQUI

# JWT
JWT_SECRET=humainze-fiap-2024-super-secret-jwt-key-256-bits-minimum-required-for-production

# SEED (apenas primeira execução)
SEED_ENABLED=true
SEED_ADMIN_SECRET=admin-secret
SEED_IA_SECRET=ia-secret
SEED_IOT_SECRET=iot-secret
ENVFILE

echo "✓ Setup concluído! Edite o arquivo .env com suas credenciais"
echo "✓ Para iniciar: cd ~/humainze-java && docker-compose up -d"
EOF
)

# Executa setup via SSH
echo "$SETUP_SCRIPT" | ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$PUBLIC_IP 'bash -s'

echo -e "\n${GREEN}✓ Configuração da VM concluída!${NC}"

# Instruções finais
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  Deploy Concluído com Sucesso! 🎉     ${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${YELLOW}📝 Próximos passos:${NC}\n"
echo -e "1. Conecte-se à VM:"
echo -e "   ${GREEN}ssh $ADMIN_USERNAME@$PUBLIC_IP${NC}\n"

echo -e "2. Edite o arquivo .env com suas credenciais:"
echo -e "   ${GREEN}cd ~/humainze-java${NC}"
echo -e "   ${GREEN}nano .env${NC}\n"

echo -e "3. Inicie os containers:"
echo -e "   ${GREEN}docker-compose up -d${NC}\n"

echo -e "4. Verifique os logs:"
echo -e "   ${GREEN}docker-compose logs -f${NC}\n"

echo -e "5. Acesse os serviços:\n"
echo -e "   🔹 Backend API: ${BLUE}http://$PUBLIC_IP:8081${NC}"
echo -e "   🔹 Swagger: ${BLUE}http://$PUBLIC_IP:8081/swagger-ui.html${NC}"
echo -e "   🔹 Dashboard: ${BLUE}http://$PUBLIC_IP:8501${NC}\n"

echo -e "${YELLOW}⚠️  Lembre-se de:${NC}"
echo -e "   • Editar DB_PASSWORD no .env"
echo -e "   • Após primeira execução, mudar SEED_ENABLED=false"
echo -e "   • Fazer backup do JWT_SECRET\n"

echo -e "${YELLOW}💰 Custos Azure Student:${NC}"
echo -e "   • VM Spot B2s: ~\$10-15/mês"
echo -e "   • IP Público: ~\$3/mês"
echo -e "   • Total estimado: ~\$13-18/mês\n"

echo -e "${YELLOW}🗑️  Para deletar tudo:${NC}"
echo -e "   ${RED}az group delete --name $RESOURCE_GROUP --yes --no-wait${NC}\n"
