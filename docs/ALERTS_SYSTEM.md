# 🚨 Sistema de Alertas Cognitivos

## Visão Geral

O **Sistema de Alertas Cognitivos** do Humainze Backend é responsável por detectar, notificar e gerenciar anomalias em tempo real nos módulos de IoT e IA.

## 🎯 Tipos de Alertas

### 1. DRIFT
**Descrição:** Detecta mudanças no comportamento do modelo de Machine Learning.

**Quando é disparado:**
- Acurácia do modelo cai abaixo do threshold (ex: de 95% para 78%)
- Distribuição de features muda significativamente
- Padrões de predição divergem do esperado

**Exemplo:**
```json
{
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Drift detectado no modelo v2.1 - acurácia caiu de 0.95 para 0.78"
}
```

### 2. MODEL_ERROR
**Descrição:** Erro crítico no pipeline de inferência ou treinamento.

**Quando é disparado:**
- Timeout em chamadas ao modelo
- Exceção durante predição
- Dados de entrada inválidos
- Falta de recursos (memória/CPU)

**Exemplo:**
```json
{
  "teamTag": "IA",
  "type": "MODEL_ERROR",
  "message": "Erro crítico no pipeline de inferência - Timeout em chamadas ao modelo"
}
```

### 3. SERVICE_DOWN
**Descrição:** Serviço crítico não está respondendo.

**Quando é disparado:**
- Health check falhou
- Serviço de coleta de dados IoT offline
- Banco de dados inacessível
- API externa não responde

**Exemplo:**
```json
{
  "teamTag": "IOT",
  "type": "SERVICE_DOWN",
  "message": "Serviço de coleta de dados IoT não está respondendo"
}
```

## 📡 Endpoints da API

### Criar Alerta
```http
POST /alerts
Authorization: Bearer {token}
Content-Type: application/json

{
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Descrição detalhada do alerta"
}
```

**Resposta 201 Created:**
```json
{
  "id": 1,
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Descrição detalhada do alerta",
  "timestamp": "2025-11-21T14:30:00Z",
  "resolved": false
}
```

### Listar Alertas (com paginação)
```http
GET /alerts?team=IA&page=0&size=20&sort=timestamp,desc
Authorization: Bearer {token}
```

**Resposta 200 OK:**
```json
{
  "content": [
    {
      "id": 5,
      "teamTag": "IA",
      "type": "DRIFT",
      "message": "Drift detectado...",
      "timestamp": "2025-11-21T14:30:00Z",
      "resolved": false
    }
  ],
  "totalElements": 50,
  "totalPages": 3,
  "size": 20,
  "number": 0
}
```

### Listar Apenas Não Resolvidos
```http
GET /alerts/unresolved?team=IA
Authorization: Bearer {token}
```

### Contar Não Resolvidos
```http
GET /alerts/unresolved/count?team=IA
Authorization: Bearer {token}
```

**Resposta 200 OK:**
```json
12
```

### Resolver Alerta
```http
PUT /alerts/{id}/resolve
Authorization: Bearer {token}
```

**Resposta 200 OK:**
```json
{
  "id": 1,
  "teamTag": "IA",
  "type": "DRIFT",
  "message": "Drift detectado...",
  "timestamp": "2025-11-21T14:30:00Z",
  "resolved": true
}
```

## 📊 Dashboard Streamlit

### Banner de Alertas

Quando há alertas não resolvidos, um **banner vermelho** aparece no topo do dashboard:

```
┌────────────────────────────────────────────────────────────┐
│ 🚨 [5] Alerta(s) Cognitivo(s) Não Resolvido(s)           │
│ Alertas críticos detectados pelo sistema de monitoramento │
│ ▼ Ver Alertas Detalhados                                  │
└────────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Contagem em tempo real de alertas ativos
- Expander para ver detalhes
- Botões de resolução inline
- Auto-refresh a cada 5 segundos (opcional)

### Aba de Alertas

**Tab "🔴 Não Resolvidos":**
- Lista todos os alertas ativos
- Cards estilizados por tipo (cores diferentes)
- Informações: ID, Team, Tipo, Mensagem, Timestamp
- Botão "✅ Resolver" para cada alerta

**Tab "✅ Todos":**
- Histórico completo de alertas
- Filtros:
  - Status: Todos / Não Resolvidos / Resolvidos
  - Tipo: Todos / DRIFT / MODEL_ERROR / SERVICE_DOWN
  - Itens por página: 10 / 20 / 50 / 100
- Paginação: Primeira / Anterior / Próxima / Última
- Alertas resolvidos aparecem com opacidade reduzida

## 🔔 Sistema de Notificações

### Auto-Refresh (Polling)

O dashboard implementa polling automático para atualizar alertas:

```python
# Auto-refresh a cada 5 segundos
if auto_refresh:
    time.sleep(5)
    st.rerun()
```

**Como ativar:**
1. Na sidebar, marcar "🔄 Auto-refresh"
2. Dashboard recarrega automaticamente
3. Banner atualiza contagem de alertas
4. Notificação visual quando novos alertas aparecem

## 🎨 Estilização por Tipo

### Cores dos Alertas

```css
DRIFT:        #ff9800 (Laranja)
MODEL_ERROR:  #f44336 (Vermelho)
SERVICE_DOWN: #ff0844 (Vermelho Intenso)
```

### Ícones

```
DRIFT:        📉
MODEL_ERROR:  ⚠️
SERVICE_DOWN: 🔴
```

## 🧪 Testes

### Script de Teste Completo

```bash
cd dashboard
python test_alerts.py
```

**O que o script testa:**
1. ✅ Autenticação como IA
2. ✅ Criação de 4 alertas de teste
3. ✅ Contagem de alertas não resolvidos
4. ✅ Listagem por team
5. ✅ Resolução de alerta
6. ✅ Histórico completo

**Saída esperada:**
```
🧪 Teste de Sistema de Alertas
============================================================
1️⃣ Autenticando como IA...
✅ Token obtido

