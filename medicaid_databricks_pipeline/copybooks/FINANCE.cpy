      ******************************************************************
      * FINANCE-TRANSACTION-RECORD
      * MEDICAID FINANCIAL TRANSACTION EXTRACT
      * SOURCE FILE: FINANCE.txt   RECORD LENGTH: 220
      ******************************************************************
       01  FINANCE-TRANSACTION-RECORD.
           05  FIN-TRANSACTION-ID           PIC X(14).
           05  FIN-CLAIM-ID                 PIC X(13).
           05  FIN-MEMBER-ID                PIC X(10).
           05  FIN-PROVIDER-ID              PIC X(10).
           05  FIN-PAYEE-ID                 PIC X(10).
           05  FIN-TRANSACTION-TYPE         PIC X(2).
           05  FIN-TRANSACTION-SUBTYPE      PIC X(3).
           05  FIN-TRANSACTION-DATE         PIC 9(8).
           05  FIN-POSTING-DATE             PIC 9(8).
           05  FIN-AMOUNT                   PIC S9(9)V9(2)
                                        SIGN IS LEADING SEPARATE CHARACTER.
           05  FIN-PAYMENT-METHOD-CODE      PIC X(2).
           05  FIN-CHECK-EFT-NUMBER         PIC X(12).
           05  FIN-CHECK-DATE               PIC 9(8).
           05  FIN-VOID-INDICATOR           PIC X(1).
           05  FIN-VOID-DATE                PIC 9(8).
           05  FIN-GL-CODE                  PIC X(8).
           05  FIN-COST-CENTER              PIC X(6).
           05  FIN-FUND-CODE                PIC X(4).
           05  FIN-FISCAL-YEAR              PIC 9(4).
           05  FIN-FISCAL-PERIOD            PIC 9(2).
           05  FIN-BATCH-NUMBER             PIC X(10).
           05  FIN-WARRANT-NUMBER           PIC X(10).
           05  FIN-VENDOR-ID                PIC X(10).
           05  FIN-FEDERAL-SHARE-AMOUNT     PIC 9(9)V9(2).
           05  FIN-STATE-SHARE-AMOUNT       PIC 9(9)V9(2).
           05  FIN-RECOUPMENT-REASON-CODE   PIC X(4).
           05  FIN-LAST-UPDATE-DATE         PIC 9(8).
           05  FIN-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(8).
