program	apply_index


INTEGER, PARAMETER	:: rx=360, ry=180
INTEGER, PARAMETER	:: nx=361, ny=361

INTEGER				:: i, j

INTEGER(KIND=2),DIMENSION(nx,ny)	:: ind_x, ind_y	

REAL*4,DIMENSION(nx,ny)	:: cov

REAL(KIND=4),DIMENSION(rx, ry) :: raw


CHARACTER*100		:: ipath, ipath2, opath
CHARACTER*50		:: fn

LOGICAL(4) status 


open(11, file='geo_to_laea_indy.bin', access='direct', STATUS = 'OLD', recl=nx*ny*2)
read(11, rec=1) ind_y
close(11)

open(12, file='geo_to_laea_indx.bin', access='direct', STATUS = 'OLD', recl=nx*ny*2) 
read(12, rec=1) ind_x
close(12)

ind_y = abs(ind_y)

open(99, file='D:\KOPRI_energy\DATA\2.Output\1.Rn_daily\1.raw\CERES_SYN\CERES_SYN_Rn_20070101.bin', access='direct', STATUS = 'OLD', recl=rx*ry*4) 
read(99,rec=1) raw
CLOSE(99)
	
	do i = 1,nx
	do j = 1,ny
		cov(i,j)= raw(ind_x(i,j),ind_y(i,j))
	enddo
	enddo

open(31, file='re_project.bin', access="direct" , recl=nx*ny*4) !, STATUS = 'NEW')
write(31, rec=1) cov
close(31)


end program 