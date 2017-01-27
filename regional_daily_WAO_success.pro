;**********************
;Regional Analysis code
;Written by Zoe Fleming and Roland Leigh (and helped by Stephen Edmundson's daily code used for CV)
;regional_analysis_wao_v2_final_testing worked for 3 hourly files on 28th September 2015
;11th November 2015 - not working yet- all zero but get output file
;**********************


;**********************
;PATHS TO CHANGE HERE
;**********************

;line 675 to change year

;Switches off plotting of maps if want to just do regional analysis'
plotout = 0
input_file_directory = '/data/name/NAME_data/marios/WAOTEST/WAO/'
;Change from high or low here
;highorlow = 'HIGH'
highorlow = 'low'

;**********************
searchstring = '*.txt'
;searchstring = '*' + highorlow + 'low*.txt'
files = file_search(input_file_directory, searchstring)
help, files

print, 'Number of files being analysed by region = ', n_elements(files)

;HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
for thisfile = 0, n_elements(files)-1 do begin

	fn = files(thisfile)

	;Output filename for .png file from this data file
	bits2 = strsplit(fn, '/', /extract)
	bits = strsplit(fn, '.', /extract)
	opfn = bits(0) + '_WAO2012.png' ;;; ????????????

	;lowCAPEVERDE_20150422
	;Weybourne_10dayback_201401010000_0-100m
	fnstring = bits2(n_elements(bits2)-1)
	bits3 = strsplit(fnstring, '_', /extract)
	fndate = bits3(n_elements(bits3)-1) ; was -2 from date_0-100m
	fnyear = strmid(fndate,0,4)
	fnmonth = strmid(fndate,4,2)
	fnday = strmid(fndate,6,2)
	fnhour = strmid(fndate, 8, 2)
	;added by zoe to get : in between hour and minute to output into IGOR
	fnminute = strmid(fndate, 10, 2)


	s = ''
	;initial run-through of file to get information on size etc.
	openr,1,fn
	;Getting header information
	readf,1,s
	modelversion = s
	readf,1,s
	bits = strsplit(s, ':', /extract)
	runname = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	runtime = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	metdata = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	startofrelease = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	endofrelease = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	SourceStrength = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	releaselocation = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	releaseheight = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	runduration = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	xgridorigin = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	ygridorigin = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	xgridsize = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	ygridsize = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	xgridresolution = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	ygridresolution = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	numberofprelimcols = bits(1)
	readf,1,s
	bits = strsplit(s, ':', /extract)
	numberoffieldcols = bits(1)


		for a= 0, 18 do begin

	readf,1,s

		endfor
	count = 0

	;speeding this process up - RJL - 21st July 2009

	linecount = 0l
	;Switch between these lines for testing
	while not eof(1) do begin
	;for x = 0, 3000 do begin
	readf,1,s
	linecount = linecount +1
	endwhile

	;pre-defining sizes of arrays
	lats = fltarr(linecount)
	lons = fltarr(linecount)
	cool=fltarr(linecount)
	concs = dblarr(8,linecount)  ; 8 of these!
	concs1=fltarr(linecount)

	close, 1
	;reopening
	openr,1,fn

		for a= 0, 36 do begin

	readf,1,s
		endfor


	;Roland added 8 October for corrupted files

		for count = 0l, linecount-1 do begin
			readf,1,s
			bits = strsplit(s, ',', /extract)
			ninfo = n_elements(bits)    ; if have extra coloumn for high
			if ninfo ne 12 then break ; now 4 initial columns and 8 time ones
		
			lats(count) = bits(3)
			lons(count) = bits(2)
			;concs(count)= double(bits(4))
			;cool[count]= double(bits(4))
			;total1=total(concs1)
			concs[0,count]= double(bits(4))
			concs[1,count]= double(bits(5))
			concs[2,count]= double(bits(6))
			concs[3,count]= double(bits(7))
			concs[4,count]= double(bits(8))
			concs[5,count]= double(bits(9))
			concs[6,count]= double(bits(10))
			concs[7,count]= double(bits(11))
		
		endfor
	print,'read finished for file number ',  thisfile

		;file has now been read in, defining graphics options.
	close, 1

					Columns=["Col1","Col2","Col3","Col4","Col5","Col6","Col7","Col8"]
					Columns_Time=[" 00:00"," 03:00"," 06:00"," 09:00"," 12:00"," 15:00"," 18:00"," 21:00"]

		n_Columns=n_elements(Columns)

	;*****************************************************************************************************************************************************************************************************************************************
			for z=0,n_Columns-1 do begin 
				total_of_each_column="total_of_"+Columns[z]
				;print,total_of_each_column,total(concs[z,*])   ; needs to be outside of the close so doesnt just sum line 0 and line 1 and line 2 etc..   (try turnig this off after you are sure it works)
				pconcs = concs[z,*]/(total(concs[z,*])) * 100.0 
				;print, concs[z,*]
				;print, concs  [z,0:3]   ; test first 4 values of each conc coloumn
				concentration = (pconcs/100)*(total(concs[z,*]))


;concs = concs/total(concs) * 100.0 



				;print,Columns_Time[z] ; (turn this off when you know it works)
				;print,pconcs [0:3] ; print first 4 lines of pconcs
		                ;print,pconcs [3] 
				;concs = pconcs ;THIS IS THE BIT THAT MAKES IT SAY ITS OUT OF RANGE CAUSE IT WILL DO ONE LOOOP THEN CHAGE ALL THE VARIABLES

					if plotout eq 1 then begin
						device, retain = 2, decomposed = 0
						window, 1, xsize = 1000, ysize = 800
						polyfill, [0,1,1,0],[0,0,1,1], color = 255,/normal
						;Set the domain here to suit CV or WAO
						loadct, 0
						MAP_SET, /mercator,   LIMIT=[0,250, 90,90], /CONTINENTS, TITLE=runname, /hires,E_CONTINENTS={FILL:1, color:200}, E_HORIZON={FILL:1, COLOR:80}
						; roland added to make logarithmic
						maxc = double(max(pconcs))
						minc = double(min(pconcs))
						usersym, [1.2,1.2,-1.2,-1.2], [-1.2,1.2,1.2,-1.2], /fill
						loadct, 39

						 for ab = 0l, n_elements(lats)-2 do begin
							col = fix((float((pconcs(ab))-minc)/(maxc-minc))*254)

							if col gt 255 then col = 255

							xs = [lons(ab)-(xgridresolution/2.0),lons(ab)+(xgridresolution/2.0),lons(ab)+(xgridresolution/2.0),lons(ab)-(xgridresolution/2.0)]
							ys = [lats(ab)-(ygridresolution/2.0), lats(ab)-(ygridresolution/2.0),lats(ab)+(ygridresolution/2.0),lats(ab)+(ygridresolution/2.0)]
							if col gt 50 then polyfill, xs, ys, color = col
						endfor

					endif ;plotout

										;Changing from here to have no fixed grid. 

										;User definition
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;defining number of zones - if add zone, then add 1 here
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										ngzones = 10
										ngmaxdefs = 3 ; maximum number of definition per line of latitude   ; change to 4

										;making latitude grid. 
										nglatmin = 0
										nglatmax = 90
										nggridres = 0.25
										ngnumlats = ((nglatmax-nglatmin)/nggridres)
										nglatgrid = (findgen(ngnumlats)-nglatmin)*nggridres

										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;defining zones - if add zone, then add new definition here
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										ngzone1 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone1(*,*) = -999

										ngzone2 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone2(*,*) = -999

										ngzone3 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone3(*,*) = -999

										ngzone4 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone4(*,*) = -999

										ngzone5 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone5(*,*) = -999

										ngzone6 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone6(*,*) = -999

										ngzone7 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone7(*,*) = -999

										ngzone8 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone8(*,*) = -999

										ngzone9 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone9(*,*) = -999

										ngzone10 = fltarr(ngnumlats,ngmaxdefs*2)
										ngzone10(*,*) = -999

										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;Filling in zones
										;Each definition is a pair!
										;first is start lon
										;Second is end lon
										;Each for the appropriate latitude band
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;Arctic zone1
										;Scandinavia zone2
										;Europe zone3
										;Atlantic zone4
										;Greenland and Iceland zone5
										;America zone6
										;UK zone7
										;North Sea zone8
										;WAO_marine ZONE 9
										;WAO_land ZONE 10

										;zone1 definition (Arctic)
										;ngzone(latitudebandstart:latitudebandend,0) = startlatband
										ngzone1(240:248,0) = -5.0 ;start Long
										ngzone1(240:248,1) = 3.4 ;End Long

										ngzone1(248:250,0) = -5.0;start Long
										ngzone1(248:250,1) = 4.8;End

										ngzone1(250:254,0) = -10.0;start Long
										ngzone1(250:254,1) = 6.0;End  Long

										ngzone1(254:256,0) = -11.0;start Long
										ngzone1(254:256,1) = 7.5;End  Lon

										ngzone1(256:258,0) = -12;start Long
										ngzone1(256:258,1) = 8;End  Lon

										ngzone1(258:260,0) = -12;start Long
										ngzone1(258:260,1) = 10;End  Lon

										ngzone1(260:262,0) = -13;start Long
										ngzone1(260:262,1) = 11;End  Lon

										ngzone1(262:264,0) = -13;start Long
										ngzone1(262:264,1) = 12;End  Lon

										ngzone1(264:274,0) = -13.0;start Long
										ngzone1(264:274,1) = 12.5;End  Lon

										ngzone1(274:280,0) = -18;start Long
										ngzone1(274:280,1) = 14;End  Lon

										ngzone1(280:282,0) = -18;start Long
										ngzone1(280:282,1) = 17;End  Lon

										ngzone1(282:286,0) = -18;start Long
										ngzone1(282:286,1) = 22;End 

										;Turn all 60 E into 80

										ngzone1(286:359,0) = -16;start Long
										ngzone1(286:359,1) = 80;End  Lon

										;zone2 definition (Scandinavia)
										ngzone2(220:230,0) = 7.0 ;start Long
										ngzone2(220:230,1) = 20.0 ;End Long

										ngzone2(230:235,0) = 4.0 ;start Long
										ngzone2(230:235,1) = 20.0 ;End Long

										ngzone2(235:240,0) = 4.0 ;start Long
										ngzone2(235:240,1) = 80.0 ;End Long

										ngzone2(240:248,0) = 3.4 ;start Long
										ngzone2(240:248,1) = 80 ;End Long

										ngzone2(248:250,0) = 4.8;start Long
										ngzone2(248:250,1) = 80;End

										ngzone2(250:254,0) = 6.0;start Long
										ngzone2(250:254,1) = 80.0;End  Long

										ngzone2(254:256,0) = 7.5;start Long
										ngzone2(254:256,1) = 80;End  Lon

										ngzone2(256:258,0) = 8;start Long
										ngzone2(256:258,1) = 80;End  Lon

										ngzone2(258:260,0) = 10;start Long
										ngzone2(258:260,1) = 80;End  Lon

										ngzone2(260:262,0) = 11;start Long
										ngzone2(260:262,1) = 80;End  Lon

										ngzone2(262:264,0) = 12;start Long-62.0
										ngzone2(262:264,1) = 80;End  Lon

										ngzone2(264:274,0) = 12.5;start Long
										ngzone2(264:274,1) = 80;End  Lon

										ngzone2(274:280,0) = 14;start Long
										ngzone2(274:280,1) = 80;End  Lon

										ngzone2(280:282,0) = 17;start Long
										ngzone2(280:282,1) = 80;End  Lon

										ngzone2(282:286,0) = 22;start Long
										ngzone2(282:286,1) = 80;End 

										;zone3 definition (Europe_Africa)
										ngzone3(60:130,0) = -18.0 ;start Long
										ngzone3(60:130,1) = 80.0 ;End Long

										ngzone3(130:180,0) = -10.0 ;start Long
										ngzone3(130:180,1) = 80.0 ;End Long

										ngzone3(180:196,0) = -5.0 ;start Long
										ngzone3(180:196,1) = 80.0 ;End Long

										ngzone3(196:202,0) = 1.0 ;start Long
										ngzone3(196:202,1) = 80.0 ;End Long

										ngzone3(202:206,0) = 2.0 ;start Long
										ngzone3(202:206,1) = 80.0 ;End Long

										ngzone3(206:212,0) = 4.0 ;start Long
										ngzone3(206:212,1) = 80.0 ;End Long

										ngzone3(212:217,0) = 5.0 ;start Long
										ngzone3(212:217,1) = 80.0 ;End Long

										ngzone3(217:220,0) = 7.0 ;start Long
										ngzone3(217:220,1) = 80.0 ;End Long

										ngzone3(220:235,0) = 20.0 ;start Long
										ngzone3(220:235,1) = 80.0 ;End Long

										;zone4 definition (Atlantic)
										;extend from 220 to 20degrees = 80: 12 April 2010 extension

										ngzone4(60:130,0) = -75.0 ;start Long
										ngzone4(60:130,1) = -18.0 ;End Long

										ngzone4(130:160,0) = -74.0 ;start Long
										ngzone4(130:160,1) = -10.0 ;End Long

										ngzone4(160:172,0) = -69.0 ;start Long
										ngzone4(160:172,1) = -10.0 ;End Long

										ngzone4(172:183,0) = -60.0 ;start Long
										ngzone4(172:183,1) = -10.0 ;End Long

										ngzone4(183:198,0) = -52.0 ;start Long
										ngzone4(183:198,1) = -5.0 ;End Long

										ngzone4(198:203,0) = -53.0 ;start Long
										ngzone4(198:203,1) = -7.0 ;End Long

										ngzone4(203:220,0) = -54 ;start Long
										ngzone4(203:220,1) = -11.0 ;End Long


										;zone5 definition (Greenland and Iceland)
										ngzone5(220:224,0) = -58.0 ;start Long
										ngzone5(220:224,1) = -8.0 ;End Long

										ngzone5(224:235,0) = -61.0 ;start Long
										ngzone5(224:235,1) = -7 ;End Long

										ngzone5(235:250,0) = -63.0 ;start Long
										ngzone5(235:250,1) = -5.0 ;End Long

										ngzone5(250:254,0) = -62.0;start Long
										ngzone5(250:254,1) = -10;End  Long

										ngzone5(254:256,0) = -62.0;start Long
										ngzone5(254:256,1) = -11;End  Lon

										ngzone5(256:264,0) = -62.0;start Long
										ngzone5(256:264,1) = -12;End  Lon

										ngzone5(264:274,0) = -61.0;start Long
										ngzone5(264:274,1) = -13;End  Lon

										ngzone5(274:286,0) = -65.0;start Long
										ngzone5(274:286,1) = -18;End  Lon

										ngzone5(286:290,0) = -71;start Long
										ngzone5(286:290,1) = -16;End  

										ngzone5(290:359,0) = -75;start Long
										ngzone5(290:359,1) = -16;End 

										;zone6 definition (America)
										;extend from 220 to 20degrees = 80: 12 April 2010 extension

										ngzone6(60:130,0) = -110.0 ;start Long
										ngzone6(60:130,1) = -75.0 ;End Long

										ngzone6(130:160,0) = -110.0 ;start Long
										ngzone6(130:160,1) = -74.0 ;End Long

										ngzone6(160:172,0) = -110.0 ;start Long
										ngzone6(160:172,1) = -69.0 ;End Long

										ngzone6(172:183,0) = -110.0 ;start Long
										ngzone6(172:183,1) = -60.0 ;End Long

										ngzone6(183:198,0) = -110.0 ;start Long
										ngzone6(183:198,1) = -52.0 ;End Long

										ngzone6(198:203,0) = -110.0 ;start Long
										ngzone6(198:203,1) = -53.0 ;End Long

										ngzone6(203:220,0) = -110 ;start Long
										ngzone6(203:220,1) = -54.0 ;End Long

										;ngzone6(80:220,0) = -110.0 ;start Long
										;ngzone6(80:220,1) = -58.0 ;End Long

										ngzone6(220:224,0) = -110.0 ;start Long
										ngzone6(220:224,1) = -58.0 ;End Long

										ngzone6(224:235,0) = -110.0 ;start Long
										ngzone6(224:235,1) = -61 ;End Long

										ngzone6(235:250,0) = -110.0 ;start Long
										ngzone6(235:250,1) = -63.0 ;End Long

										ngzone6(250:264,0) = -110.0;start Long
										ngzone6(250:264,1) = -62;End  Long

										ngzone6(264:274,0) = -110.0;start Long
										ngzone6(264:274,1) = -61;End  Lon

										ngzone6(274:286,0) = -110.0;start Long
										ngzone6(274:286,1) = -65;End  Lon

										ngzone6(286:290,0) = -110;start Long
										ngzone6(286:290,1) = -71;End  

										ngzone6(290:359,0) = -110;start Long
										ngzone6(290:359,1) = -75;End


										;zone7 definition (UK)
										ngzone7(196:198,0) = -5.0 ;start Long
										ngzone7(196:198,1) = 1.0 ;End 

										ngzone7(198:202,0) = -7.0 ;start Long
										ngzone7(198:202,1) = 1.0 ;End Long

										ngzone7(202:203,0) = -7.0 ;start Long
										ngzone7(202:203,1) = 2.0 ;End Long

										ngzone7(203:209.5,0) = -11.0 ;start Long  ; change
										ngzone7(203:209.5,1) = 2.0 ;End Long

										ngzone7(209.5:213.5,0) = -11 ;start Long  ; change
										ngzone7(209.5:213.5,1) = 0.5 ;End Long

										ngzone7(213.5:217,0) = -11 ;start Long  ; change
										ngzone7(213.5:217,1) = 0.25 ;End Long

										ngzone7(217:220,0) = -11 ;start Long
										ngzone7(217:220,1) = 0.0 ;End Long

										ngzone7(220:224,0) = -8.0 ;start Long
										ngzone7(220:224,1) = -1.0 ;End Long

										ngzone7(224:235,0) = -7.0 ;start Long
										ngzone7(224:235,1) = -2 ;End Long

										;zone8 definition (North Sea)
										ngzone8(205:206,0) = 2.0 ;start Long
										ngzone8(205:206,1) = 3.0 ;End Long

										;;ngzone8(202:212,0) = 4.0 ;start Long
										;;ngzone8(206:212,1) = 5.0 ;End Long

										ngzone8(206:212,0) = 2.0 ;start Long
										ngzone8(206:212,1) = 4.0 ;End Long Long

										ngzone8(212:213.5,0) = 2.0 ;start Long       
										ngzone8(212:213.5,1) = 5.0 ;End Long Long

										ngzone8(213.5:217,0) = 0.25 ;start Long     ; change
										ngzone8(213.5:217,1) = 5.0 ;End Long Long

										ngzone8(217:220,0) = 0.0 ;start Long
										ngzone8(217:220,1) = 7.0 ;End Long Long

										ngzone8(220:224,0) = -1.0 ;start Long
										ngzone8(220:224,1) = 8.0 ;End Long Long

										ngzone8(224:230,0) = -2.0 ;start Long
										ngzone8(224:230,1) = 7.0 ;End Long 

										ngzone8(230:235,0) = -2.0 ;start Long
										ngzone8(230:235,1) = 4.0 ;End Long

										ngzone8(235:240,0) = -5.0 ;start Long
										ngzone8(235:240,1) = 4.0 ;End Lon

										;zone9 definition (WAO_marine)
										ngzone9(211.5:213.5,0) = 0.5; start Long  ; change
										ngzone9(211.5:213.5,1) = 2.0 ;End Long

										;zone10 definition (WAO_land)

										ngzone10(209.5:211.5,0) = 0.5; start Long ;
										ngzone10(209.5:211.5,1) = 2.0 ;End Long

										;plotting out zones

										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;Plotting zones
										;Add zone plotting routine if adding new zones
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										for a = 0, ngnumlats-2 do begin
											;Plotting zone1
											if ngzone1(a,0) ne -999 and ngzone1(a+1,0) ne -999 then begin
											xs = [ngzone1(a,0),ngzone1(a,1), ngzone1(a+1, 1), ngzone1(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 60 
											endif

											;Plotting zone2
											if ngzone2(a,0) ne -999 and ngzone2(a+1,0) ne -999 then begin
											xs = [ngzone2(a,0),ngzone2(a,1), ngzone2(a+1, 1), ngzone2(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 120 
											endif

											;Plotting zone3
											if ngzone3(a,0) ne -999 and ngzone3(a+1,0) ne -999 then begin
											xs = [ngzone3(a,0),ngzone3(a,1), ngzone3(a+1, 1), ngzone3(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 30 
											endif

											;Plotting zone4
											if ngzone4(a,0) ne -999 and ngzone4(a+1,0) ne -999 then begin
											xs = [ngzone4(a,0),ngzone4(a,1), ngzone4(a+1, 1), ngzone4(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 200 
											endif

											;Plotting zone5
											if ngzone5(a,0) ne -999 and ngzone5(a+1,0) ne -999 then begin
											xs = [ngzone5(a,0),ngzone5(a,1), ngzone5(a+1, 1), ngzone5(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 170 
											endif

											;Plotting zone6
											if ngzone6(a,0) ne -999 and ngzone6(a+1,0) ne -999 then begin
											xs = [ngzone6(a,0),ngzone6(a,1), ngzone6(a+1, 1), ngzone6(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 140 
											endif

											;Plotting zone7
											if ngzone7(a,0) ne -999 and ngzone7(a+1,0) ne -999 then begin
											xs = [ngzone7(a,0),ngzone7(a,1), ngzone7(a+1, 1), ngzone7(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 90 
											endif

											;Plotting zone8
											if ngzone8(a,0) ne -999 and ngzone8(a+1,0) ne -999 then begin
											xs = [ngzone8(a,0),ngzone8(a,1), ngzone8(a+1, 1), ngzone8(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 110 
											endif

											;Plotting zone9
											if ngzone9(a,0) ne -999 and ngzone9(a+1,0) ne -999 then begin
											xs = [ngzone9(a,0),ngzone9(a,1), ngzone9(a+1, 1), ngzone9(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 220 
											endif

											;Plotting zone10
											if ngzone10(a,0) ne -999 and ngzone10(a+1,0) ne -999 then begin
											xs = [ngzone10(a,0),ngzone10(a,1), ngzone10(a+1, 1), ngzone10(a+1,0)]
											ys = [nglatgrid(a),nglatgrid(a), nglatgrid(a+1), nglatgrid(a+1)]
											polyfill, xs, ys, color = 10 
											endif

										endfor
										;MAP_GRID, LABEL=1, LATdel = 5, LATS = 0, LATLAB=0, LONLAB=0, LONDEL=5, LONS=0, ORIENTATION= 0, charsize = 2, glinethick = 1


										;matching up lats and lons arrays with our region definitions
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										;Add an extra element if add new region
										regionpercentages = fltarr(10)
										regionpercentages(*) = 0.0
										;%%%%%%%%%%%%%%%%%%%%%%%%%%
										maxlat = max(lats)
										minlat = min(lats)
										for a = 0, ngnumlats -2 do begin
											if nglatgrid(a) le maxlat and nglatgrid(a) ge minlat then begin

												;for % use pconcs and for concentration use second choice
												thisregion = 1
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone1(a,0) and lons lt ngzone1(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 2
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone2(a,0) and lons lt ngzone2(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 3
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone3(a,0) and lons lt ngzone3(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 4
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone4(a,0) and lons lt ngzone4(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 5
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone5(a,0) and lons lt ngzone5(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 6
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone6(a,0) and lons lt ngzone6(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 7
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone7(a,0) and lons lt ngzone7(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 8
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone8(a,0) and lons lt ngzone8(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 9
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone9(a,0) and lons lt ngzone9(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))

												thisregion = 10
												isinbox = where(lats gt nglatgrid(a) and lats le nglatgrid(a+1) and lons gt ngzone10(a,0) and lons lt ngzone10(a,1), np)
												if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(pconcs(isinbox))
												;if np gt 0 then regionpercentages(thisregion-1) = regionpercentages(thisregion-1) + total(concs(isinbox))
											;**********************************************************************************************************************************************************
	;print, regionpercentages(this										
	;print, total(pconcs(isinbox))

											endif

										endfor


					opcsvfn = '/data/name/NAME_data/marios/WAOTEST/WAOPLEASE.csv

					if thisfile eq 0 and z eq 0 then begin
						openw,17, opcsvfn

						opstr='Filename,dateandtime,Arctic,Scandinavia,Europe_Africa,Atlantic,Greenland and Iceland,America,UK,North Sea,WAO_marine,WAO_land'
						printf,17, opstr
						
					
						opstr = fnstring + ',' + fnday + '/' + fnmonth + '/' + fnyear+Columns_Time[z]
					;******************************************
							for b = 0, 9 do begin
								opstr = opstr + ',' + strtrim(regionpercentages(b),2)
							endfor
					;******************************************
						printf,17, opstr

						close, 17

	;print, regionpercentages(b)
	;print, opstr
					endif else begin 
						openw,17, opcsvfn, /append

					opstr = fnstring + ',' + fnday + '/' + fnmonth + '/' + fnyear+Columns_Time[z]
					;******************************************
					 		for b = 0, 9 do begin
								opstr = opstr + ',' + strtrim(regionpercentages(b),2)
							endfor
					;******************************************
						printf,17, opstr

						close, 17

					endelse


			endfor ;z= 0,7 (each column)
	                                    ;OPLOT, [-17.332667], [14.748886], PSYM=7, 	COLOR=10, SYMSIZE=4, THICK=4  
	;*****************************************************************************************************************************************************************************************************************************************

endfor ;this file (all files)
;HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
	
end
