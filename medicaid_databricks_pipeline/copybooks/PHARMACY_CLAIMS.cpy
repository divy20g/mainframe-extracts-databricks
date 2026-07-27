      ******************************************************************
      * PHARMACY-CLAIM-RECORD
      * MEDICAID PHARMACY (NCPDP-DERIVED) CLAIMS EXTRACT
      * SOURCE FILE: PHARMACY_CLAIMS.txt   RECORD LENGTH: 270
      ******************************************************************
       01  PHARMACY-CLAIM-RECORD.
           05  RXC-RX-CLAIM-ID              PIC X(12).
           05  RXC-MEMBER-ID                PIC X(10).
           05  RXC-MEDICAID-ID              PIC X(12).
           05  RXC-PHARMACY-NPI             PIC 9(10).
           05  RXC-PHARMACY-NCPDP-ID        PIC X(7).
           05  RXC-PRESCRIBER-NPI           PIC 9(10).
           05  RXC-PRESCRIBER-DEA           PIC X(9).
           05  RXC-NDC-CODE                 PIC X(11).
           05  RXC-DRUG-NAME                PIC X(30).
           05  RXC-DRUG-STRENGTH            PIC X(10).
           05  RXC-DOSAGE-FORM-CODE         PIC X(2).
           05  RXC-GCN-SEQUENCE-NUMBER      PIC X(6).
           05  RXC-THERAPEUTIC-CLASS-CODE   PIC X(6).
           05  RXC-FILL-DATE                PIC 9(8).
           05  RXC-RX-NUMBER                PIC X(12).
           05  RXC-REFILL-NUMBER            PIC 9(2).
           05  RXC-DAYS-SUPPLY              PIC 9(3).
           05  RXC-QUANTITY-DISPENSED       PIC 9(5)V9(3).
           05  RXC-INGREDIENT-COST          PIC 9(7)V9(2).
           05  RXC-DISPENSING-FEE           PIC 9(5)V9(2).
           05  RXC-SALES-TAX                PIC 9(4)V9(2).
           05  RXC-INCENTIVE-FEE            PIC 9(4)V9(2).
           05  RXC-COPAY-AMOUNT             PIC 9(4)V9(2).
           05  RXC-TPL-AMOUNT               PIC 9(5)V9(2).
           05  RXC-PAID-AMOUNT              PIC 9(7)V9(2).
           05  RXC-DAW-CODE                 PIC X(1).
           05  RXC-COMPOUND-CODE            PIC X(1).
           05  RXC-PRIOR-AUTH-NUMBER        PIC X(12).
           05  RXC-CLAIM-STATUS             PIC X(1).
           05  RXC-REVERSAL-INDICATOR       PIC X(1).
           05  RXC-RECEIVED-DATE            PIC 9(8).
           05  RXC-PAID-DATE                PIC 9(8).
           05  RXC-LAST-UPDATE-DATE         PIC 9(8).
           05  RXC-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(9).
