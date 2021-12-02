# Grain detector and Analyzer
Rice/Grains classification project at INFYU Labs, Research Park, IIT Madras.

## Requirements

1. Raspberry Pi
2. Raspberry Pi NOiR 8 MP Camera
3. Camera Cable
4. 3-D printed Body
5. Smooth matt black surface/ cardboard
6. Adhesive material/Double-sided tape
7. Light diffuser-traslucent material
8. 5000 mAh power bank
9. Micro USB cables
10. Micro USB 
11. MobaXtream/Putty

## Introduction
The advancements in technology has led to a drastic improvement in food manufacturing and processing industries. With the increase in consumers we are able to produce much more than ever. These products directly shape our health and physiology, as the production has increased it also becomes equally important for the industries to monitor and enforce regular inspections to keep up with the expected quality of the food products. 

When we particularly talk about the conventional grain processing Industries, quality checks are not really uniform and accurate, it's also expert dependent which are performed manually by humans using an individual's personal experience to identify the quality and type of the grains to classify them into various groups. Due to these limitations companies might also have to pay a big price in downtimes when there are unavailability of skilled workers or when the checks need to be performed remotely. 

Automation of such tasks can help us in every sphere. We can fasten the monitoring processes significantly which also means we can do multiple tests to verify the certainty of results at various stages of food processing. With the use of Computer vision and machine learning techniques we can perform automatic classification and analysis of food grains. After all these the device needs  to be inbuilt with methods and algorithms to eliminate false detections and unwanted samples.
Methodology/ Innovation behind
Hardware:
Design of the Handheld Grain Analyzer
The whole design was accomplished on Autodesk Fusion 360 for flexible usage. The design process went under 3 Major iterations.

### Lighting System
Two white light Leds spaced symmetrically on both sides of the camera with incorporation of proper diffusers to scatter light uniformly on the grain bed.

### Electronics
We are sampling our data using **Raspberry Pi NOiR camera** (8 MP), we manually adjust the focus of the camera by rotating the lens cap to bring it to focus at a distance of about **10 cm**. A specific box has been designed after several ideations and iterations for most feasible and compact placements of the various modules of the device.

## Code & the Algorithm
Image can be captured using the “**raspistill**” command on the raspberry pi terminal.

In the code we start with importing the image in **Grayscale format** and **resize** it down just for ease of Viewing on the Window as Original resolution is much more than desired.
We **Smoothen** the Image using **Median Blur** to dilute any unwanted internal or external Noise pixels. Then we process this image using “**Canny Edge detection**” to find the boundaries of the Rice grains. In the canny function, the Image is Converted into Binary using Adaptive Thresholding, so that variation of Lighting conditions can be handled. Then using convolution of Pixels, we convert the Binary thresholded image into an image with just the Edges of the rice grains.

After segmenting the backround from the rioce grians, various rice grains are required to be segmented seprately. To achieve this "Canny Edge detection” is used to generate edges around the Rice grains. After Edge detection, contour detection is done which detects the Edge coordinates and stores it as a multi-dimensional array. We get a set of countours for every components(a connected set).

Since rice are randomly spread on the platform, there could samples with overlapped grains. We can exclude the overlaps segmentaions using area criteria but this would reduce our sample sizeThere could be cases but before that we still need to segregate the touching rice grains which were processed as a single contour due to close contact. We will use the Convexity function around the curves of the rice contours to find the points of defects. Defects are the points where the contour of the two or more touching grains meets. We know that the shape of the rice is always oval and Convex from the outside, so whenever we encounter a concave curve around the contours it can only be as a result of some rice grains touching each other. There can be some exceptional cases that will outrun the above mentioned hypothesis, we will talk later about how we are excluding them from our results to make it error free. We have used convexHull and convexity Defects functions of OpenCV2 to find the defects as the various local maxima of Concavity in the contours. After we detect the Defects as the point of contact of the touching rice grains we separated the contours of by following two steps: First we draw a series of black line matching the background color to erase the edges joining the corners of the touching rice grains to separate the edge curves of the touching grains, then we run the Canny edge detection again over this modified image to get the new contours with most of the touching rice contours separated out. After we get our final contours we will approximate ellipses using fitEllipse function over each of the contours to find the characteristic features like Length, Breadth, Ratio and area of the rice grains. But before averaging and concluding with results we will exclude those processed samples which are exceptional as per our general hypothesis and can lead to an error in our final Averaged Output. We use categorization on the basis of Ratios (length:width) and Area of the ellipses to exclude the unwanted contours outliers from the detected contours.

After we get our final contours we will approximate ellipses using **fitEllipse** function over each of the contours to find the characteristic features like Length, Breadth, Ratio and area of the rice grains. But before averaging and concluding with results we will exclude those processed samples which are exceptional as per our general hypothesis and can lead to an error in our final Averaged Output.

We use categorization on the basis of Ratios (length:width) and Area of the ellipses to exclude the unwanted contours outliers from the detected contours.
