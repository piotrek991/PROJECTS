CREATE OR REPLACE VIEW &NEW_USER..RPT_CBB_TABALLITEMS_VW AS
SELECT  CASE WHEN AA.RU_ID IN ('RU001','RU008') THEN R.RU_NAME||':'||NVL(AA.COMPUTER_NAME,R.SERVICE)
			WHEN AA.RU_ID = 'RU007' THEN 'EWM_Sec_PrFW:'||NVL(AA.COMPUTER_NAME,R.SERVICE)
			WHEN AA.RU_ID IN ('RU009','RU005') THEN R.RU_NAME||':'||AA.MAIL
			WHEN AA.RU_ID = 'RU002' THEN  R.RU_NAME||':'||NVL(AA.APPLICATION_NAME,'Minimum Volume Software Packaging Low') 
            WHEN AA.RU_ID = 'RU003' THEN  R.RU_NAME||':'||NVL(AA.APPLICATION_NAME,'Minimum Volume Software Packaging Medium')
			WHEN AA.RU_ID = 'RU004' THEN R.RU_NAME||':'||AA.APPLICATION_NAME
            WHEN AA.RU_ID = 'RU011' THEN R.RU_NAME||':'||NVL(AA.USER_ID,'Minimum Volume ServiceNow IT Service Management Fulfiller')
            WHEN AA.RU_ID = 'RU012' THEN R.RU_NAME||':'||NVL(AA.USER_ID,'Minimum Volume ServiceNow Business Stakeholder User ')
            ELSE R.RU_NAME||':'||R.SERVICE
            END 						                                         LIFETIMEID
    , CONCAT(CAL.M || '-', LPAD(TO_CHAR(ROW_NUMBER() OVER (ORDER BY R.RU_ID)),6,'0'))   LINETIMEID
    , SUBSTR(CAL.M,0,4)                                                          CBBREPORTYEAR
    , SUBSTR(CAL.M,6,2)                                                          CBBREPORTMONTH
	, R.TOWER                                                                    TOWER
    , R.RU_NAME                                                                  PRICE_ID_CBB
    , R.SERVICE                                                                  PRODUCT_NAME
    , CASE WHEN R.RU_ID IN ('RU001','RU008','RU007') THEN AA.COMPUTER_NAME 
			WHEN AA.RU_ID = 'RU002' THEN  NVL(AA.APPLICATION_NAME,'Minimum Volume Software Packaging Low') 
            WHEN AA.RU_ID = 'RU003' THEN  NVL(AA.APPLICATION_NAME,'Minimum Volume Software Packaging Medium')
			WHEN AA.RU_ID = 'RU004' THEN AA.APPLICATION_NAME
            WHEN R.RU_ID = 'RU010' THEN  'Service management' 
            WHEN R.RU_ID = 'RU011' THEN NVL(AA.USER_ID,'Minimum Volume ServiceNow IT Service Management Fulfiller')
            WHEN R.RU_ID = 'RU012' THEN NVL(AA.USER_ID,'Minimum Volume ServiceNow Business Stakeholder User ')
			ELSE AA.MAIL END 								                     SYSTEM_NAME                                                           
    , CASE WHEN AA.RU_ID = 'RU005' THEN AA.MAIL ELSE NULL END                    USER_PRINCIPAL_NAME
    , NULL                                                                       SAM_ACCOUNT_NAME
    , AA.CLIENT_ACTIVITY                                                         STATUS
    , NULL                                                                       LAST_ACTIVITY_DATE
    , AA.COMPUTER_NAME                                                           COMPUTER_NAME
	, NULL                                                                       SERIAL_NUMBER
    , AA.QUANTITY                                                                 VOLUME
    , CASE WHEN R.PRICING_MODEL = 'A' THEN ROUND(AGG.ARCRRC_PRICE,2)
           WHEN R.PRICING_MODEL IN ('U','F') THEN ROUND(AGG.BASELINE_UNIT_PRICE,2)
           END   UNIT_PRICE
    , CASE WHEN R.PRICING_MODEL = 'A' 
                    THEN ROUND(AGG.ARCRRC_PRICE * AA.QUANTITY,2)
           WHEN R.PRICING_MODEL IN ('U','F') 
                    THEN ROUND(AGG.BASELINE_UNIT_PRICE * AA.QUANTITY,2)
           END   AMOUNT
