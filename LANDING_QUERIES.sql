USE ROLE INGESTION_ROLE;
USE DATABASE KIPITHON_DB;
USE SCHEMA KIPITHON_DB.LANDING;
---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE TABLE KIPITHON_DB.LANDING.QUERY_HISTORY_RESULTS_STG (
    QUERY VARCHAR,
    DB_NAME VARCHAR,
    FULL_SCAN VARCHAR,
    EXEC_COUNT INT,
    ERR_COUNT INT,
    TOTAL_LATENCY VARCHAR,
    MAX_LATENCY VARCHAR,
    AVG_LATENCY VARCHAR,
    MAX_TOTAL_MEMORY VARCHAR,
    ROWS_SENT INT,
    ROWS_EXAMINED INT,
    ROWS_AFFECTED INT,
    FIRST_SEEN DATE,
    LAST_SEEN DATE
);
---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE TABLE  KIPITHON_DB.LANDING.SCHEMA_MEMORY_DETAILS_STG (
TABLE_SCHEMA VARCHAR,
TABLE_NAME VARCHAR,
TABLE_TYPE VARCHAR, 
DATA_LENGTH INT,
INDEX_LENGTH INT
);
---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE TABLE  KIPITHON_DB.LANDING.DB_OBJECT_OVERVIEW_STG (
DB VARCHAR,
OBJECT_TYPE VARCHAR,
COUNT INT 
);
---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE TABLE  KIPITHON_DB.LANDING.DB_HOST_SUMMARY_STG (
STATEMENTS NUMBER(38,0),
	STATEMENT_LATENCY VARCHAR,
	TABLE_SCANS NUMBER(38,0),
	TOTAL_CONNECTIONS NUMBER(38,0),
	CURRENT_MEMORY VARCHAR,
	TOTAL_MEMORY_ALLOCATED VARCHAR
);

---------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE TABLE KIPITHON_DB.LANDING.QUERY_HISTORY_RESULTS_STG_HISTORY (
    QUERY VARCHAR,
    DB_NAME VARCHAR,
    FULL_SCAN VARCHAR,
    EXEC_COUNT INT,
    ERR_COUNT INT,
    TOTAL_LATENCY VARCHAR,
    MAX_LATENCY VARCHAR,
    AVG_LATENCY VARCHAR,
    MAX_TOTAL_MEMORY VARCHAR,
    ROWS_SENT INT,
    ROWS_EXAMINED INT,
    ROWS_AFFECTED INT,
    FIRST_SEEN DATE,
    LAST_SEEN DATE
);


