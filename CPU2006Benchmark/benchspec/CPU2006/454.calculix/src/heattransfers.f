!
!     CalculiX - A 3-dimensional finite element program
!              Copyright (C) 1998 Guido Dhondt
!
!     This program is free software; you can redistribute it and/or
!     modify it under the terms of the GNU General Public License as
!     published by the Free Software Foundation(version 2);
!     
!
!     This program is distributed in the hope that it will be useful,
!     but WITHOUT ANY WARRANTY; without even the implied warranty of 
!     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
!     GNU General Public License for more details.
!
!     You should have received a copy of the GNU General Public License
!     along with this program; if not, write to the Free Software
!     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
!
      subroutine heattransfers(text,textpart,nmethod,iperturb,isolver,
     &  istep,istat,in,n,tinc,tper,tmin,tmax,idrct,ithermal)
!
!     reading the input deck: *HEAT TRANSFER
!
!     isolver=0: SPOOLES
!             1: profile solver
!             2: iterative solver with diagonal scaling
!             3: iterative solver with Cholesky preconditioning
!
      implicit none
!
      character*33 solver
      character*40 textpart(16)
      character*132 text
!
      integer nmethod,iperturb,isolver,istep,istat,in,n,key,i,idrct,
     &  ithermal
!
      real*8 tinc,tper,tmin,tmax
!
      idrct=0
      tmin=0.d0
      tmax=0.d0
      nmethod=4
!
      if(iperturb.eq.0) then
         iperturb=2
      elseif(iperturb.eq.1) then
         write(*,*) '*ERROR in heattransfers: perturbation analysis is'
         write(*,*) '       not provided in a *HEAT TRANSFER step.'
         stop
      endif
!
      if(istep.lt.1) then
         write(*,*) '*ERROR in heattransfers: *HEAT TRANSFER can only'
         write(*,*) '       be used within a STEP'
         stop
      endif
!
      if(ithermal.eq.0) then
         write(*,*) '*ERROR in heattransfers: please define initial '
         write(*,*) '       conditions for the temperature'
         stop
      else
         ithermal=2
      endif
!
!     default solver
!
      solver(1:7)='spooles'
      isolver=0
!
      do i=2,n
         if(textpart(i)(1:7).eq.'SOLVER=') then
            read(textpart(i)(8:40),'(a33)') solver
         elseif(textpart(i)(1:6).eq.'DIRECT') then
            idrct=1
         elseif(textpart(i)(1:11).eq.'STEADYSTATE') then
            nmethod=1
         endif
      enddo
!
      if(solver(1:7).eq.'PROFILE') then
         isolver=1
      elseif(solver(1:16).eq.'ITERATIVESCALING') then
         isolver=2
      elseif(solver(1:17).eq.'ITERATIVECHOLESKY') then
         isolver=3
      endif
!
      nmethod=1
!
      call getnewline(text,textpart,istat,in,n,key)
      if((istat.lt.0).or.(key.eq.1)) then
         if(iperturb.ge.2) then
            write(*,*) '*WARNING in heattransfers: a nonlinear geometric
     & analysis is requested'
            write(*,*) '         but no time increment nor step is speci
     &fied'
            write(*,*) '         the defaults (1,1) are used'
            tinc=1.d0
            tper=1.d0
            tmin=1.d-5
            tmax=1.d+30
         endif
         return
      endif
!
      read(textpart(1),'(f40.0)',iostat=istat) tinc
      if(istat.gt.0) call inputerror(text)
      read(textpart(2),'(f40.0)',iostat=istat) tper
      if(istat.gt.0) call inputerror(text)
      read(textpart(3),'(f40.0)',iostat=istat) tmin
      if(istat.gt.0) call inputerror(text)
      read(textpart(4),'(f40.0)',iostat=istat) tmax
      if(istat.gt.0) call inputerror(text)
!
      if(tinc.le.0.d0) then
         write(*,*) '*ERROR in heattransfers: initial increment size is 
     &negative'
      endif
      if(tper.le.0.d0) then
         write(*,*) '*ERROR in heattransfers: step size is negative'
      endif
      if(tinc.gt.tper) then
         write(*,*) '*ERROR in heattransfers: initial increment size exc
     &eeds step size'
      endif
!      
      if(idrct.ne.1) then
         if(dabs(tmin).lt.1.d-10) then
            tmin=min(tinc,1.d-5*tper)
         endif
         if(dabs(tmax).lt.1.d-10) then
            tmax=1.d+30
         endif
      endif
!
      call getnewline(text,textpart,istat,in,n,key)
!
      return
      end








