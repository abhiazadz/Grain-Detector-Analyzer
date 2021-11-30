import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

print ("Starting")

orig = cv2.imread ('C:/Users/abhia/Desktop/INFY U/data/photo3.jpg', cv2.IMREAD_UNCHANGED)
orig = cv2.resize(orig, (800, 600)) #resizing
orig2 = orig
orig3 = orig

img = cv2.imread ('C:/Users/abhia/Desktop/INFY U/data/photo3.jpg',0);  # load in grayscale mode
img = cv2.resize(img, (800, 600)) #resizing
img = cv2.medianBlur (img, 5)

cv2.imshow("Resized image", img)
cv2.waitKey(0)
 
#imgg = cv2.bitwise_not(img);
#cv2.imwrite("dstinvert.png", imgg);
#canny_edges = cv2.Canny(img,100,200)

#imgg = cv2.medianBlur (img, 1)
ret, th1 = cv2.threshold (img, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold (img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 119, 1)
th3 = cv2.adaptiveThreshold (img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 119, 1)

#cv2.imshow('Th1',th1)
#cv2.waitKey(0)

kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
#opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel) 

#EDGE DETECTION using canny
#using Canny
#canny_edges = cv2.Canny(img,100,250)
#canny_inv=cv2.bitwise_not(canny_edges)

#OR Try this if it gives a better result in case we have bacckground noise...
edged = cv2.Canny(img, 100, 250)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
#edged = cv2.bitwise_not(edged);
cv2.imshow('1st Edge detection',edged)
cv2.waitKey(0)

#### Size detection
#contours, hierarchy = cv2.findContours (th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#xx=cv2.drawContours(th3, contours, 1, (0, 255, 0), 7)

#### OR try this
contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#conversion into correct format using imutils.grab_contours()
contours = imutils.grab_contours(contours)
xx=cv2.drawContours(orig, contours, -1, (0, 255, 0),1)

#cv2.imshow("Contours", xx)
#cv2.waitKey(0)

print(len(contours))
########################################################
########################################################

#1. find the defects in convex hull with respect to the rice contours
for contour in contours:
    #epsilon = 0.1 * cv2.arcLength(contour, True)
    #approx = cv2.approxPolyDP(contour, epsilon, True)
    #x, y, w, h = cv2.boundingRect(approx)
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    #yy=cv2.drawContours(orig,contours,0,(200,0,0),1)
    #print(defects)
    area = cv2.contourArea(contour)
    #print(area)
    j=0
    if np.any(defects!=None):
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            #print(far, d)
            if d>1000 and area>800:     
                cv2.line(orig,start,end,[200,100,30],1)
                cv2.circle(orig,far,5,[100,0,255],-1)
                if j==0:
                    far2=far
                    j=j+1
                if j==1:
                    #cv2.line(edged,far,far2,[255,255,255],5)
                    cv2.line(edged,far,far2,[0,0,0],5)
                    cv2.circle(edged,far,5,[0,0,0],-1)
            #print(far)
            #print('next')
        #cv2.drawContours(edged,contours,0,(200,0,0),1)
    
cv2.imshow('1.contours with defects and convex hull',orig)
cv2.waitKey(0)

cv2.imshow('edge image after drawing',edged)
cv2.waitKey(0)
#########################################################
#########################################################

#img = cv2.medianBlur (img, 3)
#edged = cv2.Canny(img, 100, 250)
#edged = cv2.dilate(edged, None, iterations=1)
#edged = cv2.erode(edged, None, iterations=1)

#cv2.imshow('Canny edge detection 2',edged)
#cv2.waitKey(0)

#edge detection by laplacian and drawing2
laplacian = cv2.Laplacian(edged,cv2.CV_64F) 

#cv2.imshow('edge detection by laplacian and drawing2',laplacian)
#cv2.waitKey(0)

#edged = cv2.Canny(img, 100, 250)
#cv2.imshow('Canny edge detection after laplacian and drawing2',edged)
#cv2.waitKey(0)

contours = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
yy=cv2.drawContours(orig3, contours, -1, (0, 255, 0),1)

cv2.imshow("Contours 2nd time", yy)
cv2.waitKey(0)

#############################################################

pixelsPerMetric = None
i=0
for cnt in contours:
    area = cv2.contourArea(cnt)
    print(area)
    if area>10:
        #rect = cv2.minAreaRect(ellipse)
        rect = cv2.fitEllipse(cnt)
        #print(rect)
        im = cv2.ellipse(orig,rect,(255,10,0),2)
        #cv2.imshow("ellipsce contours", im)
        #cv2.waitKey(0)
        if (rect[1][0] != 0) and (rect[1][1] != 0):
            if rect[1][1] >= rect[1][0]:
                ratio=rect[1][1]/rect[1][0]
            else:
                ratio=rect[1][0]/rect[1][1]    
        print(ratio)
        box = cv2.boxPoints(rect)
        #print('box',box)
        ###converting tuples to int values
        box = np.int0(box)
        #print('np.into(box)',box)
    
        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / 1

        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}in".format(dimA),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 1)
        cv2.putText(orig, "{:.1f}in".format(dimB),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 1)

        # show the output image
        #cv2.imshow("Image", orig)
        #cv2.waitKey(0)
        cv2.drawContours(orig,[box],0,(200,23,200),1)

    #x,y=np.int0(tuple(cnt[1][0]))
    ##check area of each contours, if open contouts area are not taken in closed way..
    #cv2.putText(orig, "No.{:}".format(area),(x,y), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
    #i=i+1

cv2.imshow('Original',orig)
cv2.waitKey(0)

cv2.destroyAllWindows
