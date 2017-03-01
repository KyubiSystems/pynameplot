;**********************
; Regional Analysis code for Cape Verde (Daily files)
;Written Stephen Edmundson and Zoe fleming (based  on old code from by Roland Leigh
;30th October 2009 original with 3 hourly files
;24th September 2015
;Stephen Edmundson called this TEST4.pro on 24 September 2015
;******************************************************************************
;input_file_directory = '/data/name/NAME_data/output_zoe/CAPEVERDE/CV_2014_daily/'
;Switches off plotting of maps if want to just do regional analysis' 1 for plotting
plotout = 0
input_file_directory = '/data/name/NAME_data/output_zoe/CAPEVERDE/CV_2014_daily/new/'
;input_file_directory = '/home/s/sle20/Atmos_chem/CapeVerde'
;Change from high or low here
;highorlow = 'HIGH'
highorlow = 'low'

;**********************
searchstring = '*' + highorlow + '*.txt'   ; normal search but if renamed do below..
;searchstring = '*.txt'
files = file_search(input_file_directory, searchstring)
help, files

for thisfile = 0, n_elements(files)-1 do begin   ; This file
fn = files(thisfile)

bits2 = strsplit(fn, '/', /extract)
bits = strsplit(fn, '.', /extract)

fnstring = bits2(n_elements(bits2)-1)
bits3 = strsplit(fnstring, '_', /extract)
fndate = bits3(n_elements(bits3)-1)           ; -1 for 170000.txt but -2 for 00_0-100m.txt
fnyear = strmid(fndate,0,4)
fnmonth = strmid(fndate,4,2)
fnday = strmid(fndate,6,2)
fnhour = strmid(fndate, 8, 2)
;fnhour = strmid(fndate, 8, 4)
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
			ninfo = n_elements(bits)
			if ninfo ne 12 then break ; now 4 initial columns and 8 time ones

			lats(count) = bits(3)  ; this is just seeing the frst line of the first bit of data before a comma
			lons(count) = bits(2)   ; this is just seeing the second line of the first bit of data before a comma
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
close, 1

				Columns=["Col1","Col2","Col3","Col4","Col5","Col6","Col7","Col8"]
				Columns_Time=[" 00:00"," 03:00"," 06:00"," 09:00"," 12:00"," 15:00"," 18:00"," 21:00"]


	n_Columns=n_elements(Columns)
For z=0,n_Columns-1 do begin 
			total_of_each_column="total_of_"+Columns[z]
			;print,total_of_each_column,total(concs[z,*])   ; needs to be outside of the close so doesnt just sum line 0 and line 1 and line 2 etc..   (try turnig this off after you are sure it works)
			pconcs = concs[z,*]/(total(concs[z,*])) * 100.0  
			concentration = (pconcs/100)*(total(concs[z,*]))

			;print,Columns_Time[z] ; (turn this off when you know it works)
			;print,pconcs
			;concs = pconcs ;THIS IS THE BIT THAT MAKES IT SAY ITS OUT OF RANGE CAUSE IT WILL DO ONE LOOOP THEN CHAGE ALL THE VARIABLES

				if plotout eq 1 then begin
					device, retain = 2, decomposed = 0
					window, 1, xsize = 1000, ysize = 800g
					polyfill, [0,1,1,0],[0,0,1,1], color = 255,/normal
					;Set the domain here to suit CV or WAO
					loadct, 0
					MAP_SET, /mercator,   LIMIT=[-30,210, 80,80], /CONTINENTS, TITLE=runname, /hires,E_CONTINENTS={FILL:1, color:200}, E_HORIZON={FILL:1, COLOR:80}
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


				;********************
				;SETTING UP A GRID
				gridxresolution = 5.0 ;degrees

				gridyresolution = 5.0 ;degrees
				;gridxstart = 260.0
				;gridxend = 55.0
				;gridystart = 0.0
				;gridyend = 80.0
				gridxstart = 210.0
				gridxend = 80.0
				gridystart = -30.0
				gridyend = 80.0
				;crude coding - assuming going over London (0 deg).
				xgrids = (gridxend-gridxstart+360.0)/gridxresolution
				ygrids = (gridyend-gridystart)/gridyresolution

				;Setup grid coordinates
				gridlons =findgen(xgrids)*gridxresolution + gridxstart

				gridlats = findgen(ygrids)*gridyresolution + gridystart
				ov = where(gridlons ge 360.0, ng)
				if ng gt 0 then gridlons(ov) = gridlons(ov)-360.0
				gridlats = reverse(gridlats)
				

				 if plotout eq 1 then begin
					 for a = 0, xgrids -1 do begin
						plots, [gridlons(a), gridlons(a)],[gridlats(0), gridlats(ygrids-1)], color = 250, thick = 2

				     	endfor
				endif ;plotout

				gridindexarray = intarr(xgrids-1, ygrids-1)
				gridregionarray = gridindexarray	
				
				if plotout eq 1 then begin
					  for b = 0, ygrids -1 do begin
						plots, [gridlons(0), gridlons(xgrids-1)],[gridlats(b), gridlats(b)], color = 250, thick = 2
					   endfor
				endif ;plotouts

				for b = 0, ygrids -2 do begin
					for a = 0, xgrids -2 do begin

						if plotout eq 1 then xyouts, gridlons(a)+(gridxresolution/4.0), gridlats(b)-(gridyresolution/3.0), strtrim(round((b*(xgrids-1))+a+1),2), color = 250
						gridindexarray(a,b) = round((b*(xgrids-1))+a+1)
					endfor
				endfor
				

				indexgridlons = gridlons(0:xgrids-2)
				indexgridlats = gridlats(0:ygrids-2)

				leftgridlons = gridindexarray

;defining the left side of each square
				
				for a= 0, 14 do begin
					leftgridlons(*,a) = gridlons(0:n_elements(gridlons)-2)
				endfor

				bottomgridlats = gridindexarray
				


;defining the bottom side of each square

				for a= 0, 29 do begin
					bottomgridlats(a,*) = gridlats(1:n_elements(gridlats)-1)
				endfor
				
				rightgridlons = gridindexarray
				
;defining the right side of each square

				for a= 0, 14 do begin
					rightgridlons(*,a) = gridlons(1:n_elements(gridlons)-1)
				endfor

				topgridlats = gridindexarray

;defining the top side of each square

				for a= 0, 29 do begin
					topgridlats(a,*) = gridlats(0:n_elements(gridlats)-2)
				endfor


;print, gridindexarray



				if plotout eq 1 then MAP_CONTINENTS, /COUNTRIES,  COLOR=255, MLINETHICK=1
				

					;************************
					;************************
					;To add a new region

					; 1. Copy an existing region loop
					; 2. add in region definition (whatever name you want - and an array of box numbers)
					; 3. Change array name to new region after n_elements
					; 4. Change array name to new region in where statement
					; 5. change number to region number.
					;************************
					;************************

					;Region 1 - Coastal African -trajectories that pass within four degrees of longitude of the African coast or the Canary Islands
					;but do not pass over central Africa or Europe .
					;These are basically open ocean but with coastal African input.
					CoastalAfrican = [388,389,432,433,477,522,567,613,659,660,661,662,707]
					;Applying to main grid
					for a = 0, n_elements(CoastalAfrican) -1 do begin
					gridpos = where(gridindexarray eq CoastalAfrican(a),np)
					if np gt 0 then gridregionarray(gridpos) = 1
					endfor
					;************************
					;Region 2 - European - Trajectories that pass over Europe at an elevation of less than 3500 m (Lee et al.)
					;and do not pass over Africa
					Polluted_marine = [78,79,80,81,82,83,84,85,86,87,88,89,90,122,123,124,125,126,127,128,129,130,131,132,133,134,135,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,209,210,211,212,213,214,215,216,217,218,219,220,$
					221,222,223,224,225,255,256,$
					257,258,259,260,261,262,263,264,265,266,267,268,269,270,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360]
					;Applying to main grid
					for a = 0, n_elements(Polluted_marine) -1 do begin
					gridpos = where(gridindexarray eq Polluted_marine(a),np)
					if np gt 0 then gridregionarray(gridpos) = 2
					endfor
					;************************
					;Region 3 - Continental African - pass over central or northern Africa and do not pass over European land mass
					;Dust = [390,391,392,393,394,395,396,397,398,399,400,405,401,402,403,404,405,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,$
					;478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,$
					;;614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,663,664,665,666,667,668,669,670,671,672,673,674,675,708,709,710,711,712,713,714,715,716,717,718,719,720,$
					;753,754,755,756,757,758,759,760,761,762,763,764,765,798,799,800,801,802,803,804,805,806,807,808,809,810,843,844,845,846,847,848,849,850,851,852,853,854,855,888,889,890,891,892,893,894,895,896,897,898,899,900,$
					;933,934,935,936,937,938,939,940,941,942,943,944,945]
					;Applying to main grid
					;for a = 0, n_elements(Dust) -1 do begin
					;gridpos = where(gridindexarray eq Dust(a),np)
					;if np gt 0 then gridregionarray(gridpos) = 3
					;endfor
					;************************
					;Region 3 - Saharan African 
					Sahara = [390,391,392,393,394,395,396,397,398,399,400,405,401,402,403,404,405,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495]
					;Applying to main grid
					for a = 0, n_elements(Sahara) -1 do begin
					gridpos = where(gridindexarray eq Sahara(a),np)
					if np gt 0 then gridregionarray(gridpos) = 3
					endfor
					;************************
					;Region 4 - Sahel African 
					Sahel = [523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,$
					614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630]
					;Applying to main grid
					for a = 0, n_elements(Sahel) -1 do begin
					gridpos = where(gridindexarray eq Sahel(a),np)
					if np gt 0 then gridregionarray(gridpos) = 4
					endfor
					;************************
					;Region5 -NAmerica (formerly Atlantic continental with South America)
					NAmerica = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,$
					136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,$
					271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375]
					;Applying to main grid
					for a = 0, n_elements(NAmerica) -1 do begin
					gridpos = where(gridindexarray eq NAmerica(a),np)
					if np gt 0 then gridregionarray(gridpos) = 5
					endfor
					;************************
					;Region6 -Atlantic marine
					Atlantic_marine = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,64,65,66,67,68,69,70,71,72,73,74,75,76,77,108,109,110,111,112,113,114,115,116,117,118,119,120,121,154,155,156,157,158,159,160,161,162,163,$
					200,201,202,203,204,205,206,207,208,245,246,247,248,249,250,251,252,253,254,289,290,291,292,293,294,295,296,297,298,331,332,333,334,335,336,337,338,339,340,341,342,343,376,377,378,379,380,381,382,383,384,385,386,387,420,421,422,423,424,425,426,427,428,$
					429,430,431,466,467,468,469,470,471,472,473,474,475,476,512,513,514,515,516,517,518,519,559,560,561,562,563,564,605,606,607,608,609,610,611,612,651,652,653,654,655,656,657,658,$
					698,699,700,701,702,703,704,705,706,744,745,746,747,748,749,750,751,752,789,790,791,792,793,794,795,796,797,833,834,835,836,837,838,839,840,841,842,878,879,880,881,882,883,884,885,886,887,922,923,924,925,926,927,928,929,930,931,932]
					;Applying to main grid
					for a = 0, n_elements(Atlantic_marine) -1 do begin
					gridpos = where(gridindexarray eq Atlantic_marine(a),np)
					if np gt 0 then gridregionarray(gridpos) = 6
					endfor
					;************************
					;Could I get rid of these from the total percentage? NE is misleading as so frequent and could be one of many
					;************************
					;Region 7 - NE of site
					site_ne = [521]
					;Applying to main grid
					for a = 0, n_elements(site_ne) -1 do begin
					gridpos = where(gridindexarray eq site_ne(a),np)
					if np gt 0 then gridregionarray(gridpos) = 7
					endfor
					;************************
					;Region 8 - Nw of site
					site_nw = [520]
					;Applying to main grid
					for a = 0, n_elements(site_nw) -1 do begin
					gridpos = where(gridindexarray eq site_nw(a),np)
					if np gt 0 then gridregionarray(gridpos) = 8
					endfor
					;************************
					;Region 9 - SW of site
					site_sw = [565]
					;Applying to main grid
					for a = 0, n_elements(site_sw) -1 do begin
					gridpos = where(gridindexarray eq site_sw(a),np)
					if np gt 0 then gridregionarray(gridpos) = 9
					endfor
					;************************
					;Region 10 - SE of site
					site_se = [566]
					;Applying to main grid
					for a = 0, n_elements(site_se) -1 do begin
					gridpos = where(gridindexarray eq site_se(a),np)
					if np gt 0 then gridregionarray(gridpos) = 10
					endfor
					;************************
					;Region 11 - Tropical African - central and southern Africa 
					TropAf = [663,664,665,666,667,668,669,670,671,672,673,674,675,708,709,710,711,712,713,714,715,716,717,718,719,720,$
					753,754,755,756,757,758,759,760,761,762,763,764,765,798,799,800,801,802,803,804,805,806,807,808,809,810,843,844,845,846,847,848,849,850,851,852,853,854,855,888,889,890,891,892,893,894,895,896,897,898,899,900,$
					933,934,935,936,937,938,939,940,941,942,943,944,945]
					;Applying to main grid
					for a = 0, n_elements(TropAf) -1 do begin
					gridpos = where(gridindexarray eq TropAf(a),np)
					if np gt 0 then gridregionarray(gridpos) = 11
					endfor
					;************************
					;Region12 -South America
					South_Am =[406,407,408,409,410,411,412,413,414,415,416,417,418,419,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,604,601,602,603,604,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,650,695,696,697,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,901,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921]
					;Applying to main grid
					for a = 0, n_elements(South_Am) -1 do begin
					gridpos = where(gridindexarray eq South_Am(a),np)
					if np gt 0 then gridregionarray(gridpos) = 12
					endfor
					;************************
				regionpercentages = fltarr(12)
       			

				For thisregion = 1,12 do begin    ; for each region
					thisreg = 0.0
					isregion = where(gridregionarray eq thisregion,np)
					
						if np gt 0 then begin
						  for b = 0, np-1 do begin

							normlons = where(lons lt 0)
							if n_elements(normlons) gt 1 then lons(normlons) = lons(normlons) + 360.0
							isinbox = where(lats gt bottomgridlats(isregion(b)) and lats lt topgridlats(isregion(b)) and lons gt leftgridlons(isregion(b)) and lons lt rightgridlons(isregion(b)), np)
							if isinbox(0) ne -1 then thisreg = thisreg + total(pconcs(isinbox))  
							;if isinbox(0) ne -1 then thisreg = thisreg + total(concentration(isinbox))    ; CONCENTRATION only!!!
							regionpercentages(thisregion-1) = thisreg

					  	 endfor
						endif
				Endfor
	

			;opcsvfn = '/home/s/sle20/Atmos_chem/CapeVerde/'+'STEVIE'+ '.csv'
			opcsvfn = '/data/name/NAME_data/output_zoe/regional analysis/CapeVerde/Daily/'+'CV_regional2014extra'+ '.csv'

				if thisfile eq 0 and z eq 0 then begin
					openw,17, opcsvfn

					opstr='Filename,date,CoastalAfrican,Polluted_marine,Sahara,Sahel,NAmerica,Atlantic_marine,site_ne,site_nw,site_sw,site_se,TropAf,South_Am'
					printf,17, opstr
					

					
					
					opstr = fnstring + ',' + fnday + '/' + fnmonth + '/' + fnyear+Columns_Time[z]
						for b = 0, 11 do begin
							opstr = opstr + ',' + strtrim(regionpercentages(b),2)
						endfor
					printf,17, opstr

					close, 17


				endif else begin 
					openw,17, opcsvfn, /append


					opstr = fnstring + ',' + fnday + '/' + fnmonth + '/' + fnyear+Columns_Time[z]
				 		for b = 0, 11 do begin
							opstr = opstr + ',' + strtrim(regionpercentages(b),2)
						endfor
					printf,17, opstr

					close, 17

				endelse


				if plotout eq 1 then begin

					;********************************************
					;If I want to show legend1 (ColourScale), set this to 1
					showlegend1 = 0
					;********************************************
					;Location of legend1
					leg1x0 = 0.03
					leg1x1 = 0.26
					leg1y0 = 0.65
					leg1y1 = 0.97
					;********************************************


						if showlegend1 eq 1 then begin
							polyfill, [leg1x0,leg1x1,leg1x1,leg1x0],[leg1y0,leg1y0,leg1y1,leg1y1], color = 0, /normal
							polyfill, [leg1x0+0.01,leg1x1-0.01,leg1x1-0.01,leg1x0+0.01],[leg1y0+0.01,leg1y0+0.01,leg1y1-0.01,leg1y1-0.01], color = 255, /normal

								for a = 0, 254 do begin
									xs = [leg1x0+0.02, leg1x0+0.06, leg1x0+0.06,leg1x0+0.02]
									ys = [leg1y0 + 0.03+(a*0.001),leg1y0 + 0.03+(a*0.001),leg1y0 + 0.03+((a+1)*0.001),leg1y0 + 0.03+((a+1)*0.001) ]
									polyfill, xs, ys, color = a, /normal
								endfor

							plots, [leg1x0+0.02,leg1x0+0.02],[leg1y0 + 0.03,leg1y0 + 0.285], color = 0, /normal
							plots, [leg1x0+0.06,leg1x0+0.06],[leg1y0 + 0.03,leg1y0 + 0.285], color = 0, /normal
							plots, [leg1x0+0.02,leg1x0+0.06],[leg1y0 + 0.03,leg1y0 + 0.03], color = 0, /normal
							plots, [leg1x0+0.02,leg1x0+0.06],[leg1y0 + 0.285,leg1y0 + 0.285], color = 0, /normal

								for a = 0, 10 do begin
									plots, [leg1x0+0.02,leg1x0+0.08],[leg1y0 + 0.03+(a*0.0255),leg1y0 + 0.03+(a*0.0255)], color = 0, /normal
									mystr = string(10^(minc+((maxc-minc)/10.0) * a), FORMAT = '(F10.6)')
									;mystr=string(strtrim(exp(minc+((maxc-minc)/10.0*a)) ,2), FORMAT = '(F10.2)')
									xyouts, leg1x0+0.09, leg1y0 + 0.025+(a*0.0255), color = 0, mystr, /normal
								endfor

							xyouts, leg1x0+0.03, leg1y0 + 0.295, '% of total airmass', color = 0, /normal

						endif
					;********************************************
					;If I want to show legend2 (Runinfo), set this to 1
					showlegend2 = 0
					;********************************************
					;Location of legend2
					leg2x0 = 0.55
					leg2x1 = 0.98
					leg2y0 = 0.65
					leg2y1 = 0.97
					;********************************************


						if showlegend2 eq 1 then begin
							polyfill, [leg2x0,leg2x1,leg2x1,leg2x0],[leg2y0,leg2y0,leg2y1,leg2y1], color = 0, /normal
							polyfill, [leg2x0+0.01,leg2x1-0.01,leg2x1-0.01,leg2x0+0.01],[leg2y0+0.01,leg2y0+0.01,leg2y1-0.01,leg2y1-0.01], color = 255, /normal


							xyouts, leg2x0+0.03, leg2y0 + 0.295, 'Run Information', color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.275, 'Run name: ' + strtrim(runname,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.255, 'Run Time: ' + strtrim(runtime,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.235, 'Met Data: ' + strtrim(metdata,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.215, 'Start of Release: ' + strtrim(startofrelease,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.195, 'End of Release: ' + strtrim(endofrelease,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.175, 'Run Duration: ' + strtrim(runduration,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.155, 'X Grid Resolution: ' + strtrim(xgridresolution,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.135, 'Y Grid Resolution: ' + strtrim(ygridresolution,2), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.115, 'Model Run by Zoe Fleming and Roland Leigh', color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.095, 'Plot produced on:', color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.075, systime(), color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.055, 'Plotted on Version 1.0 of Leicester Software', color = 0, /normal
							xyouts, leg2x0+0.03, leg2y0 + 0.035, 'Author: Roland Leigh: July 2009', color = 0, /normal
						endif



						;if want logos on
						logoson = 0

							if logoson eq 1 then begin
								;Adding in logos
								;infn = 'W:\Campaigns\LAMP\Analysis\Modelling\lcc_logo.png'
								queryStatus = QUERY_IMAGE(infn, imageInfo)
								imageSize = imageInfo.dimensions
								img = read_png(infn)
								imageDims = SIZE(image, /DIMENSIONS)
								interleaving = WHERE((imageDims NE imageSize[0]) AND $
								   (imageDims NE imageSize[1])) + 1

								PRINT, 'Type of Interleaving = ', interleaving

								;TV, img, TRUE = interleaving[0] ,16
								;infn = 'W:\Campaigns\LAMP\Analysis\Modelling\airviro_logo.png'
								;img = read_png(infn)
								;TV, img, TRUE = interleaving[0] ,167


								;infn = 'W:\Campaigns\LAMP\Analysis\Modelling\smhi_logo.png'

								;img = read_png(infn)


								;TV, img, TRUE = 1 ,84
								infn = '/work/modelling/NAME/IDL_code/NAME_logos3.png'
								;infn = 'D:\IDL\Roland batch run Aug2009\Air mass sectors\NAME_logos3.png'

								img = read_png(infn)
								TV, img, TRUE =  interleaving[0] ,16

							endif




;plotting the colour map (make bigger than 0-80 Lat- make -30 to 80)[0,260, 80,50]; 4 July 2012

						window, 2, xsize = 1000, ysize = 800
						MAP_SET, /mercator,   LIMIT=[-30,260, 80,60], /CONTINENTS, TITLE=runname, /hires,E_CONTINENTS={FILL:1, color:200}, E_HORIZON={FILL:1, COLOR:80}
						
							for b = 0, ygrids -2 do begin
								for a = 0, xgrids -2 do begin
									xs = [gridlons(a), gridlons(a+1), gridlons(a+1), gridlons(a)]
									ys = [gridlats(b), gridlats(b), gridlats(b+1), gridlats(b+1)]
									;if more than 10 regions - change colour scaler here.
									;col = gridregionarray(a,b)*10.0 for 14 regions
									;greens very similar when use 30 PLAY with this to change colour of regions (Oct 2011)
									col = gridregionarray(a,b)*39.0;39.0
									if col eq 0 then col = 255
									polyfill, xs, ys, color = col
									;This puts text on top of the map output (Karen October 2011)
									;xyouts, gridlons(a)+(gridxresolution/4.0), gridlats(b)-(gridyresolution/3.0), strtrim(round((b*(xgrids-1))+a+1),2), color = 250
									;xyouts, gridlons(a)+(gridxresolution/8.0), gridlats(b)-(gridyresolution*3.0/4.0), strtrim(gridregionarray(a,b),2), color = 0, charsize = 2, charthick = 2
									;OPLOT, [-17.332667], [14.748886], PSYM=7, 	COLOR=10, SYMSIZE=2, THICK=3 ;Dakar
									;OPLOT, [-15.983217], [18.07295], PSYM=7, 	COLOR=10, SYMSIZE=2, THICK=3 ;Noaukchott
									;OPLOT, [-7.993983], [12.651325], PSYM=7, 	COLOR=10, SYMSIZE=3, THICK=3 ;Bamako
									OPLOT, [-16.574969], [13.437294], PSYM=7, 	COLOR=10, SYMSIZE=2, THICK=3 ;Banjul
									OPLOT, [-15.601186], [11.860089], PSYM=7, 	COLOR=10, SYMSIZE=4, THICK=3 ;Bissau
								endfor
							endfor

					MAP_CONTINENTS, /COUNTRIES,  COLOR=0, MLINETHICK=1
					MAP_CONTINENTS,  COLOR=0, MLINETHICK=1
					;contour, gridindexarray, indexgridlons, indexgridlats, /fill, nlevels = 25
					;plotting the colour map
					bits = strsplit(fn, '.', /extract)
					opfn = bits(0) + '_regionsBOO.png'
					write_png, opfn, tvrd(true = 1)
			endif ;plotout
endfor ;z loop

				;Dakar 14.748886, -17.332667)
				;Noaukchott 18.07295, -15.983217
				;Bamako 12.651325,-7.993983
				;Banjul 13.437294,- 16.574969
				;Bissau 11.860089, -15.601186
				OPLOT, [-17.332667], [14.748886], PSYM=7, 	COLOR=10, SYMSIZE=4, THICK=4  



endfor ; this file
			






end
