import math
import numpy as np
from matplotlib import pyplot as plt 

n = 1.5
lamda = 650e-6 #mm
beta = 40*1/3600*np.pi/180
h = 2.6                         #thickness of the wedge plate (mm)
incident_angle = 45*np.pi/180   # rad
gamma = 80*np.pi/180            # rad
s = h*np.sin(2*incident_angle)/math.sqrt(n*n - pow(np.sin(incident_angle),2))   #mm
print(s)

omega_0 = 1  #mm
f = np.pi*omega_0*omega_0/lamda
z = list(range(100,100000,100))
R = []
z_num = len(z)
for i in range(0,z_num):
	Radius = z[i] + f*f/z[i]
	R.append(Radius)

# R = list(range(1000,50000,1000))

thetaset = []
thetaset_ = []
diff = []
deltax_set = []
e_set=[]

R_num = len(R)
for i in range(0,R_num):
	tan_theta =s/(2*n*beta*R[i])
	tan_theta_ = (s/R[i] + 2*n*beta*math.cos(gamma))/(2*n*beta*math.sin(gamma))
	theta = math.atan(tan_theta)
	theta_ = math.atan(tan_theta_)
	e = lamda*R[i]*math.sin(theta)/s
	deltax = lamda * R[i] / s
	thetaset.append(theta) 
	thetaset_.append(theta_)
	e_set.append(e)
	deltax_set.append(deltax)
	diff.append(theta_-theta)

	
print(diff[1:100])
plt.figure(1)
plt.subplot(4,1,1)
plt.plot(z,R,'g-')
plt.xlabel('z (mm)')
plt.ylabel('R (mm)')
plt.subplot(4,1,2)
plt.plot(z,thetaset,'r-',z,thetaset_,'y-',z,diff,'g-')
plt.xlabel('z (mm)')
plt.ylabel('theta (rad)')
plt.subplot(4,1,3)
plt.plot(z,e_set,'b-')
plt.xlabel('z (mm)')
plt.ylabel('Distance (mm)')
plt.subplot(4,1,4)
plt.plot(z,deltax_set,'k-')
plt.xlabel('z (mm)')
plt.ylabel('dx (mm)')
plt.show()