FROM (
    SELECT F.RU_ID, F.QUANTITY,F.COMPUTER_NAME,F.MAIL,F.USER_ID,F.CLIENT_ACTIVITY,F.APPLICATION_NAME
    FROM DISTRELEC.FACTS F
    WHERE (F.ROW_STATUS_ID = FRAMEWORK.CTL_DATA_STATUSES_PKG.GET_STATUS_ID_APPROVED()
			OR F.ROW_STATUS_ID = FRAMEWORK.CTL_DATA_STATUSES_PKG.GET_STATUS_ID_INVOICED())
    AND F.BILLINGPERIOD = framework.CTL_Session_Parameters_PKG.GET_BillingPeriod()
        UNION ALL
    SELECT AGG.RU_ID, NVL(AGG.ARCRRC_QUANTITY,AGG.DELIVERED_QUANTITY) - NVL(A.HOW_MANY,0),NULL,NULL,NULL,NULL,NULL
    FROM DISTRELEC.RPT_AGG_CHARGES_SUMMARY_VW AGG
    LEFT JOIN (
        SELECT F.RU_ID, SUM(F.QUANTITY) HOW_MANY
        FROM DISTRELEC.FACTS F
        WHERE (F.ROW_STATUS_ID = FRAMEWORK.CTL_DATA_STATUSES_PKG.GET_STATUS_ID_APPROVED()
			OR F.ROW_STATUS_ID = FRAMEWORK.CTL_DATA_STATUSES_PKG.GET_STATUS_ID_INVOICED())
        AND F.BILLINGPERIOD = framework.CTL_Session_Parameters_PKG.GET_BillingPeriod()
        GROUP BY F.RU_ID
    ) A
        ON A.RU_ID = AGG.RU_ID
    WHERE ( NVL(AGG.ARCRRC_QUANTITY,AGG.DELIVERED_QUANTITY) - NVL(A.HOW_MANY,0)) > 0
) AA
LEFT JOIN DISTRELEC.DIM_RESOURCEUNITS_VW R
    ON AA.RU_ID = R.RU_ID
LEFT JOIN (
    SELECT TO_CHAR(FRAMEWORK.DIM_CALENDAR_PKG.GET_StartDate(),'YYYY-MM') M FROM DUAL
) CAL ON 1=1
LEFT JOIN DISTRELEC.RPT_AGG_CHARGES_SUMMARY_VW AGG
        ON R.RU_ID = AGG.RU_ID
WHERE R.RU_ID <> 'RU006';

----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------

