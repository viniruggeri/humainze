/**
 * Teste 3: Comunicação com Backend Java
 *
 * Descrição:
 *   Valida autenticação JWT e envio de métricas ao backend.
 *
 * Objetivo:
 *   - Conectar WiFi
 *   - Fazer login (POST /auth/login)
 *   - Receber token JWT
 *   - Enviar métrica de teste (POST /otel/v1/metrics)
 *   - Validar resposta HTTP 201
 *
 * Resultado esperado:
 *   - Login: HTTP 200 com token
 *   - Envio métrica: HTTP 201 Created
 *
 * IMPORTANTE:
 *   Configure BACKEND_HOST com o IP do seu backend Java.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

// WiFi
const char *WIFI_SSID = "Wokwi-GUEST";
const char *WIFI_PASSWORD = "";

// Backend
const char *BACKEND_HOST = "192.168.1.100"; // ⚠️ ALTERE AQUI
const int BACKEND_PORT = 8080;
const char *TEAM_NAME = "IOT";
const char *TEAM_SECRET = "iot-secret";

String jwtToken = "";

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n╔════════════════════════════════════════════╗");
    Serial.println("║   TESTE 3: Comunicação com Backend        ║");
    Serial.println("╚════════════════════════════════════════════╝\n");

    // Conectar WiFi
    Serial.println("[TESTE 3.1] Conectando WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int tentativas = 0;
    while (WiFi.status() != WL_CONNECTED && tentativas < 20)
    {
        delay(500);
        Serial.print(".");
        tentativas++;
    }

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("\n✓ WiFi conectado!");
        Serial.print("  IP: ");
        Serial.println(WiFi.localIP());
    }
    else
    {
        Serial.println("\n✗ FALHOU: WiFi não conectou");
        return;
    }

    // Configurar NTP
    configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
    delay(2000);

    // Teste de Login
    Serial.println("\n[TESTE 3.2] Login no backend...");
    Serial.println("  Backend: http://" + String(BACKEND_HOST) + ":" + String(BACKEND_PORT));
    Serial.println("  Team: " + String(TEAM_NAME));

    if (fazerLogin())
    {
        Serial.println("✓ Login bem-sucedido!");
        Serial.println("  Token: " + jwtToken.substring(0, 30) + "...");
    }
    else
    {
        Serial.println("✗ FALHOU: Login não funcionou");
        Serial.println("\nVerifique:");
        Serial.println("  1. Backend está rodando?");
        Serial.println("  2. IP/porta corretos?");
        Serial.println("  3. Team IOT cadastrado?");
        return;
    }

    // Teste de Envio de Métrica
    Serial.println("\n[TESTE 3.3] Enviando métrica de teste...");

    if (enviarMetricaTeste())
    {
        Serial.println("✓ Métrica enviada com sucesso!");
    }
    else
    {
        Serial.println("✗ FALHOU: Erro ao enviar métrica");
    }

    Serial.println("\n════════════════════════════════════════════");
    Serial.println("Teste 3 concluído!");
    Serial.println("════════════════════════════════════════════\n");
}

void loop()
{
    // Enviar métrica a cada 15 segundos
    delay(15000);

    Serial.println("\n[LOOP] Enviando nova métrica de teste...");

    if (enviarMetricaTeste())
    {
        Serial.println("✓ Métrica enviada");
    }
    else
    {
        Serial.println("✗ Erro ao enviar");

        // Tentar relogin
        Serial.println("Tentando relogin...");
        fazerLogin();
    }
}

// ========== Fazer Login ==========
bool fazerLogin()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("  ✗ WiFi não conectado");
        return false;
    }

    HTTPClient http;
    String url = String("http://") + BACKEND_HOST + ":" + BACKEND_PORT + "/auth/login";

    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(10000);

    // Payload
    StaticJsonDocument<200> doc;
    doc["team"] = TEAM_NAME;
    doc["secret"] = TEAM_SECRET;

    String payload;
    serializeJson(doc, payload);

    Serial.println("  URL: " + url);
    Serial.println("  Payload: " + payload);

    int httpCode = http.POST(payload);

    Serial.print("  HTTP Code: ");
    Serial.println(httpCode);

    if (httpCode == 200)
    {
        String response = http.getString();
        Serial.println("  Response: " + response);

        StaticJsonDocument<512> responseDoc;
        DeserializationError error = deserializeJson(responseDoc, response);

        if (!error)
        {
            jwtToken = responseDoc["token"].as<String>();
            http.end();
            return true;
        }
        else
        {
            Serial.print("  ✗ Erro JSON: ");
            Serial.println(error.c_str());
        }
    }
    else
    {
        Serial.print("  ✗ HTTP ");
        Serial.print(httpCode);
        Serial.print(": ");
        Serial.println(http.getString());
    }

    http.end();
    return false;
}

// ========== Enviar Métrica de Teste ==========
bool enviarMetricaTeste()
{
    if (jwtToken.length() == 0)
    {
        Serial.println("  ✗ Token JWT não disponível");
        return false;
    }

    HTTPClient http;
    String url = String("http://") + BACKEND_HOST + ":" + BACKEND_PORT + "/otel/v1/metrics";

    http.begin(url);
    http.addHeader("Authorization", "Bearer " + jwtToken);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(10000);

    // Timestamp ISO
    time_t now;
    struct tm timeinfo;
    time(&now);
    gmtime_r(&now, &timeinfo);
    char timestamp[30];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);

    // PayloadJson interno
    StaticJsonDocument<256> innerDoc;
    innerDoc["metric"] = "test_connectivity";
    innerDoc["value"] = 1.0;
    innerDoc["sensor"] = "ESP32-TEST";
    innerDoc["location"] = "test-bench";

    String payloadJson;
    serializeJson(innerDoc, payloadJson);

    // Request body
    StaticJsonDocument<512> requestDoc;
    requestDoc["teamTag"] = TEAM_NAME;
    requestDoc["timestamp"] = timestamp;
    requestDoc["payloadJson"] = payloadJson;

    String requestBody;
    serializeJson(requestDoc, requestBody);

    Serial.println("  URL: " + url);
    Serial.println("  Body: " + requestBody);

    int httpCode = http.POST(requestBody);

    Serial.print("  HTTP Code: ");
    Serial.println(httpCode);

    if (httpCode == 201 || httpCode == 200)
    {
        Serial.println("  Response: " + http.getString());
        http.end();
        return true;
    }
    else
    {
        Serial.print("  ✗ HTTP ");
        Serial.print(httpCode);
        Serial.print(": ");
        Serial.println(http.getString());
        http.end();
        return false;
    }
}
