# 🚀 QUICK START

## 1️⃣ Faça os 3 logins:

### Admin:
Abra `admin.http` → Execute POST /auth/login → Copie o token

### IA:
Abra `ia.http` → Execute POST /auth/login → Copie o token

### IOT:
Abra `iot.http` → Execute POST /auth/login → Copie o token

---

## 2️⃣ Configure os tokens:

Abra `http-client.env.json` e cole os 3 tokens:

```json
{
  "dev": {
    "baseUrl": "http://localhost:8080",
    "adminToken": "COLE_TOKEN_ADMIN_AQUI",
    "iaToken": "COLE_TOKEN_IA_AQUI",
    "iotToken": "COLE_TOKEN_IOT_AQUI"
  }
}
```

Salve (Ctrl+S)

---

## 3️⃣ Use qualquer requisição!

Agora todas as requisições nos 3 arquivos funcionam automaticamente!

O IntelliJ substitui `{{adminToken}}`, `{{iaToken}}`, `{{iotToken}}` pelos valores do `http-client.env.json`.

---

## 📁 Arquivos:

- **`admin.http`** - Gestão (CRUD times, ver tudo)
- **`ia.http`** - Métricas de ML (acurácia, CPU, alertas)
- **`iot.http`** - Sensores (temperatura, umidade, CO2...)
- **`http-client.env.json`** - Tokens (EDITE AQUI)

---

## ✅ Pronto!

Simples assim! 🎉

