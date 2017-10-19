# python 3.6 opencv 3.3
# Shearing Interference Measurement 2017.10.18
import cv2
import numpy as np
import math


def rad2deg(rad):
	return rad*180/np.pi

# ------------decide whether this point is in the original zone(before rotation)
#  which requires consideration -----------------------------------------------------
def p_decision(rows,cols,theta,x,y):	# note: x axis here aligns to rows axis
	xc = rows/2
	yc = cols/2
	dx = x - xc
	dy = y - yc
	r = math.sqrt(dx*dx+dy*dy)
	if x == xc:
		alpha = np.sign(dy) * np.pi /2
	else:
		alpha = np.arctan((y-yc)/(x-xc))
		if x < xc:
			alpha = alpha + np.pi
	alpha_ = alpha + theta
	x_ = xc + r*np.cos(alpha_)
	y_ = yc + r*np.sin(alpha_)
	return (x_>0) and (x_<rows) and (y_>0) and (y_<cols)
#-------------------------------------------------------------------------------------

#-------------------------------------optical parameter----------------------------------------
pixel2real = 1.55e-3*10.25   	# pixel --> mm
incident_angle = 45*np.pi/180   # rad
optical_length_delta = 606      # mm
beta = 40*1/3600*np.pi/180      #angle of the wedge plate  (rad)
h = 2.6                         #thickness of the wedge plate (mm)
n = 1.5                         #index of refraction
wavelength = 650e-6             #wavelength (mm) 
s = h*np.sin(2*incident_angle)/math.sqrt(n*n - pow(np.sin(incident_angle),2))	  #shearing distance (mm)						
R = [1,-1]

# ------------------------------image para and split para---------------------------------------
ResolutionX = 320
ResolutionY = 240
SplitPos = int(ResolutionX/2)
pic = 1   #which one part to be selected 0:left 1:right

label=['--------------------left pattern----------------------------------------',
       '--------------------right pattern---------------------------------------']


# -----------------------------image process-----------------------------------------------
target = cv2.imread('SIimg0000.jpg',0)
target = cv2.resize(target,(ResolutionX,ResolutionY))
cv2.imshow('SIimg',target)

targetl = target[:,0:SplitPos]                 #left side pattern
targetr = target[:,SplitPos:ResolutionX]       #right side pattern
targetset=[targetl,targetr];
# cv2.imshow('targetl',targetl)
# cv2.imshow('targetr',targetr)



tarblur = cv2.medianBlur(targetset[pic],9)
cv2.imshow('SIimg1',tarblur)
# tarblur = cv2.GaussianBlur(tarblur,(13,13),0)
# cv2.imshow('SIimg2',tarblur)
# print (tarblur)
# print (np.mean(tarblur))
# print (np.median(tarblur))
# print (np.var(tarblur))
tarbin = cv2.adaptiveThreshold(tarblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,71,4)
cv2.imshow('SIimg3',tarbin)
tarbin = cv2.medianBlur(tarbin,17)
cv2.imshow('SIimg4',tarbin)
taredges = cv2.Canny(tarbin,20,30,apertureSize=3)
cv2.imshow('SIimg5',taredges)
lines = cv2.HoughLines(taredges,1,np.pi/180,45)
print (lines)

theta_set = lines[:,0,1]
theta_result = np.mean(theta_set)

print(theta_result,rad2deg(theta_result))

rotate_theta = rad2deg(theta_result-np.pi/2)
rows,cols = tarbin.shape[:2]
print(cols,rows)
rotateM = cv2.getRotationMatrix2D((cols/2,rows/2),rotate_theta,1)   #positive angle if count-clockwise; negative angle if clockwise
tar_rotate = cv2.warpAffine(tarbin,rotateM,(cols,rows))
cv2.imshow('SIimg6',tar_rotate)

for y in range(0,rows):
	white = 0
	black = 0
	for x in range (0,cols):
		x1 = x
		if p_decision(rows,cols,np.pi/2-theta_result,y,x1):
			if tar_rotate[y][x1] > 128 :
				white = white + 1	
			else:
				black = black + 1
	if black > white + int(cols/3):
		cv2.line(tar_rotate,(0,y),(cols,y),(0,0,0),1)	#for visualize need; 
	else:
		cv2.line(tar_rotate,(0,y),(cols,y),(255,255,255),1)
cv2.imshow('SIimg7',tar_rotate)
tar2edge = cv2.Canny(tar_rotate,25,30,apertureSize=3)
lines2 = cv2.HoughLines(tar2edge,1,np.pi/180,70)
print(lines2)


spacing_acc = 0
linenum2 = lines2.shape[0]
if linenum2%2 == 0 :
    linenum2 = linenum2-1
spacing = [0 for x in range(0,linenum2-1)]
for x in range(0,linenum2-1):
    # if lines2[x][0][1]==np.pi/2 and lines2[x+1][0][1]==np.pi/2:
    spacing[x] = lines2[x+1][0][0] - lines2[x][0][0]
    spacing_acc = spacing_acc + spacing[x]
if linenum2 > 1:
    spacing_result = 2*spacing_acc/(linenum2-1)


period = spacing_result/np.sin(theta_result)    # in pixels
R[pic] = R[pic]*period*pixel2real*s/(wavelength - 2*period*pixel2real*n*beta)


print(label[pic])
print('distance of the pattern:',spacing_result,'pixels  ',spacing_result*pixel2real,'mm')
print('theta of the pattern:',theta_result,'rad  ',rad2deg(theta_result),'degree')
print('period of the pattern:',period,'pixels  ',period*pixel2real,'mm')
print('Radius:', R[pic],'mm')


cv2.waitKey(0)
cv2.destroyAllWindows()