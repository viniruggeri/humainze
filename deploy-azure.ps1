# Script de deploy automático para Azure (Suíça/Itália) - PowerShell
# Para Azure Student Plan

$ErrorActionPreference = "Stop"

# Configurações
$RESOURCE_GROUP = "humainze-rg"
$LOCATION = "switzerlandnorth"  # ou "italynorth" ou "westeurope"
$VM_NAME = "humainze-vm"
$VM_SIZE = "Standard_B2s"  # Student: 2 vCPUs, 4GB RAM
$VM_IMAGE = "Ubuntu2204"
$ADMIN_USERNAME = "azureuser"
$NSG_NAME = "humainze-nsg"
$PUBLIC_IP_NAME = "humainze-ip"
$GITHUB_REPO = "https://github.com/viniruggeri/humainze-java.git"
$GITHUB_BRANCH = "IoT"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Humainze - Deploy Automático Azure  " -ForegroundColor Blue
Write-Host "========================================`n" -ForegroundColor Blue

# Verifica se Azure CLI está instalado
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Azure CLI não encontrado!" -ForegroundColor Red
    Write-Host "Instale: https://docs.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Azure CLI encontrado`n" -ForegroundColor Green

# Login no Azure
Write-Host "🔐 Fazendo login no Azure..." -ForegroundColor Yellow
az login

# Verifica assinatura
Write-Host "`n📋 Assinaturas disponíveis:" -ForegroundColor Yellow
az account list --output table

# Define assinatura
Write-Host "`n🎯 Definindo assinatura..." -ForegroundColor Yellow
$SUBSCRIPTION_ID = az account show --query id -o tsv
Write-Host "✓ Usando assinatura: $SUBSCRIPTION_ID" -ForegroundColor Green

