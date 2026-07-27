      ******************************************************************
      * DRUG-REBATE-RECORD
      * MEDICAID DRUG REBATE PROGRAM (MDRP) EXTRACT
      * SOURCE FILE: DRUG_REBATE.txt   RECORD LENGTH: 260
      ******************************************************************
       01  DRUG-REBATE-RECORD.
           05  REB-REBATE-RECORD-ID         PIC X(14).
           05  REB-NDC-CODE                 PIC X(11).
           05  REB-DRUG-NAME                PIC X(30).
           05  REB-LABELER-CODE             PIC X(5).
           05  REB-MANUFACTURER-NAME        PIC X(30).
           05  REB-REBATE-QUARTER           PIC X(1).
           05  REB-REBATE-YEAR              PIC 9(4).
           05  REB-UNITS-REIMBURSED         PIC 9(9)V9(3).
           05  REB-NUMBER-OF-PRESCRIPTIONS  PIC 9(7).
           05  REB-TOTAL-AMOUNT-REIMBURSED  PIC 9(9)V9(2).
           05  REB-INGREDIENT-COST-PAID     PIC 9(9)V9(2).
           05  REB-DISPENSING-FEES-PAID     PIC 9(9)V9(2).
           05  REB-AMP-AMOUNT               PIC 9(5)V9(4).
           05  REB-BEST-PRICE-AMOUNT        PIC 9(5)V9(4).
           05  REB-URA-AMOUNT               PIC 9(5)V9(4).
           05  REB-CPI-PENALTY-AMOUNT       PIC 9(7)V9(2).
           05  REB-REBATE-AMOUNT-INVOICED   PIC 9(9)V9(2).
           05  REB-REBATE-AMOUNT-COLLECTED  PIC 9(9)V9(2).
           05  REB-DISPUTE-INDICATOR        PIC X(1).
           05  REB-DISPUTE-REASON-CODE      PIC X(4).
           05  REB-INVOICE-DATE             PIC 9(8).
           05  REB-PAYMENT-DUE-DATE         PIC 9(8).
           05  REB-PAYMENT-RECEIVED-DATE    PIC 9(8).
           05  REB-DRUG-CATEGORY-CODE       PIC X(1).
           05  REB-UNIT-OF-MEASURE          PIC X(2).
           05  REB-STATE-CODE               PIC X(2).
           05  REB-LAST-UPDATE-DATE         PIC 9(8).
           05  REB-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(10).