2️⃣ Criando alertas de teste...
   ✅ Alerta criado: DRIFT - IA
   ✅ Alerta criado: MODEL_ERROR - IA
   ✅ Alerta criado: SERVICE_DOWN - IOT
   ✅ Alerta criado: DRIFT - IA

✅ 4/4 alertas criados com sucesso

3️⃣ Verificando alertas não resolvidos...
   📊 Total geral: 4 alerta(s)
   🟣 Team IA: 3 alerta(s)
   🟢 Team IOT: 1 alerta(s)

4️⃣ Listando alertas do Team IA...
   Total: 3 alerta(s)
   🔸 [DRIFT] Detectado drift no modelo de predição...
   🔸 [MODEL_ERROR] Erro crítico no pipeline de inferência...

5️⃣ Testando resolução de alerta...
   Resolvendo alerta ID 1...
   ✅ Alerta 1 resolvido com sucesso!
   📊 Nova contagem Team IA: 2 alerta(s)

6️⃣ Listando histórico completo...
   📊 Total no histórico: 4 alerta(s)
   ✅ Resolvidos: 1
   🔴 Ativos: 3
   📈 Por tipo:
      • DRIFT: 2
      • MODEL_ERROR: 1
      • SERVICE_DOWN: 1

============================================================
✅ Teste concluído!
```

## 📐 Arquitetura de Alertas

```
┌─────────────────────────────────────────────────────────┐
│                    Fluxo de Alertas                     │
└─────────────────────────────────────────────────────────┘

1. Detecção de Anomalia (IA/IoT)
   ↓
2. POST /alerts (Backend Java)
   ↓
3. Validação Bean Validation
   ↓
4. Persistência no Banco (OracleDB/H2)
   ↓
5. Dashboard polling GET /alerts/unresolved/count
   ↓
6. Banner vermelho aparece
   ↓
7. Usuário expande detalhes
   ↓
8. PUT /alerts/{id}/resolve
   ↓
9. Alerta marcado como resolvido
   ↓
10. Banner atualiza contagem
```

## 🔒 Segurança e RBAC

### Permissões por Role

| Endpoint | ADMIN | IA | IOT |
|----------|-------|----|----|
| GET /alerts | ✅ | ✅ | ❌ |
| POST /alerts | ✅ | ✅ | ✅ |
| PUT /alerts/{id}/resolve | ✅ | ✅ | ❌ |
| GET /alerts/unresolved | ✅ | ✅ | ❌ |

**Regras:**
- **ADMIN:** Acesso total a todos os alertas
- **IA:** Pode criar e resolver alertas do próprio team
- **IOT:** Pode apenas criar alertas (sem visualização)

### Filtro por Team

```java
// AlertService.java
public Page<AlertResponse> listUnresolvedAlerts(String teamTag, Pageable pageable) {
    if (teamTag == null) {
        return alertRepository.findByResolvedFalse(pageable).map(this::toResponse);
    }
    return alertRepository.findByTeamTagAndResolvedFalse(teamTag, pageable).map(this::toResponse);
}
```

## 📊 Métricas e KPIs

### Métricas Expostas

```
# Contador de alertas criados
alerts.created.total{type="DRIFT", team="IA"} = 15

# Contador de alertas resolvidos
alerts.resolved.total{type="MODEL_ERROR", team="IA"} = 8

# Gauge de alertas ativos
alerts.unresolved.count{team="IA"} = 7

# Histograma de tempo de resolução
alerts.resolution.time.seconds{team="IA", quantile="0.95"} = 120
```

### Queries SQL para Análise

```sql
-- Alertas por tipo nas últimas 24h
SELECT 
  type, 
  COUNT(*) as count
FROM alerts
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '24' HOUR
GROUP BY type
ORDER BY count DESC;

-- Tempo médio de resolução por team
SELECT 
  teamTag,
  AVG(TIMESTAMPDIFF(SECOND, timestamp, resolvedAt)) as avg_resolution_seconds
FROM alerts
WHERE resolved = true
GROUP BY teamTag;
```

## 🚀 Próximas Funcionalidades

- [ ] Notificações via WebSocket (push em tempo real)
- [ ] Alertas compostos (múltiplas condições)
- [ ] Severidade dos alertas (LOW, MEDIUM, HIGH, CRITICAL)
- [ ] SLA tracking (tempo máximo de resolução)
- [ ] Integração com Slack/Teams
- [ ] Machine Learning para predição de alertas
- [ ] Dashboard de analytics de alertas

## 📚 Referências

- [AlertController.java](../src/main/java/com/backend/humainzedash/controller/AlertController.java)
- [AlertService.java](../src/main/java/com/backend/humainzedash/service/AlertService.java)
- [AlertRepository.java](../src/main/java/com/backend/humainzedash/repository/AlertRepository.java)
- [app.py (Dashboard)](../dashboard/app.py)
- [test_alerts.py](../dashboard/test_alerts.py)

---

**Última atualização:** 21/11/2025  
**Versão:** 1.0.0  
**Autor:** Equipe Humainze (RM560431, RM560593, RM560039)