# Cria Resource Group
Write-Host "`n📦 Criando Resource Group..." -ForegroundColor Yellow
try {
    az group create `
        --name $RESOURCE_GROUP `
        --location $LOCATION `
        --output none
    Write-Host "✓ Resource Group criado: $RESOURCE_GROUP em $LOCATION" -ForegroundColor Green
}
catch {
    Write-Host "⚠ Resource Group já existe (continuando...)" -ForegroundColor Yellow
}

# Cria Network Security Group
Write-Host "`n🔒 Configurando Network Security Group..." -ForegroundColor Yellow
az network nsg create `
    --resource-group $RESOURCE_GROUP `
    --name $NSG_NAME `
    --location $LOCATION `
    --output none

# Regras NSG
Write-Host "🔐 Adicionando regras de firewall..." -ForegroundColor Yellow

# SSH (22)
az network nsg rule create `
    --resource-group $RESOURCE_GROUP `
    --nsg-name $NSG_NAME `
    --name AllowSSH `
    --priority 1000 `
    --source-address-prefixes '*' `
    --destination-port-ranges 22 `
    --protocol Tcp `
    --access Allow `
    --output none

# HTTP (80)
az network nsg rule create `
    --resource-group $RESOURCE_GROUP `
    --nsg-name $NSG_NAME `
    --name AllowHTTP `
    --priority 1001 `
    --source-address-prefixes '*' `
    --destination-port-ranges 80 `
    --protocol Tcp `
    --access Allow `
    --output none

# Backend (8081)
az network nsg rule create `
    --resource-group $RESOURCE_GROUP `
    --nsg-name $NSG_NAME `
    --name AllowBackend `
    --priority 1002 `
    --source-address-prefixes '*' `
    --destination-port-ranges 8081 `
    --protocol Tcp `
    --access Allow `
    --output none

# Dashboard (8501)
az network nsg rule create `
    --resource-group $RESOURCE_GROUP `
    --nsg-name $NSG_NAME `
    --name AllowDashboard `
    --priority 1003 `
    --source-address-prefixes '*' `
    --destination-port-ranges 8501 `
    --protocol Tcp `
    --access Allow `
    --output none

Write-Host "✓ Regras de firewall configuradas" -ForegroundColor Green

# Cria IP Público
Write-Host "`n🌐 Criando IP Público..." -ForegroundColor Yellow
az network public-ip create `
    --resource-group $RESOURCE_GROUP `
    --name $PUBLIC_IP_NAME `
    --allocation-method Static `
    --sku Standard `
    --location $LOCATION `
    --output none
Write-Host "✓ IP Público criado" -ForegroundColor Green

# Gera chave SSH se não existir
$sshKeyPath = "$env:USERPROFILE\.ssh\id_rsa"
if (-not (Test-Path $sshKeyPath)) {
    Write-Host "`n🔑 Gerando chave SSH..." -ForegroundColor Yellow
    ssh-keygen -t rsa -b 4096 -f $sshKeyPath -N '""'
    Write-Host "✓ Chave SSH gerada" -ForegroundColor Green
}

# Cria VM
Write-Host "`n🖥️  Criando Máquina Virtual (isso pode demorar 3-5 minutos)..." -ForegroundColor Yellow
az vm create `
    --resource-group $RESOURCE_GROUP `
    --name $VM_NAME `
    --location $LOCATION `
    --size $VM_SIZE `
    --image $VM_IMAGE `
    --admin-username $ADMIN_USERNAME `
    --ssh-key-values "$sshKeyPath.pub" `
    --public-ip-address $PUBLIC_IP_NAME `
    --nsg $NSG_NAME `
    --priority Spot `
    --max-price -1 `
    --eviction-policy Deallocate `
    --output none

Write-Host "✓ VM criada com sucesso!" -ForegroundColor Green

# Obtém IP público
$PUBLIC_IP = az network public-ip show `
    --resource-group $RESOURCE_GROUP `
    --name $PUBLIC_IP_NAME `
    --query ipAddress `
    --output tsv

Write-Host "`n✓ IP Público: $PUBLIC_IP" -ForegroundColor Green

# Script de setup na VM
Write-Host "`n⚙️  Configurando VM (instalando Docker, clonando repo...)..." -ForegroundColor Yellow

$setupScript = @'
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

# Cria arquivo .env
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
'@

# Executa setup via SSH
$setupScript | ssh -o StrictHostKeyChecking=no "$ADMIN_USERNAME@$PUBLIC_IP" 'bash -s'

Write-Host "`n✓ Configuração da VM concluída!" -ForegroundColor Green

# Instruções finais
Write-Host "`n========================================" -ForegroundColor Blue
Write-Host "  Deploy Concluído com Sucesso! 🎉     " -ForegroundColor Blue
Write-Host "========================================`n" -ForegroundColor Blue

Write-Host "📝 Próximos passos:`n" -ForegroundColor Yellow
Write-Host "1. Conecte-se à VM:"
Write-Host "   ssh $ADMIN_USERNAME@$PUBLIC_IP`n" -ForegroundColor Green

Write-Host "2. Edite o arquivo .env com suas credenciais:"
Write-Host "   cd ~/humainze-java" -ForegroundColor Green
Write-Host "   nano .env`n" -ForegroundColor Green

Write-Host "3. Inicie os containers:"
Write-Host "   docker-compose up -d`n" -ForegroundColor Green

Write-Host "4. Verifique os logs:"
Write-Host "   docker-compose logs -f`n" -ForegroundColor Green

Write-Host "5. Acesse os serviços:`n"
Write-Host "   🔹 Backend API: http://$PUBLIC_IP:8081" -ForegroundColor Blue
Write-Host "   🔹 Swagger: http://$PUBLIC_IP:8081/swagger-ui.html" -ForegroundColor Blue
Write-Host "   🔹 Dashboard: http://$PUBLIC_IP:8501`n" -ForegroundColor Blue

Write-Host "⚠️  Lembre-se de:" -ForegroundColor Yellow
Write-Host "   • Editar DB_PASSWORD no .env"
Write-Host "   • Após primeira execução, mudar SEED_ENABLED=false"
Write-Host "   • Fazer backup do JWT_SECRET`n"

Write-Host "💰 Custos Azure Student:" -ForegroundColor Yellow
Write-Host "   • VM Spot B2s: ~`$10-15/mês"
Write-Host "   • IP Público: ~`$3/mês"
Write-Host "   • Total estimado: ~`$13-18/mês`n"

Write-Host "🗑️  Para deletar tudo:" -ForegroundColor Yellow
Write-Host "   az group delete --name $RESOURCE_GROUP --yes --no-wait`n" -ForegroundColor Red
