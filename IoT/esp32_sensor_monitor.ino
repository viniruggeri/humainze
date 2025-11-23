/**
 * ESP32 - Sistema de Monitoramento de Ambiente de Trabalho
 *
 * Descrição:
 *   Sistema IoT para monitoramento inteligente de ambientes corporativos
 *   alinhado ao tema "O Futuro do Trabalho" (FIAP).
 *
 * Sensores:
 *   - DHT22: Temperatura e Umidade
 *   - MQ-135: Qualidade do ar (CO2/gases)
 *   - LDR: Luminosidade
 *
 * Comunicação:
 *   - Protocolo: HTTP/JSON
 *   - Backend: Spring Boot Java (porta 8080)
 *   - Endpoint: POST /otel/v1/metrics
 *   - Auth: JWT (Bearer token)
 *
 * Autores:
 *   - Barbara Bonome Filipus (RM560431)
 *   - Vinicius Lira Ruggeri (RM560593)
 *   - Yasmin Pereira da Silva (RM560039)
 *
 * Data: 22/11/2025
 * Turma: 2TDSPR
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"
#include <time.h>

// ========== CONFIGURAÇÕES WiFi ==========
const char *WIFI_SSID = "Wokwi-GUEST"; // Para Wokwi: "Wokwi-GUEST"
const char *WIFI_PASSWORD = "";        // Para Wokwi: deixar vazio
// Para WiFi real, altere acima

// ========== CONFIGURAÇÕES Backend ==========
const char *BACKEND_HOST = "192.168.1.100"; // IP do backend Java
const int BACKEND_PORT = 8080;
const char *TEAM_NAME = "IOT";
const char *TEAM_SECRET = "iot-secret";
const char *LOCATION = "sala-1"; // Identificação da sala

// ========== CONFIGURAÇÕES Sensores ==========
#define DHT_PIN 4 // GPIO 4 para DHT22
#define DHT_TYPE DHT22
#define MQ135_PIN 34 // GPIO 34 (ADC1_6)
#define LDR_PIN 35   // GPIO 35 (ADC1_7)

// ========== CONFIGURAÇÕES Temporização ==========
#define INTERVALO_LEITURA 30000   // 30 segundos entre leituras
#define INTERVALO_RELOGIN 3600000 // 1 hora para renovar token

// ========== Objetos Globais ==========
DHT dht(DHT_PIN, DHT_TYPE);
String jwtToken = "";
unsigned long ultimaLeitura = 0;
unsigned long ultimoLogin = 0;

// ========== Protótipos de Funções ==========
void conectarWiFi();
bool fazerLogin();
String getISOTimestamp();
void lerSensores();
bool enviarMetrica(String metric, float value, String sensor);
String escapeJson(String str);

// ========== Setup ==========
void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n\n╔════════════════════════════════════════════╗");
    Serial.println("║   ESP32 - Monitoramento de Trabalho       ║");
    Serial.println("║   FIAP - Futuro do Trabalho                ║");
    Serial.println("╚════════════════════════════════════════════╝\n");

    // Inicializar sensores
    dht.begin();
    pinMode(MQ135_PIN, INPUT);
    pinMode(LDR_PIN, INPUT);

    Serial.println("✓ Sensores inicializados");

    // Conectar WiFi
    conectarWiFi();

    // Configurar NTP (horário)
    configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
    Serial.println("✓ NTP configurado (GMT-3)");

    // Fazer login inicial
    if (fazerLogin())
    {
        Serial.println("✓ Autenticação bem-sucedida\n");
        Serial.println("════════════════════════════════════════════");
        Serial.println("Sistema pronto! Iniciando monitoramento...");
        Serial.println("════════════════════════════════════════════\n");
    }
    else
    {
        Serial.println("✗ ERRO: Falha na autenticação");
        Serial.println("Verifique se o backend está rodando");
    }
}

// ========== Loop Principal ==========
void loop()
{
    unsigned long agora = millis();

    // Renovar token a cada 1 hora
    if (agora - ultimoLogin > INTERVALO_RELOGIN)
    {
        Serial.println("\n[INFO] Renovando token JWT...");
        fazerLogin();
    }

    // Ler sensores a cada 30 segundos
    if (agora - ultimaLeitura > INTERVALO_LEITURA)
    {
        lerSensores();
        ultimaLeitura = agora;
    }

    delay(100);
}

// ========== Conectar WiFi ==========
void conectarWiFi()
{
    Serial.print("Conectando ao WiFi");
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
        Serial.println(" conectado!");
        Serial.print("IP: ");
        Serial.println(WiFi.localIP());
    }
    else
    {
        Serial.println(" FALHOU!");
        Serial.println("Verifique SSID e senha");
    }
}

// ========== Fazer Login (Obter JWT) ==========
bool fazerLogin()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("✗ WiFi não conectado");
        return false;
    }

    HTTPClient http;
    String url = String("http://") + BACKEND_HOST + ":" + BACKEND_PORT + "/auth/login";

    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    // Payload de login
    StaticJsonDocument<200> loginDoc;
    loginDoc["team"] = TEAM_NAME;
    loginDoc["secret"] = TEAM_SECRET;

    String loginPayload;
    serializeJson(loginDoc, loginPayload);

    Serial.println("[LOGIN] Autenticando...");
    Serial.println("URL: " + url);

    int httpCode = http.POST(loginPayload);

    if (httpCode == 200)
    {
        String response = http.getString();

        // Parse JSON response
        StaticJsonDocument<512> responseDoc;
        DeserializationError error = deserializeJson(responseDoc, response);

        if (!error)
        {
            jwtToken = responseDoc["token"].as<String>();
            Serial.println("✓ Token obtido: " + jwtToken.substring(0, 20) + "...");
            ultimoLogin = millis();
            http.end();
            return true;
        }
        else
        {
            Serial.println("✗ Erro ao parsear JSON");
        }
    }
    else
    {
        Serial.print("✗ HTTP ");
        Serial.print(httpCode);
        Serial.print(": ");
        Serial.println(http.getString());
    }

    http.end();
    return false;
}

// ========== Obter Timestamp ISO 8601 ==========
String getISOTimestamp()
{
    time_t now;
    struct tm timeinfo;

    time(&now);
    gmtime_r(&now, &timeinfo);

    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);

    return String(buffer);
}

// ========== Ler Todos os Sensores ==========
void lerSensores()
{
    Serial.println("\n┌─────────────────────────────────────┐");
    Serial.println("│  Leitura de Sensores                │");
    Serial.println("└─────────────────────────────────────┘");

    bool algumSucesso = false;

    // ===== DHT22 (Temperatura e Umidade) =====
    float temperatura = dht.readTemperature();
    float umidade = dht.readHumidity();

    if (!isnan(temperatura) && !isnan(umidade))
    {
        Serial.printf("🌡️  Temperatura: %.1f°C\n", temperatura);
        Serial.printf("💧 Umidade: %.1f%%\n", umidade);

        // Enviar métricas
        if (enviarMetrica("temperature", temperatura, "DHT22"))
        {
            algumSucesso = true;
        }
        delay(500);

        if (enviarMetrica("humidity", umidade, "DHT22"))
        {
            algumSucesso = true;
        }
        delay(500);

        // Alerta de temperatura
        if (temperatura > 28.0)
        {
            Serial.println("⚠️  ALERTA: Temperatura alta!");
        }
        else if (temperatura < 18.0)
        {
            Serial.println("⚠️  ALERTA: Temperatura baixa!");
        }

        // Alerta de umidade
        if (umidade > 70.0)
        {
            Serial.println("⚠️  ALERTA: Umidade alta!");
        }
        else if (umidade < 30.0)
        {
            Serial.println("⚠️  ALERTA: Umidade baixa!");
        }
    }
    else
    {
        Serial.println("✗ Erro ao ler DHT22");
    }

    // ===== MQ-135 (Qualidade do Ar) =====
    int leituraMQ135 = analogRead(MQ135_PIN);
    // Conversão simplificada: 0-4095 ADC → 400-2000 ppm CO2
    float co2_ppm = map(leituraMQ135, 0, 4095, 400, 2000);

    Serial.printf("☁️  Qualidade Ar: %.0f ppm\n", co2_ppm);

    if (enviarMetrica("air_quality_ppm", co2_ppm, "MQ135"))
    {
        algumSucesso = true;
    }
    delay(500);

    if (co2_ppm > 1500)
    {
        Serial.println("⚠️  ALERTA: CO2 crítico! Ventile o ambiente.");
    }

    // ===== LDR (Luminosidade) =====
    int leituraLDR = analogRead(LDR_PIN);
    // Conversão simplificada: 0-4095 ADC → 0-1000 lux
    float luminosidade = map(leituraLDR, 0, 4095, 0, 1000);

    Serial.printf("💡 Luminosidade: %.0f lux\n", luminosidade);

    if (enviarMetrica("luminosity_lux", luminosidade, "LDR"))
    {
        algumSucesso = true;
    }
    delay(500);

    if (luminosidade < 200)
    {
        Serial.println("⚠️  ALERTA: Pouca luz! Risco de fadiga visual.");
    }

    // Status final
    if (algumSucesso)
    {
        Serial.println("\n✓ Leitura concluída com sucesso");
    }
    else
    {
        Serial.println("\n✗ Falha ao enviar métricas");
    }

    Serial.println("─────────────────────────────────────\n");
}

// ========== Enviar Métrica ao Backend ==========
bool enviarMetrica(String metric, float value, String sensor)
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("✗ WiFi desconectado");
        return false;
    }

    if (jwtToken.length() == 0)
    {
        Serial.println("✗ Token JWT não disponível");
        return false;
    }

    HTTPClient http;
    String url = String("http://") + BACKEND_HOST + ":" + BACKEND_PORT + "/otel/v1/metrics";

    http.begin(url);
    http.addHeader("Authorization", "Bearer " + jwtToken);
    http.addHeader("Content-Type", "application/json");

    // Construir payloadJson interno
    StaticJsonDocument<256> innerDoc;
    innerDoc["metric"] = metric;
    innerDoc["value"] = value;
    innerDoc["sensor"] = sensor;
    innerDoc["location"] = LOCATION;

    String payloadJson;
    serializeJson(innerDoc, payloadJson);

    // Construir request body
    StaticJsonDocument<512> requestDoc;
    requestDoc["teamTag"] = TEAM_NAME;
    requestDoc["timestamp"] = getISOTimestamp();
    requestDoc["payloadJson"] = payloadJson;

    String requestBody;
    serializeJson(requestDoc, requestBody);

    // Enviar POST
    int httpCode = http.POST(requestBody);

    if (httpCode == 201 || httpCode == 200)
    {
        Serial.print("  ✓ ");
        Serial.print(metric);
        Serial.print(" = ");
        Serial.print(value, 1);
        Serial.println(" enviado");
        http.end();
        return true;
    }
    else
    {
        Serial.print("  ✗ Erro HTTP ");
        Serial.print(httpCode);
        Serial.print(": ");
        Serial.println(http.getString());
        http.end();
        return false;
    }
}

// ========== Escape JSON String ==========
String escapeJson(String str)
{
    str.replace("\\", "\\\\");
    str.replace("\"", "\\\"");
    str.replace("\n", "\\n");
    str.replace("\r", "\\r");
    str.replace("\t", "\\t");
    return str;
}
