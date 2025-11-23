-- Criar sequences para geração de IDs no Oracle
-- Estas sequences serão usadas pelo Hibernate com @SequenceGenerator

-- Sequence para metric_records
CREATE SEQUENCE METRIC_SEQ START WITH 1 INCREMENT BY 1;

-- Sequence para span_records
CREATE SEQUENCE SPAN_SEQ START WITH 1 INCREMENT BY 1;

-- Sequence para log_records
CREATE SEQUENCE LOG_SEQ START WITH 1 INCREMENT BY 1;
