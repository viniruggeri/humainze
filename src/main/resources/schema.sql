-- Criar sequences para geração de IDs no Oracle
-- Estas sequences serão usadas pelo Hibernate com @SequenceGenerator

-- Sequence para metric_records (IF NOT EXISTS não funciona no Oracle, usar BEGIN/EXCEPTION)
BEGIN
   EXECUTE IMMEDIATE 'CREATE SEQUENCE METRIC_SEQ START WITH 1 INCREMENT BY 1';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE = -955 THEN
         NULL; -- Sequence já existe, ignorar
      ELSE
         RAISE;
      END IF;
END;
/

-- Sequence para span_records
BEGIN
   EXECUTE IMMEDIATE 'CREATE SEQUENCE SPAN_SEQ START WITH 1 INCREMENT BY 1';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE = -955 THEN
         NULL; -- Sequence já existe, ignorar
      ELSE
         RAISE;
      END IF;
END;
/

-- Sequence para log_records
BEGIN
   EXECUTE IMMEDIATE 'CREATE SEQUENCE LOG_SEQ START WITH 1 INCREMENT BY 1';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE = -955 THEN
         NULL; -- Sequence já existe, ignorar
      ELSE
         RAISE;
      END IF;
END;
/
