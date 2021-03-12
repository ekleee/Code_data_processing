PROGRAM geo_to_laea

IMPLICIT NONE

INTEGER				:: i, j

INTEGER, PARAMETER			:: nx= 361, ny= 361
REAL(KIND=4), PARAMETER		:: pixel_size =	 0.25
REAL(KIND=4), PARAMETER		:: start_lat = -89.875	  ! UPPER
REAL(KIND=4), PARAMETER		:: start_lon = -179.875	  !	left

REAL(KIND=4),DIMENSION(nx,ny)		:: ul_lon, ul_lat
INTEGER(KIND=2),DIMENSION(nx,ny)	:: ind_y, ind_x


OPEN (11, FILE='./latlon/app_x_longitude.bin', ACCESS = 'DIRECT', RECL = nx*ny*4, STATUS = 'OLD')
OPEN (12, FILE='./latlon/app_x_latitude.bin', ACCESS = 'DIRECT', RECL = nx*ny*4, STATUS = 'OLD')

READ(11, REC = 1) ul_lon
READ(12, REC = 1) ul_lat


CLOSE(11)	;	CLOSE(12)

!WHERE(ul_lon .lt. 0) ul_lon=ul_lon+360

DO i = 1, nx
DO j = 1, ny
	ind_y(i,j) = NINT( (start_lat - ul_lat(i,j)) /pixel_size) + 1
	ind_x(i,j) = NINT( (ul_lon(i,j) - start_lon) /pixel_size) + 1 

	IF (mod(i, 10) == 0 )print*, i, j 
ENDDO
ENDDO


OPEN(98, FILE='./latlon/saf_to_laea_indy.bin', ACCESS = 'DIRECT', RECL = nx*ny*2) !, STATUS = 'NEW')
OPEN(99, FILE='./latlon/saf_to_laea_indx.bin', ACCESS = 'DIRECT', RECL = nx*ny*2) !, STATUS = 'NEW')

WRITE(98, REC = 1 ) ind_y
WRITE(99, REC = 1 ) ind_x

CLOSE(98)	;	CLOSE(99)

END

 
