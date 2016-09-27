C 15 MAY 03 - MK  - FUTURE LIBRARY OF MCP'S
C
C*MODULE MCPLIB  *DECK MCPLIB
C
C     MCPLIB RETURNS  VALENCE BASIS-SET INFORMATION
C     OR MODEL-POTENTIALS WITH CORE BASIS-SET INFORMATION
C
      SUBROUTINE MCPLIB(MMPMOD,NUCZ,MMPTYP,SHINFO,CDFCTR,NOSH,KTYP,KNG,
     2                  EX,C,ZCORE,NOAN0,NOAN1,AN0,ALPN0,AN1,
     3                  ALPN1,BPAR,ITYP,IERR)
C
C     --- MMPMOD: 0  READ VALENCE BASIS-SET
C     ---         1  READ MODEL-POTENTIAL-PARAMETERS
C     ---            AND CORE-SHELL BASIS-SET
C
C     --- NUCZ:    NUCLEAR CHARGE
C     --- MMPTYP:  1  NON-RELATIVISTIC   MOD.POT.
C     ---          2  QUASI-RELATIVISTIC MOD.POT.
C     ---          3  READ IN MOD.POT.FROM $MCP GROUP
C     ---          4  TYPE NOT SPECIFIED
C     ---    W*10**I  FOR I-TH SHELL (I>=1)
C     ---    W: 1,2,3,4,6  S,P,D,F,L - SHELL
C     --- CDFCTR(I) CODED DEFAULT CONTRACTION OF VALENCE-SHELL I
C     --- NOSH     NO.OF (VALENCE OR CORE) SHELLS
C     --- KTYP(I)  TYPE OF SHELL I
C     --- KNG(I)   NO.OF GTFS IN SHELL I
C     --- EX(J)    EXPONENT OF J-TH GTF
C     --- C(J)     CONTRACTION COEFF.OF J-TH GTF
C     --- ZCORE    CORE-CHARGE
C     --- NOAN0    NO.OF A-TERMS FOR N=0
C     --- NOAN1    NO.OF A-TERMS FOR N=1
C     --- AN0(I)   A-PARAMETERS FOR N=0
C     --- ALPN0(I) ALPHA-EXPONENTS FOR N=0
C     --- AN1(I)   A-PARAMETERS FOR N=1
C     --- ALPN1(I) ALPHA-EXPONENTS FOR N=1
C     --- BPAR(I)  B-PARAMETERS
C     --- IERR(I)  ERROR-STATUS   FOR MMPMOD=0:
C     ---          0  OK; 1  NOT MMP-ATOM; 2 MMPTYP WRONG
C
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      DIMENSION AN0(*),ALPN0(*),AN1(*),ALPN1(*)
      DIMENSION BPAR(*),KNG(*),KTYP(*)
      DIMENSION C(*),EX(*)
      CHARACTER*20 CDFCTR(*),SHINFO
C
      DIMENSION ITYP(10)
      COMMON /IOFILE/ IR,IW,IP,IJK,IPK,IDAF,NAV,IODA(400)
C
      IERR=0
C
      DUMMY = MMPMOD+MMPTYP+NUCZ
      CDFCTR(1) = '                    '
      SHINFO = '                    '
      NOAN0 = 1
      NOAN1 = 1
      AN0(1) = DUMMY
      ALPN0(1) = DUMMY
      AN1(1) = DUMMY
      ALPN1(1) = DUMMY
      BPAR(1) = DUMMY
      C(1) = DUMMY
      EX(1) = DUMMY
      KNG(1) = 1
      KTYP(1) = 1
      ZCORE = DUMMY
      NOSH = 1
      ITYP(1)=1
       
C
      WRITE(IW,FMT='('' MCPLIB - IN PROGRESS '')')
      CALL ABRT
      RETURN
      END