# python 3.6 Opencv 3.3
# require for numpy and matplotlib package
# Use this to illustrate how parameters influence the threshold result
# Find the para to a settled optical environment  
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt


def rad2deg(rad):
	return rad*180/np.pi

ResolutionX = 320
ResolutionY = 240

target = cv2.imread('SIimg0000.jpg',0)
target = cv2.resize(target,(ResolutionX,ResolutionY))
cv2.imshow('SIimg',target)

targetl = target[:,0:int(ResolutionX/2)]                 #left side pattern
targetr = target[:,int(ResolutionX/2):ResolutionX]       #right side pattern
# cv2.imshow('targetl',targetl)
# cv2.imshow('targetr',targetr)

tarblur = cv2.medianBlur(targetr,9)
cv2.imshow('SIimg1',tarblur)

# ----------------------------the manualy set thresholding-----------------------------------------
ret,tarbin = cv2.threshold(tarblur,np.median(tarblur)-5,255,cv2.THRESH_BINARY)  #-5
cv2.imshow('SIimg3',tarbin)

#-----------------------------adaptive threshold (regional mean method) at different parameters---- 
plt.figure();
for i in range(-10,10):
	tarbin = cv2.adaptiveThreshold(tarblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,111,i)
	plt.subplot(4,5,i+11)
	plt.imshow(tarbin,'gray')
	plt.title(str(i))
	plt.xticks([]),plt.yticks([])
plt.figure();
for i in range(-10,10):
	tarbin = cv2.adaptiveThreshold(tarblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,91,i)
	plt.subplot(4,5,i+11)
	plt.imshow(tarbin,'gray')
	plt.title(str(i))
	plt.xticks([]),plt.yticks([])
plt.figure();
for i in range(-10,10):
	tarbin = cv2.adaptiveThreshold(tarblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,71,i)
	plt.subplot(4,5,i+11)
	plt.imshow(tarbin,'gray')
	plt.title(str(i))
	plt.xticks([]),plt.yticks([])
plt.figure();
for i in range(-10,10):
	tarbin = cv2.adaptiveThreshold(tarblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51,i)
	plt.subplot(4,5,i+11)
	plt.imshow(tarbin,'gray')
	plt.title(str(i))
	plt.xticks([]),plt.yticks([])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()