CREATE OR REPLACE VIEW &NEW_USER..RPT_CBB_CBBTOTAL_VW AS
SELECT R.TOWER 		"Tower"
    , R.RU_NAME 	"Price_ID_CBB"
    , R.SERVICE 	"Product"
    , R.UNIT_MEASURE 		"Accounting_Unit"
    , WBS.WBS_ID  			"WBS"
    , DECODE(R.RU_NAME,
        'EWM_InTune_MDM','EWM_InTune_MDM',
        'EWM_SCCM','EWM_SCCM',
        'EWM_Sec_Encr','EWM_Sec_Encr',
        'EWM_Sec_EndPoint_PrFW','EWM_Sec_PrFW',
        'EWM_Sec_PrPoint','EWM_Sec_PrPoint',
        'EWM_SD','EWM_SD',
        'EWM_SM_FIX','FIX',
        'EWM_SNOW_BSU','EWM_SNOW_BSU',
        'EWM_SNOW_SMFF','EWM_SNOW_SMFF',
        'EWM_Package_High','EWM_PH',
        'EWM_Package_Low','EWM_PL',
        'EWM_Package_Medium','EWM_PM'
    )		"LTID_Prefix"
    , ROUND(NVL(PXQ_BAS.BASELINE_CHARGE,NVL(PXQ_PRC.UNIT_PRICE,ARC_PRC.UNIT_PRICE)),2)      "Unit_Price"
    , NVL(RU_BASE.BASELINE_VOLUME,0)       "Baselinevolumes"
    , NVL(RU_BASE.BANDWIDTH,0)             "Bandwidth"
	, NVL(RU_BASE.FLOOR,0)                 "Floor"
    , NVL(RU_BASE.CEILING,0)               "Ceiling"
    , CASE WHEN R.PRICING_MODEL = 'A' THEN AGG.FLOOR_QUANTITY
           WHEN R.PRICING_MODEL IN ('U','F') THEN 1
     END                                                        "MinimumBaselineVolumes"
    , NVL(AGG_PAST.DELIVERED_QUANTITY,0)                               "prev_Invoiced_Volume"
    , NVL(CASE WHEN R.PRICING_MODEL = 'A' THEN AGG.ARCRRC_QUANTITY
        WHEN R.PRICING_MODEL IN ('U','F') THEN AGG.DELIVERED_QUANTITY
        END,0)                                                   "Invoiced_Volume"
    , NVL((CASE WHEN R.PRICING_MODEL = 'A' THEN AGG.ARCRRC_QUANTITY
        WHEN R.PRICING_MODEL IN ('U','F') THEN AGG.DELIVERED_QUANTITY
        END) - AGG_PAST.DELIVERED_QUANTITY,0)                   "Delta_Volume"
    , ROUND(NVL(100/RU_BASE.BASELINE_VOLUME * (CASE WHEN R.PRICING_MODEL = 'A' THEN AGG.ARCRRC_QUANTITY
        WHEN R.PRICING_MODEL IN ('U','F') THEN AGG.DELIVERED_QUANTITY
        END),0),2)                              "Pct_Baseline"
    , ROUND(NVL(AGG.TOTAL_CHARGE,0),2)       "Amount"
    FROM DISTRELEC.DIM_RESOURCEUNITS_VW R
	LEFT JOIN DISTRELEC.REF_WBSES_VW WBS
		ON R.RU_ID = WBS.RU_ID
    LEFT JOIN DISTRELEC.RPT_AGG_CHARGES_SUMMARY_VW AGG
        ON R.RU_ID = AGG.RU_ID
    LEFT JOIN (
        SELECT R.RU_ID
        , NVL(B.ARCRRC_QUANTITY,NVL(A.DELIVERED_QUANTITY,C.DELIVERED_QUANTITY)) DELIVERED_QUANTITY
        FROM DISTRELEC.DIM_RESOURCEUNITS_VW R
        LEFT JOIN DISTRELEC.AGG_FACTS_QUANTITIES A
            ON R.RU_ID = A.RU_ID AND A.BILLINGPERIOD = FRAMEWORK.DIM_CALENDAR_PKG.ADD_BillingPeriods(-1)
        LEFT JOIN DISTRELEC.AGG_FACTS_ARCRRC_CHARGES B
            ON R.RU_ID = B.RU_ID AND B.BILLINGPERIOD = FRAMEWORK.DIM_CALENDAR_PKG.ADD_BillingPeriods(-1)
        LEFT JOIN DISTRELEC.AGG_FACTS_PXQ_CHARGES C
            ON R.RU_ID = C.RU_ID AND C.BILLINGPERIOD = FRAMEWORK.DIM_CALENDAR_PKG.ADD_BillingPeriods(-1)
    ) AGG_PAST ON
        R.RU_ID = AGG_PAST.RU_ID
    LEFT JOIN DISTRELEC.REF_PXQ_BASELINES_VW PXQ_BAS
        ON R.RU_ID = PXQ_BAS.RU_ID
    LEFT JOIN DISTRELEC.REF_PXQ_PRICES_VW PXQ_PRC
        ON R.RU_ID = PXQ_PRC.RU_ID
    LEFT JOIN  DISTRELEC.REF_ARCRRC_PRICES_VW ARC_PRC
        ON R.RU_ID = ARC_PRC.RU_ID
    LEFT JOIN DISTRELEC.REF_RU_BASELINE_VW RU_BASE
        ON R.RU_ID = RU_BASE.RU_ID; 