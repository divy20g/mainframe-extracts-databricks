      ******************************************************************
      * PRIOR-AUTH-RECORD
      * MEDICAID PRIOR AUTHORIZATION EXTRACT
      * SOURCE FILE: PRIOR_AUTH.txt   RECORD LENGTH: 180
      ******************************************************************
       01  PRIOR-AUTH-RECORD.
           05  PA-PA-ID                     PIC X(12).
           05  PA-MEMBER-ID                 PIC X(10).
           05  PA-MEDICAID-ID               PIC X(12).
           05  PA-REQUESTING-PROVIDER-ID    PIC X(10).
           05  PA-SERVICING-PROVIDER-ID     PIC X(10).
           05  PA-SERVICE-TYPE              PIC X(3).
           05  PA-PA-TYPE                   PIC X(2).
           05  PA-DIAGNOSIS-CODE-1          PIC X(7).
           05  PA-DIAGNOSIS-CODE-2          PIC X(7).
           05  PA-PROCEDURE-CODE            PIC X(5).
           05  PA-MODIFIER                  PIC X(2).
           05  PA-REVENUE-CODE              PIC X(4).
           05  PA-NDC-CODE                  PIC X(11).
           05  PA-REQUESTED-UNITS           PIC 9(5).
           05  PA-APPROVED-UNITS            PIC 9(5).
           05  PA-REQUESTED-DATE            PIC 9(8).
           05  PA-DECISION-DATE             PIC 9(8).
           05  PA-DECISION-STATUS           PIC X(1).
           05  PA-DENIAL-REASON-CODE        PIC X(4).
           05  PA-REVIEW-TYPE               PIC X(2).
           05  PA-URGENCY-INDICATOR         PIC X(1).
           05  PA-START-DATE                PIC 9(8).
           05  PA-END-DATE                  PIC 9(8).
           05  PA-EXTENSION-INDICATOR       PIC X(1).
           05  PA-PEER-REVIEW-INDICATOR     PIC X(1).
           05  PA-REVIEWER-ID               PIC X(8).
           05  PA-LAST-UPDATE-DATE          PIC 9(8).
           05  PA-SOURCE-SYSTEM-CODE        PIC X(3).
           05  FILLER                       PIC X(14).
