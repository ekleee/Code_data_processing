subroutine LeapYear_check(year, flag)
implicit none

integer*2, intent(in)				:: year
integer*1, intent(out)				:: flag  !! flag = 0 (regular year), flag = 1 (leap year)

flag = 0
if( mod(year,   4) .eq. 0) flag = 1
if( mod(year, 100) .eq. 0) flag = 0
if( mod(year, 400) .eq. 0) flag = 1

return 
end

