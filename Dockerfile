# Multi-stage build para Java backend
FROM eclipse-temurin:21-jdk-alpine AS build

WORKDIR /app

# Copia arquivos do Maven
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

# Dá permissão e baixa dependências (cache layer)
RUN chmod +x mvnw && ./mvnw dependency:go-offline -B

# Copia código fonte
COPY src ./src

# Build da aplicação (pula testes para build mais rápido)
RUN ./mvnw clean package -DskipTests

# Stage final - runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copia JAR do stage de build
COPY --from=build /app/target/*.jar app.jar

# Cria usuário não-root para segurança
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Expõe porta 8081
EXPOSE 8081

# Variáveis de ambiente com valores padrão
ENV JAVA_OPTS="-Xms256m -Xmx512m" \
    SPRING_PROFILES_ACTIVE=prod

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8081/actuator/health || exit 1

# Comando de execução
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
