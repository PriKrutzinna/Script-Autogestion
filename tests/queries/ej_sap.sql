SELECT
  CAST(ST."GCARTNO" AS BIGINT) AS "GCARTNO",
  LCBATCHP BatchNumber,
  ST.LCSTORLOC StockStorage,
  ST.LCBATCHS__LCVFDAT DateBatchExpiry,
  ST.LCSTDPRCE AS STDPrice, 
  SUM(ST.LCCSPEM) AS BlockedStock,
  SUM(ST.LCCRETM) AS BlockedStockReturns,
  SUM(ST.LCCEINM) AS NotFreeStock,
  SUM(ST.LCCINSM) AS StockInQualityInspection,
  SUM(ST.LCCLABS) AS Total_Stock_Unrestricted
FROM  _SYS_BIC."system-local.bw.bw2hana/GLAL01C" AS MM
     LEFT JOIN _SYS_BIC."system-local.bw.bw2hana/LCMISTC" ST
        ON MM.GLCOMPANY=ST.LCCOMPANY
        AND MM.GLARTNO=ST."GCARTNO"
        AND ST.LCSTORLOC IN ('UY31','UY33')
        AND ST."0CALMONTH"=(SELECT MAX(STS."0CALMONTH") "0CALMONTH"
                            FROM _SYS_BIC."system-local.bw.bw2hana/LCMISTC" STS
                            WHERE STS."0CALMONTH"<=TO_VARCHAR(CURRENT_DATE,'YYYYMM')
                            AND (STS.LCCOMPANY='6256')
                            AND STS.LCSTORLOC IN ('UY31','UY33')) 
WHERE (MM."GLCOMPANY"='6256')
AND ST.LCSTORLOC IN ('UY31','UY33')
AND MM."GLMSTATPL"='AC'
GROUP BY
      CAST(ST."GCARTNO" AS BIGINT),
      LCBATCHP,
      ST.LCSTORLOC ,
      ST.LCBATCHS__LCVFDAT,
      ST.LCSTDPRCE