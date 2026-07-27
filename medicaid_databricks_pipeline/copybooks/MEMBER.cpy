      ******************************************************************
      * MEMBER-RECORD
      * MEDICAID MEMBER ELIGIBILITY EXTRACT
      * SOURCE FILE: MEMBER.txt   RECORD LENGTH: 380
      ******************************************************************
       01  MEMBER-RECORD.
           05  MBR-MEMBER-ID                PIC X(10).
           05  MBR-MEDICAID-ID              PIC X(12).
           05  MBR-CASE-NUMBER              PIC X(10).
           05  MBR-SSN                      PIC 9(9).
           05  MBR-LAST-NAME                PIC X(20).
           05  MBR-FIRST-NAME               PIC X(15).
           05  MBR-MIDDLE-NAME              PIC X(15).
           05  MBR-NAME-SUFFIX              PIC X(4).
           05  MBR-DOB                      PIC 9(8).
           05  MBR-GENDER                   PIC X(1).
           05  MBR-RACE-CODE                PIC X(2).
           05  MBR-ETHNICITY-CODE           PIC X(1).
           05  MBR-MARITAL-STATUS           PIC X(1).
           05  MBR-ADDRESS-LINE1            PIC X(30).
           05  MBR-ADDRESS-LINE2            PIC X(20).
           05  MBR-CITY                     PIC X(20).
           05  MBR-STATE                    PIC X(2).
           05  MBR-ZIP                      PIC 9(9).
           05  MBR-COUNTY-CODE              PIC X(3).
           05  MBR-HOME-PHONE               PIC 9(10).
           05  MBR-CELL-PHONE               PIC 9(10).
           05  MBR-EMAIL                    PIC X(40).
           05  MBR-PREFERRED-LANGUAGE       PIC X(3).
           05  MBR-CITIZENSHIP-CODE         PIC X(1).
           05  MBR-IMMIGRATION-STATUS       PIC X(2).
           05  MBR-AID-CATEGORY             PIC X(3).
           05  MBR-ELIGIBILITY-STATUS       PIC X(1).
           05  MBR-ELIGIBILITY-START        PIC 9(8).
           05  MBR-ELIGIBILITY-END          PIC 9(8).
           05  MBR-RE-CODE                  PIC X(4).
           05  MBR-MCO-PLAN-ID              PIC X(8).
           05  MBR-PCP-PROVIDER-ID          PIC X(10).
           05  MBR-LOC-CODE                 PIC X(2).
           05  MBR-SPENDDOWN-AMOUNT         PIC 9(7)V9(2).
           05  MBR-MEDICARE-ID              PIC X(12).
           05  MBR-MEDICARE-PART-A-IND      PIC X(1).
           05  MBR-MEDICARE-PART-B-IND      PIC X(1).
           05  MBR-MEDICARE-PART-D-IND      PIC X(1).
           05  MBR-DUAL-ELIGIBLE-CODE       PIC X(2).
           05  MBR-INSTITUTIONAL-STATUS     PIC X(1).
           05  MBR-WAIVER-PROGRAM-CODE      PIC X(3).
           05  MBR-CASEWORKER-ID            PIC X(8).
           05  MBR-HOUSEHOLD-SIZE           PIC 9(2).
           05  MBR-FPL-PERCENT              PIC 9(3).
           05  MBR-DECEASED-INDICATOR       PIC X(1).
           05  MBR-DEATH-DATE               PIC 9(8).
           05  MBR-LAST-UPDATE-DATE         PIC 9(8).
           05  MBR-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(15).
