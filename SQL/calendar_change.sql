DROP TABLE DIM_CALENDAR;

CREATE TABLE DIM_CALENDAR (
    BILLINGPERIOD VARCHAR2(6 BYTE)
    , CLIENT_ID VARCHAR2(100 BYTE)
);

/

DECLARE
    TYPE periods IS TABLE OF VARCHAR2(6 BYTE);
    bill_periods periods := periods();
    
    billing_base VARCHAR2(1 BYTE) := 'M';
    final_billing VARCHAR2(10 BYTE);
    client_id VARCHAR2(20 BYTE) := 'DISTRELEC';

    desired_number SMALLINT := 100;
BEGIN
    DBMS_output.put_line(final_billing);
    for i in 1..desired_number
    loop
        final_billing := '';
        bill_periods.EXTEND;
        final_billing := RPAD(billing_base,LENGTH(desired_number)-LENGTH(i) + 1,0);

        bill_periods(bill_periods.COUNT) := final_billing||i;
    end loop;
    
    FORALL item IN BILL_PERIODS.FIRST..BILL_PERIODS.LAST
        INSERT INTO DIM_CALENDAR VALUES(bill_periods(item), client_id);
END;