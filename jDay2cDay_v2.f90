subroutine jDay2cDay(year, jday, month, day, smonth, sday)
implicit none

integer*2, intent(in)			:: year, jday
integer*2, intent(out)			:: month, day
integer*2, dimension(13)		:: nday
integer							:: k
character*2, intent(out)		:: smonth, sday

nday =(/0,31,28,31,30,31,30,31,31,30,31,30,31/) 

if(mod(year,   4) .eq. 0) nday(3) = 29
if(mod(year, 100) .eq. 0) nday(3) = 28
if(mod(year, 400) .eq. 0) nday(3) = 29

do k = 1, 13
	if( jday .gt. sum(nday(1:k)) .and. jday .le. sum(nday(1:k+1)) ) then 
		month = k
		day = jday-sum(nday(1:k))
		exit
	endif
enddo

write(smonth, '(i2.2)') month
write(sday, '(i2.2)') day

return
end
