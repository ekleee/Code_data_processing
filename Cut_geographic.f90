SUBROUTINE Cut_geographic(start_lat,start_lon,ul_lat,ul_lon,lr_lat,lr_lon,pixel_size,ulx,uly,lrx,lry)

REAL,INTENT(IN)                    :: start_lat, start_lon
REAL,INTENT(IN)                    :: ul_lat, ul_lon
REAL,INTENT(IN)                    :: lr_lat, lr_lon
REAL,INTENT(IN)                    :: pixel_size
INTEGER,INTENT(OUT)                :: ulx,uly,lrx,lry

uly = NINT( (start_lat-ul_lat)/pixel_size ) + 1
ulx = NINT( (ul_lon-start_lon)/pixel_size ) + 1 

lry = NINT( (start_lat-lr_lat)/pixel_size ) + 1
lrx = NINT( (lr_lon-start_lon)/pixel_size ) + 1 

return

end

