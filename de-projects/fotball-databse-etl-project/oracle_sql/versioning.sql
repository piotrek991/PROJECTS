DROP TABLE FOOTBALLERS_HISTORY;

CREATE TABLE FOOTBALLERS_HISTORY (
    FOOTBALLER_ID NUMBER,
    TEAM_ID NUMBER,
    VALID_SINCE DATE NOT NULL,
    VALID_TILL DATE DEFAULT SYSDATE NULL,
    CONSTRAINT FH_PK PRIMARY KEY(FOOTBALLER_ID,VALID_SINCE)
)

CREATE OR REPLACE PROCEDURE new_fh_version (
    foot_id in footballers_history.footballer_id%TYPE,
    team_id in footballers_history.team_id%TYPE,
    valid_since in footballers_history.valid_since%TYPE
)
IS
    TYPE valids_t2 is record(
        valid_till_p footballers_history.valid_till%TYPE,
        valid_till_f footballers_history.valid_till%TYPE
    );
    valids_data valids_t2;
    foot_rec footballers_history%ROWTYPE;
    check_rows smallint;
    
    no_data_to_update EXCEPTION;
    PRAGMA EXCEPTION_INIT(no_data_to_update, -900);
    
BEGIN
    BEGIN
        SELECT a.*
        INTO foot_rec
        FROM FOOTBALLERS_HISTORY a
        WHERE a.footballer_id = foot_id
        AND a.valid_since = new_fh_version.valid_since;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                foot_rec := null;
    END;
    
    DBMS_OUTPUT.PUT_LINE('here');
    IF foot_rec.footballer_id is not null and 
        foot_rec.team_id = new_fh_version.team_id then
        DBMS_OUTPUT.PUT_LINE('here1');
        RAISE no_data_to_update;
    ELSIF foot_rec.footballer_id is not null and 
        foot_rec.team_id <> new_fh_version.team_id then
        DBMS_OUTPUT.PUT_LINE('here2');
        UPDATE FOOTBALLERS_HISTORY a
        SET a.team_id = new_fh_version.team_id
        WHERE a.footballer_id = new_fh_version.foot_id
        AND a.valid_since = new_fh_version.valid_since;
    ELSE
       DBMS_OUTPUT.PUT_LINE('HERE');
       SELECT MAX(aa.valid_since) 
       ,MAX(aa.next_val_since) LEAD_SINCE
       INTO valids_data.valid_till_p,
            valids_data.valid_till_f
            FROM (
                SELECT a.valid_since
                        , LEAD(a.valid_since,1) OVER(PARTITION BY a.footballer_id order by a.valid_since) next_val_since
                        FROM FOOTBALLERS_HISTORY a
                        WHERE a.footballer_id = new_fh_version.foot_id
                        ) aa
                WHERE aa.valid_since < new_fh_version.valid_since;
        UPDATE FOOTBALLERS_HISTORY fh
        SET fh.valid_till = new_fh_version.valid_since - interval '1' day
        WHERE fh.valid_since = valids_data.valid_till_p
            AND fh.footballer_id = new_fh_version.foot_id;
        DBMS_OUTPUT.PUT_LINE('here with data p : '||valids_data.valid_till_p||' and f :'||valids_data.valid_till_f);
        INSERT INTO footballers_history 
            VALUES (foot_id, new_fh_version.team_id, new_fh_version.valid_since, valids_data.valid_till_f - interval '1' day);    
    end if; 
    EXCEPTION
        WHEN no_data_to_update THEN
            DBMS_OUTPUT.PUT_LINE('theres no data to update - row with exact data exists');
        WHEN OTHERS then
            DBMS_OUTPUT.PUT_LINE('different erroc occured');
END;


insert all
INTO footballers_history values (1,1,SYSDATE, ADD_MONTHS(SYSDATE,2) - INTERVAL '1' DAY)
INTO footballers_history values (1,1,ADD_MONTHS(SYSDATE,2), ADD_MONTHS(SYSDATE,4) - INTERVAL '1' DAY)
INTO footballers_history values (1,1,ADD_MONTHS(SYSDATE,4), ADD_MONTHS(SYSDATE,6) - INTERVAL '1' DAY)
SELECT 1 FROM DUAL;

BEGIN
 new_fh_version(1,1,'2024/01/18');
END;
    
    


