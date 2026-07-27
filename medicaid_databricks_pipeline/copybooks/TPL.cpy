      ******************************************************************
      * TPL-RECORD
      * MEDICAID THIRD PARTY LIABILITY / COB EXTRACT
      * SOURCE FILE: TPL.txt   RECORD LENGTH: 230
      ******************************************************************
       01  TPL-RECORD.
           05  TPL-TPL-ID                   PIC X(10).
           05  TPL-MEMBER-ID                PIC X(10).
           05  TPL-MEDICAID-ID              PIC X(12).
           05  TPL-CARRIER-NAME             PIC X(30).
           05  TPL-CARRIER-CODE             PIC X(6).
           05  TPL-CARRIER-ADDRESS          PIC X(30).
           05  TPL-CARRIER-CITY             PIC X(20).
           05  TPL-CARRIER-STATE            PIC X(2).
           05  TPL-CARRIER-ZIP              PIC 9(9).
           05  TPL-CARRIER-PHONE            PIC 9(10).
           05  TPL-POLICY-NUMBER            PIC X(15).
           05  TPL-GROUP-NUMBER             PIC X(12).
           05  TPL-SUBSCRIBER-ID            PIC X(12).
           05  TPL-RELATIONSHIP-CODE        PIC X(2).
           05  TPL-COVERAGE-TYPE            PIC X(2).
           05  TPL-PLAN-TYPE                PIC X(3).
           05  TPL-EFFECTIVE-DATE           PIC 9(8).
           05  TPL-TERM-DATE                PIC 9(8).
           05  TPL-COB-INDICATOR            PIC X(1).
           05  TPL-VERIFICATION-DATE        PIC 9(8).
           05  TPL-VERIFICATION-SOURCE      PIC X(3).
           05  TPL-VERIFICATION-STATUS      PIC X(1).
           05  TPL-LAST-UPDATE-DATE         PIC 9(8).
           05  TPL-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(5).
