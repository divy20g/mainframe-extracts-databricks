      ******************************************************************
      * MEDICAL-CLAIM-RECORD
      * MEDICAID MEDICAL (INSTITUTIONAL/PROFESSIONAL) CLAIMS EXTRACT
      * SOURCE FILE: MEDICAL_CLAIMS.txt   RECORD LENGTH: 320
      ******************************************************************
       01  MEDICAL-CLAIM-RECORD.
           05  CLM-CLAIM-ID                 PIC X(13).
           05  CLM-ICN                      PIC X(15).
           05  CLM-MEMBER-ID                PIC X(10).
           05  CLM-MEDICAID-ID              PIC X(12).
           05  CLM-BILLING-PROVIDER-ID      PIC X(10).
           05  CLM-RENDERING-PROVIDER-ID    PIC X(10).
           05  CLM-REFERRING-PROVIDER-ID    PIC X(10).
           05  CLM-CLAIM-TYPE               PIC X(2).
           05  CLM-CLAIM-FREQUENCY-CODE     PIC X(1).
           05  CLM-PLACE-OF-SERVICE         PIC X(2).
           05  CLM-TYPE-OF-BILL             PIC X(3).
           05  CLM-FROM-DOS                 PIC 9(8).
           05  CLM-TO-DOS                   PIC 9(8).
           05  CLM-ADMISSION-DATE           PIC 9(8).
           05  CLM-DISCHARGE-DATE           PIC 9(8).
           05  CLM-ADMISSION-TYPE           PIC X(1).
           05  CLM-ADMISSION-SOURCE         PIC X(1).
           05  CLM-DISCHARGE-STATUS         PIC X(2).
           05  CLM-PRINCIPAL-DIAGNOSIS-CODE PIC X(7).
           05  CLM-DIAGNOSIS-CODE-2         PIC X(7).
           05  CLM-DIAGNOSIS-CODE-3         PIC X(7).
           05  CLM-DIAGNOSIS-CODE-4         PIC X(7).
           05  CLM-PRINCIPAL-PROCEDURE-CODE PIC X(5).
           05  CLM-PROCEDURE-CODE-2         PIC X(5).
           05  CLM-MODIFIER-1               PIC X(2).
           05  CLM-MODIFIER-2               PIC X(2).
           05  CLM-REVENUE-CODE             PIC X(4).
           05  CLM-DRG-CODE                 PIC X(3).
           05  CLM-UNITS                    PIC 9(5).
           05  CLM-BILLED-AMOUNT            PIC 9(9)V9(2).
           05  CLM-ALLOWED-AMOUNT           PIC 9(9)V9(2).
           05  CLM-PAID-AMOUNT              PIC 9(9)V9(2).
           05  CLM-PATIENT-RESPONSIBILITY-AMOUNT PIC 9(7)V9(2).
           05  CLM-TPL-AMOUNT               PIC 9(7)V9(2).
           05  CLM-CLAIM-STATUS             PIC X(1).
           05  CLM-CLAIM-STATUS-DATE        PIC 9(8).
           05  CLM-ADJUSTMENT-REASON-CODE   PIC X(4).
           05  CLM-EOB-CODE                 PIC X(4).
           05  CLM-RECEIVED-DATE            PIC 9(8).
           05  CLM-PROCESSED-DATE           PIC 9(8).
           05  CLM-PAID-DATE                PIC 9(8).
           05  CLM-CHECK-EFT-NUMBER         PIC X(10).
           05  CLM-COB-INDICATOR            PIC X(1).
           05  CLM-PRIOR-AUTH-NUMBER        PIC X(12).
           05  CLM-LAST-UPDATE-DATE         PIC 9(8).
           05  CLM-SOURCE-SYSTEM-CODE       PIC X(3).
           05  FILLER                       PIC X(16).
