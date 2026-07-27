      ******************************************************************
      * REFERENCE-RECORD
      * MEDICAID REFERENCE / CODE TABLE EXTRACT
      * SOURCE FILE: REFERENCE.txt   RECORD LENGTH: 180
      ******************************************************************
       01  REFERENCE-RECORD.
           05  REF-REFERENCE-TABLE-ID       PIC X(6).
           05  REF-CODE-VALUE               PIC X(10).
           05  REF-SHORT-DESCRIPTION        PIC X(30).
           05  REF-LONG-DESCRIPTION         PIC X(60).
           05  REF-CODE-CATEGORY            PIC X(4).
           05  REF-PARENT-CODE              PIC X(10).
           05  REF-EFFECTIVE-DATE           PIC 9(8).
           05  REF-TERMINATION-DATE         PIC 9(8).
           05  REF-ACTIVE-INDICATOR         PIC X(1).
           05  REF-FEDERAL-CODE-INDICATOR   PIC X(1).
           05  REF-STATE-SPECIFIC-INDICATOR PIC X(1).
           05  REF-REIMBURSABLE-INDICATOR   PIC X(1).
           05  REF-PRIOR-AUTH-REQUIRED-INDICATOR PIC X(1).
           05  REF-AGE-RESTRICTION-MIN      PIC 9(3).
           05  REF-AGE-RESTRICTION-MAX      PIC 9(3).
           05  REF-GENDER-RESTRICTION       PIC X(1).
           05  REF-RATE-AMOUNT              PIC 9(7)V9(2).
           05  REF-UNIT-OF-MEASURE          PIC X(2).
           05  REF-SORT-ORDER               PIC 9(4).
           05  REF-LAST-UPDATE-DATE         PIC 9(8).
           05  REF-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(6).
