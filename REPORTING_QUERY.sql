USE ROLE REPORTING_ROLE;
USE DATABASE KIPITHON_DB;
USE SCHEMA KIPITHON_DB.REPORTING;

---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.SCHEMA_MEMORY_DETAILS --- SAMPLE_DB.REPORTING.TBL_NAME_SIZE_TBL - Volumetric Analysis
AS
SELECT 
	TABLE_SCHEMA AS OBJECT_SCHEMA,
    TABLE_NAME AS OBJECT_NAME,
    TABLE_TYPE AS OBJECT_TYPE,
	ROUND((DATA_LENGTH+INDEX_LENGTH)/POWER(1024,2),2) AS OBJECT_SIZE
FROM KIPITHON_DB.LANDING.SCHEMA_MEMORY_DETAILS_STG;

---------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.DB_QUERY_TABLE_TYPE --- SAMPLE_DB.REPORTING.ACCESS_COUNT_TBL 
AS
SELECT 
    AC.DB_NAME AS DB_NAME,
    AC.TABLE_NAME AS TABLE_NAME, 
    AC.EXEC_COUNT AS EXEC_COUNT, 
    RL.OBJECT_TYPE AS TABLE_TYPE
FROM KIPITHON_DB.LANDING.QUERY_HISTORY_RESULTS_EXTRACT AC
JOIN KIPITHON_DB.REPORTING.SCHEMA_MEMORY_DETAILS RL
ON AC.TABLE_NAME=RL.OBJECT_NAME AND AC.DB_NAME=RL.OBJECT_SCHEMA;

---------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.DB_OBJECT_OVERVIEW --- SAMPLE_DB.REPORTING.DB_OBJECT_OVERVIEW
AS
SELECT 
    DB AS DB_NAME,
    TRIM(object_type,'"') AS OBJECT_TYPE, 
    COUNT 
FROM KIPITHON_DB.LANDING.DB_OBJECT_OVERVIEW_STG;

---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.SCHEMA_TOTAL_MEMORY_DETAILS --- SAMPLE_DB.REPORTING.DB_SIZE_TBL
AS
SELECT 
    TABLE_SCHEMA as OBJECT_TYPE,
    SUM(ROUND((DATA_LENGTH+INDEX_LENGTH)/POWER(1024,2),2)) AS OBJECT_SIZE
FROM KIPITHON_DB.LANDING.SCHEMA_MEMORY_DETAILS_STG
GROUP BY TABLE_SCHEMA;

---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.DB_HOST_SUMMARY
AS
SELECT 
	STATEMENTS,
	STATEMENT_LATENCY,
	TABLE_SCANS,
	TOTAL_CONNECTIONS,
	CURRENT_MEMORY,
	TOTAL_MEMORY_ALLOCATED,
	INGEST_DATE
FROM KIPITHON_DB.LANDING.DB_HOST_SUMMARY_STG
;

---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW KIPITHON_DB.REPORTING.DB_HOST_SUMMARY
CREATE OR REPLACE TABLE KIPITHON_DB.REPORTING.CREDENTIALS ( --- SAHIL_DB.credentials table
    USERNAME VARCHAR NOT NULL,
    NAME VARCHAR,
    PASSWORD VARCHAR,
    EMAIL VARCHAR,
    PRIMARY KEY (USERNAME)
);
