/**
 * Teste 2: Leitura de Sensores
 *
 * Descrição:
 *   Valida leitura de todos os sensores (DHT22, MQ-135, LDR).
 *
 * Objetivo:
 *   - Ler temperatura e umidade do DHT22
 *   - Ler qualidade do ar do MQ-135
 *   - Ler luminosidade do LDR
 *   - Validar valores dentro de faixas esperadas
 *
 * Resultado esperado:
 *   - Temperatura: 15-40°C
 *   - Umidade: 20-95%
 *   - CO2: 400-2000 ppm
 *   - Luminosidade: 0-1000 lux
 */

#include "DHT.h"

// Pinos dos sensores
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define MQ135_PIN 34
#define LDR_PIN 35

DHT dht(DHT_PIN, DHT_TYPE);

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n╔════════════════════════════════════════════╗");
    Serial.println("║   TESTE 2: Leitura de Sensores            ║");
    Serial.println("╚════════════════════════════════════════════╝\n");

    // Inicializar sensores
    dht.begin();
    pinMode(MQ135_PIN, INPUT);
    pinMode(LDR_PIN, INPUT);

    Serial.println("✓ Sensores inicializados\n");
    Serial.println("Aguarde 2 segundos para estabilização...\n");
    delay(2000);
}

void loop()
{
    Serial.println("┌─────────────────────────────────────┐");
    Serial.println("│  Nova Leitura                       │");
    Serial.println("└─────────────────────────────────────┘");

    // ===== DHT22 =====
    Serial.println("\n[TESTE 2.1] DHT22 (Temperatura e Umidade)");

    float temperatura = dht.readTemperature();
    float umidade = dht.readHumidity();

    if (!isnan(temperatura) && !isnan(umidade))
    {
        Serial.print("  🌡️  Temperatura: ");
        Serial.print(temperatura, 1);
        Serial.println("°C");

        Serial.print("  💧 Umidade: ");
        Serial.print(umidade, 1);
        Serial.println("%");

        // Validação
        if (temperatura >= 15.0 && temperatura <= 40.0)
        {
            Serial.println("  ✓ Temperatura dentro do esperado");
        }
        else
        {
            Serial.println("  ⚠️  Temperatura fora da faixa esperada");
        }

        if (umidade >= 20.0 && umidade <= 95.0)
        {
            Serial.println("  ✓ Umidade dentro do esperado");
        }
        else
        {
            Serial.println("  ⚠️  Umidade fora da faixa esperada");
        }

        // Alertas
        if (temperatura > 28.0)
        {
            Serial.println("  🔴 ALERTA: Temperatura alta!");
        }
        if (umidade < 30.0)
        {
            Serial.println("  🔴 ALERTA: Ar muito seco!");
        }
        else if (umidade > 70.0)
        {
            Serial.println("  🔴 ALERTA: Umidade alta!");
        }
    }
    else
    {
        Serial.println("  ✗ ERRO: Falha ao ler DHT22");
    }

    // ===== MQ-135 =====
    Serial.println("\n[TESTE 2.2] MQ-135 (Qualidade do Ar)");

    int leituraMQ135 = analogRead(MQ135_PIN);
    float co2_ppm = map(leituraMQ135, 0, 4095, 400, 2000);

    Serial.print("  ☁️  ADC: ");
    Serial.println(leituraMQ135);

    Serial.print("  ☁️  CO2: ");
    Serial.print(co2_ppm, 0);
    Serial.println(" ppm");

    if (co2_ppm >= 400 && co2_ppm <= 2000)
    {
        Serial.println("  ✓ CO2 dentro do esperado");
    }
    else
    {
        Serial.println("  ⚠️  CO2 fora da faixa esperada");
    }

    // Alertas
    if (co2_ppm < 800)
    {
        Serial.println("  🟢 Qualidade do ar: EXCELENTE");
    }
    else if (co2_ppm < 1000)
    {
        Serial.println("  🟡 Qualidade do ar: BOA");
    }
    else if (co2_ppm < 1500)
    {
        Serial.println("  🟠 Qualidade do ar: MODERADA");
    }
    else
    {
        Serial.println("  🔴 ALERTA: Qualidade do ar RUIM! Ventile.");
    }

    // ===== LDR =====
    Serial.println("\n[TESTE 2.3] LDR (Luminosidade)");

    int leituraLDR = analogRead(LDR_PIN);
    float luminosidade = map(leituraLDR, 0, 4095, 0, 1000);

    Serial.print("  💡 ADC: ");
    Serial.println(leituraLDR);

    Serial.print("  💡 Luminosidade: ");
    Serial.print(luminosidade, 0);
    Serial.println(" lux");

    if (luminosidade >= 0 && luminosidade <= 1000)
    {
        Serial.println("  ✓ Luminosidade dentro do esperado");
    }
    else
    {
        Serial.println("  ⚠️  Luminosidade fora da faixa esperada");
    }

    // Alertas
    if (luminosidade < 200)
    {
        Serial.println("  🔴 ALERTA: Pouca luz! Acenda as luzes.");
    }
    else if (luminosidade < 300)
    {
        Serial.println("  🟡 Luminosidade ADEQUADA para trabalho");
    }
    else if (luminosidade < 750)
    {
        Serial.println("  🟢 Luminosidade IDEAL");
    }
    else
    {
        Serial.println("  🟠 Luminosidade ALTA (pode causar ofuscamento)");
    }

    Serial.println("\n─────────────────────────────────────\n");
    Serial.println("✓ Leitura concluída!");
    Serial.println("Próxima leitura em 10 segundos...\n");

    delay(10000);
}
