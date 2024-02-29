CREATE OR REPLACE TRIGGER RAW_DATA_ID
AFTER INSERT ON RAW_FOOTBALLERS_DATA
DECLARE
    TYPE foot_r is RECORD (
        foots_id    RAW_FOOTBALLERS_DATA.FOOT_ID%TYPE
        , r_num     NUMBER
    );
    
    TYPE foot_ids IS TABLE OF foot_r;
    footballers foot_ids;
BEGIN
    SELECT FOOT_ID
    , ROW_NUMBER() OVER(ORDER BY FOOT_ID) r_num
    BULK COLLECT INTO footballers
    FROM RAW_FOOTBALLERS_DATA;
    
    FORALL INDX IN 1 .. footballers.COUNT
        UPDATE RAW_FOOTBALLERS_DATA
            SET AGE = footballers(INDX).r_num
            WHERE FOOT_ID = footballers(INDX).foots_id;
    
END;


CREATE OR REPLACE PROCEDURE PROCESS_RAW_DATA (
    raw_tab_name VARCHAR2
)
IS
    l_sql CLOB := 'EMPTY';
    g_crlf CONSTANT VARCHAR(1) := CHR(10);
    TYPE cols IS TABLE OF VARCHAR2(100);
    tab_cols cols;
    pk_cols cols;
    
    dest_tab_name VARCHAR2(50) := SUBSTR(raw_tab_name,5);
    
    CURSOR pk_check (tab_name VARCHAR2)
    IS
    SELECT a.COLUMN_NAME
            FROM all_cons_columns a
            JOIN all_constraints b
            ON a.CONSTRAINT_NAME = b.CONSTRAINT_NAME
            where a.table_name = UPPER(tab_name)
            and b.CONSTRAINT_TYPE = 'P';
    
    FUNCTION CONCAT_STRINGS (
        to_merge IN cols
    ) RETURN VARCHAR2 DETERMINISTIC
    AS
        p_result VARCHAR2(4000);
    BEGIN
        FOR indx IN 1 .. to_merge.COUNT
        LOOP
            p_result :=  p_result||',rfd.'||to_merge(indx);
        END LOOP;
        RETURN SUBSTR(p_result,2);
    END;
BEGIN
    l_sql := DBMS_ASSERT.SQL_OBJECT_NAME(raw_tab_name);
    l_sql := 'SELECT COLUMN_NAME '
            || g_crlf || 'FROM ALL_TAB_COLUMNS'
            || g_crlf || 'WHERE TABLE_NAME = ' || DBMS_ASSERT.ENQUOTE_LITERAL(l_sql);
    execute immediate l_sql bulk collect into tab_cols;
    
    l_sql := DBMS_ASSERT.SQL_OBJECT_NAME(dest_tab_name);
    l_sql := 'MERGE INTO ' || l_sql || ' fd'
    || g_crlf || 'USING ' || raw_tab_name || ' rfd'
    || g_crlf || 'ON (';
    
    open pk_check(raw_tab_name);
    LOOP
        FETCH pk_check BULK COLLECT INTO pk_cols LIMIT 100;
        exit when pk_check%NOTFOUND;
    END LOOP;
    FOR indx IN 1 .. pk_cols.COUNT
    LOOP
        l_sql := l_sql || 'rfd.' || pk_cols(indx) || '= fd.' || pk_cols(indx)
            || g_crlf || 'and ';
    END LOOP;
    
    l_sql := SUBSTR(l_sql, 0, LENGTH(l_sql)-4) || ' )'
    || g_crlf || ' WHEN MATCHED THEN'
    || g_crlf ||    'UPDATE SET ';
        FOR indx in 1 .. tab_cols.COUNT
        LOOP
            IF not tab_cols(indx) MEMBER OF pk_cols then
                l_sql := l_sql || 'fd.' || tab_cols(indx)
                 || '= rfd.' || tab_cols(indx) 
                 || g_crlf || ', ';
            end if;
        END LOOP;
    l_sql := SUBSTR(l_sql, 0, LENGTH(l_sql) - 2) || 'WHEN NOT MATCHED THEN'
    || g_crlf || 'INSERT VALUES(' || concat_strings(tab_cols) || ')';
    
    execute immediate l_sql;
    COMMIT;
    
    EXCEPTION
        WHEN DBMS_ASSERT.INVALID_OBJECT_NAME THEN
            RAISE_APPLICATION_ERROR(-20130, 'Code near below sql expression failed '
                                || g_crlf || l_sql 
                                || G_CRLF ||  'with oracle error :'
                                || g_crlf || SQLERRM);
    
END;


BEGIN
DBMS_OUTPUT.PUT_LINE(DBMS_ASSERT.SQL_OBJECT_NAME('RAW_FOOTBALLERS_DATA'));
EXCEPTION
    WHEN DBMS_ASSERT.INVALID_OBJECT_NAME THEN
        RAISE_APPLICATION_ERROR(-20120,'ERROR OCCUERED' || DBMS_UTILITY.FORMAT_ERROR_STACK);
END;


BEGIN
    PROCESS_RAW_DATA('RAW3_FOOTBALLERS_DATA');
END;

TRUNCATE TABLE FOOTBALLERS_DATA;




    
    
    





