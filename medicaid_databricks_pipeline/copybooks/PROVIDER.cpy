      ******************************************************************
      * PROVIDER-RECORD
      * MEDICAID PROVIDER ENROLLMENT EXTRACT
      * SOURCE FILE: PROVIDER.txt   RECORD LENGTH: 400
      ******************************************************************
       01  PROVIDER-RECORD.
           05  PRV-PROVIDER-ID              PIC X(10).
           05  PRV-NPI                      PIC 9(10).
           05  PRV-LEGACY-PROVIDER-ID       PIC X(10).
           05  PRV-PROVIDER-NAME            PIC X(35).
           05  PRV-DBA-NAME                 PIC X(35).
           05  PRV-PROVIDER-TYPE            PIC X(2).
           05  PRV-PROVIDER-CATEGORY        PIC X(3).
           05  PRV-SPECIALTY-CODE-1         PIC X(4).
           05  PRV-SPECIALTY-CODE-2         PIC X(4).
           05  PRV-TAXONOMY-CODE            PIC X(10).
           05  PRV-TAX-ID                   PIC 9(9).
           05  PRV-SSN                      PIC 9(9).
           05  PRV-LICENSE-NUMBER           PIC X(15).
           05  PRV-LICENSE-STATE            PIC X(2).
           05  PRV-DEA-NUMBER               PIC X(9).
           05  PRV-ADDRESS-LINE1            PIC X(30).
           05  PRV-ADDRESS-LINE2            PIC X(20).
           05  PRV-CITY                     PIC X(20).
           05  PRV-STATE                    PIC X(2).
           05  PRV-ZIP                      PIC 9(9).
           05  PRV-COUNTY-CODE              PIC X(3).
           05  PRV-PHONE                    PIC 9(10).
           05  PRV-FAX                      PIC 9(10).
           05  PRV-EMAIL                    PIC X(40).
           05  PRV-BILLING-NPI              PIC 9(10).
           05  PRV-GROUP-AFFILIATION-ID     PIC X(10).
           05  PRV-ENROLLMENT-DATE          PIC 9(8).
           05  PRV-REVALIDATION-DATE        PIC 9(8).
           05  PRV-TERMINATION-DATE         PIC 9(8).
           05  PRV-STATUS                   PIC X(1).
           05  PRV-MEDICAID-PARTICIPATION-IND PIC X(1).
           05  PRV-MEDICARE-PARTICIPATION-IND PIC X(1).
           05  PRV-OWNERSHIP-TYPE           PIC X(2).
           05  PRV-ACCREDITATION-CODE       PIC X(4).
           05  PRV-SITE-OF-SERVICE-CODE     PIC X(2).
           05  PRV-PANEL-CAPACITY           PIC 9(4).
           05  PRV-LANGUAGE-SPOKEN          PIC X(3).
           05  PRV-LAST-UPDATE-DATE         PIC 9(8).
           05  PRV-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(16).
