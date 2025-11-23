/**
 * Teste 1: Conectividade WiFi e NTP
 *
 * Descrição:
 *   Valida conexão WiFi e sincronização de horário.
 *
 * Objetivo:
 *   - Conectar ao WiFi
 *   - Obter IP válido
 *   - Sincronizar horário via NTP
 *   - Imprimir timestamp ISO 8601
 *
 * Resultado esperado:
 *   - WiFi conectado
 *   - IP exibido
 *   - Timestamp válido (formato: 2025-11-22T15:30:00Z)
 */

#include <WiFi.h>
#include <time.h>

const char *WIFI_SSID = "Wokwi-GUEST";
const char *WIFI_PASSWORD = "";

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n╔════════════════════════════════════════════╗");
    Serial.println("║   TESTE 1: Conectividade WiFi e NTP       ║");
    Serial.println("╚════════════════════════════════════════════╝\n");

    // Teste 1: Conectar WiFi
    Serial.println("[TESTE 1.1] Conectando WiFi...");
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
        Serial.print("  RSSI: ");
        Serial.print(WiFi.RSSI());
        Serial.println(" dBm");
    }
    else
    {
        Serial.println("\n✗ FALHOU: WiFi não conectou");
        return;
    }

    // Teste 2: Configurar NTP
    Serial.println("\n[TESTE 1.2] Configurando NTP...");
    configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");

    // Aguardar sincronização
    Serial.print("  Aguardando sincronização");
    int timeout = 0;
    time_t now = 0;
    while (now < 1000000000 && timeout < 20)
    {
        delay(500);
        Serial.print(".");
        time(&now);
        timeout++;
    }

    if (now >= 1000000000)
    {
        Serial.println("\n✓ NTP sincronizado!");

        struct tm timeinfo;
        gmtime_r(&now, &timeinfo);

        char buffer[30];
        strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);

        Serial.print("  Timestamp ISO: ");
        Serial.println(buffer);
    }
    else
    {
        Serial.println("\n✗ FALHOU: Timeout ao sincronizar NTP");
    }

    Serial.println("\n════════════════════════════════════════════");
    Serial.println("Teste 1 concluído!");
    Serial.println("════════════════════════════════════════════\n");
}

void loop()
{
    // Imprimir timestamp a cada 5 segundos
    delay(5000);

    time_t now;
    struct tm timeinfo;

    time(&now);
    gmtime_r(&now, &timeinfo);

    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);

    Serial.print("[");
    Serial.print(buffer);
    Serial.println("] Sistema ativo");
}
