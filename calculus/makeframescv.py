#from PIL import Image
import numpy as np
import cv2
from subprocess import Popen, PIPE
#for i in range(1,25):
#	im = Image.open("img"+str(i)+".png")
#	rgb_im = im.convert('RGB')
#	rgb_im.save("img"+str(i)+".gif", "GIF")







for i in range(1,1):
	if i % 2 == 1:
		im = cv2.imread("img"+str(i)+".jpeg")
		if imgnext < 10:
			cv2.imwrite("img00"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
		elif imgnext < 100:
			cv2.imwrite("img0"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
		elif imgnext < 1000:
			cv2.imwrite("img"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
	else:
		im = cv2.imread("img"+str(i)+".jpeg")
		for ii in range(0,nmid+1):
			if ii > 0:
				im = im[0:602, nshift:]
				im = cv2.copyMakeBorder(im,0,0,0,nshift,cv2.BORDER_CONSTANT,value=[255,255,255])
			if imgnext < 10:
				cv2.imwrite("img00"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1
			elif imgnext < 100:
				cv2.imwrite("img0"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1
			elif imgnext < 1000:
				cv2.imwrite("img"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1


def makeframes(hashprefix,nimages):
	sizewidth = 600
	f = open('images/new/'+hashprefix+'inputs.txt','w')
	imgnext = 1
	nmid = 8
	nshift = int(sizewidth/nmid)
	im = cv2.imread('images/new/'+hashprefix+'ex'+str(0)+".png")
	im = cv2.copyMakeBorder(im,10,10,10,10,cv2.BORDER_CONSTANT,value=[255,255,255])
	allims = [im[0:sizewidth, 0:sizewidth]]
	for iimage in range(0,nimages-1):
		im = cv2.imread('images/new/'+hashprefix+'ex'+str(iimage+1)+".png")
		im = cv2.copyMakeBorder(im,10,10,10,10,cv2.BORDER_CONSTANT,value=[255,255,255])
		im = im[0:sizewidth, 0:sizewidth]
		allims.append(im)
		
		im0 = cv2.copyMakeBorder(allims[iimage],0,0,0,sizewidth,cv2.BORDER_CONSTANT,value=[255,255,255])
		cv2.imwrite('images/new/'+hashprefix+'img'+str(imgnext)+".bmp", im0)
		f.write("file '"+hashprefix+'img'+str(imgnext)+".bmp'\nduration 2\n")
		imgnext += 1

		im1 = np.concatenate((allims[iimage], allims[iimage+1]), axis=1)
		cv2.imwrite('images/new/'+hashprefix+'img'+str(imgnext)+".bmp", im1)
		f.write("file '"+hashprefix+'img'+str(imgnext)+".bmp'\nduration 2\n")
		imgnext += 1

		for ii in range(1,nmid+1):
			im1 = im1[0:sizewidth, nshift:]
			im1 = cv2.copyMakeBorder(im1,0,0,0,nshift,cv2.BORDER_CONSTANT,value=[255,255,255])
			cv2.imwrite('images/new/'+hashprefix+'img'+str(imgnext)+".bmp", im1)
			f.write("file '"+hashprefix+'img'+str(imgnext)+".bmp'\nduration 0.1\n")
			imgnext += 1

	im0 = cv2.copyMakeBorder(allims[nimages-1],0,0,0,sizewidth,cv2.BORDER_CONSTANT,value=[255,255,255])
	cv2.imwrite('images/new/'+hashprefix+'img'+str(imgnext)+".bmp", im0)
	f.write("file '"+hashprefix+'img'+str(imgnext)+".bmp'\nduration 2\n")

	f.close()




	