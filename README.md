
**Provided:**
A FITS file is provided with a galaxy present it. We need to find the separation between the two inner edges

**Approach used:**
We use the technique of Hough Transformation to roughly draw the circle and also find the radius of the drawn circle. Since, the FITS image provided is very dark and noisy, we use some preprocessing steps to implement Hough's Transform efficiently


```python
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm
import cv2
```

Image is first trimmed to region of interest in order to simplify the processing, as looping for a bigger image with majority of it being not very helpful as it does not contain any useful data.


```python
def trim_image(image):
    n=int(image.shape[0]/9)
    maximum = 0
    cut_image=np.zeros([n,n])
    for i in range(9):
        for j in range(9):
            s = np.sum(image[i*n:(i+1)*n,j*n:(j+1)*n])
            if s>maximum:
                maximum = s
                cut_image = image[i*n:(i+1)*n,j*n:(j+1)*n]
    return cut_image
```

Otsu's Thresholding technique is used to Threshold the image to make it binary, so that we can perform Morphological Operations on it


```python
def get_histogram(img):
    max_val = np.amax(img)
    k=1
    while k<max_val:
        k=k*2
    histogram = np.zeros(k)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            histogram[img[i][j]] = histogram[img[i][j]]+1
    return histogram
        
def otsu_threshold(hist,graph=False):
    sig=[]
    for mid in range(2,len(hist)):
        background = hist[:mid-1]
        foreground = hist[mid:]
        N = sum(hist)
        Wb = sum(background)/N
        Wf = sum(foreground)/N
        ub,uf,Nb,Nf=0,0,sum(background),sum(foreground)
        sigmaB,sigmaF = 0,0
        ub = sum(np.arange(len(background))*background)/ (Wb*N+1)
        #for m in range(len(background)):
         #   sigmaB = sigmaB + (m-ub)**2*background[m]/Nb
        sigmaB = sum((np.arange(len(background))-ub)**2*background)/Nb
        
        uf = sum(np.arange(len(foreground))*foreground)/ (Wf*N+1)
        #for n in range(len(foreground)):
        #    sigmaF = sigmaF + (n-uf)**2*foreground[n]/Nf
        sigmaF = sum((np.arange(len(foreground))-uf)**2*foreground)/Nf
        

        sig.append(Wb*sigmaB + Wf*sigmaF)
    if graph:
        plt.plot(np.arange(len(sig)),sig)
        plt.title("Weighted inter-class variance")
        plt.show()
    sig = np.nan_to_num(sig)
    return np.nonzero(sig==np.amin(sig[sig!=0]))[0]

def thresholder(img,t):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > t:
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img
```

Defining basic Morphological Operations methods, so that we can call them later.


```python
def morphological_operate(img,ker,choice='dilate'):
    
    img_ = np.zeros(img.shape)
    kx,ky = ker.shape
    kx,ky = int(kx/2),int(ky/2)
    for i in range(kx,img.shape[0]-kx):
        for j in range(ky,img.shape[1]-ky):
            select = img[i-kx:i+kx+1,j-ky:j+ky+1]
            if choice=='erode':
                img_[i][j] = np.logical_not(np.sum(np.logical_not(select).any() and ker.any()))
            elif choice=='dilate':
                img_[i][j] = np.sum(select.any() and ker.any())
    return img_.astype(int)

def open_close(img,SE,iteration=1):
    img_cl = img.copy()
    for i in range(iteration):
        img_cl = morphological_operate(morphological_operate(img_cl,SE,'erode'),SE,'dilate')
        img_cl = morphological_operate(morphological_operate(img_cl,SE),SE,'erode')

    return img_cl
```

Implementing Hough's transform to detect circles.


```python
def get_circles(img,dp=1.8,minDist=25):
    img = cv2.imread('readyImage.png',1)
    img = cv2.Canny(img,10,1)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp,minDist)
    if circles is not None:
        return circles[0, :]
    else:
        return circles
```

Preprocessing Images include

- Converting normalised image into 'Int32' dtype, so that we can get histogram from 0-255
- Threshold the Image, to Binarize the image
- Perform Opening of image, followed by Closing, in order to eliminate noisy stars


```python
def moving_avg(arr,n=5,iteration=2):
    new_arr=[]
    for i in range(len(arr)-n):
        new_arr.append(sum(arr[i:i+n])/n)
    for j in range(iteration-1):
        for i in range(len(new_arr)-n):
            new_arr[i]=sum(arr[i:i+n])/n
    return new_arr

def unimodal_threshold(histogram):
    H=[]
    histogram= histogram/np.amax(histogram)
    for i in range(1,256):
        H.append(((histogram[i]+1)/(histogram[i-1]+1))**2)
    threshold = np.nonzero(H==np.amax(H))[0][0]
    return threshold+1
    
    #smooth_hist = moving_avg(histogram.copy(),iteration=5)
    #dif_hist = np.abs(np.diff(smooth_hist))
    #return otsu_threshold(dif_hist)[0]
```


```python
def preprocess(image):
    image = ((image+0.5)*255).astype('int32')
    
    
    #otsu_thres = otsu_threshold(get_histogram(image.copy()))-25
    #img_t = thresholder(image.copy(),otsu_thres)
    #print("Thresholding Value = ",otsu_thres)
    unimod_thres = unimodal_threshold(get_histogram(image.copy()))
    img_t = thresholder(image.copy(),unimod_thres)
    print("Thresholding Value = ",unimod_thres)
    
    
    SE = np.ones([3,3])
    morph_img = open_close(img_t.copy(),SE)
    morph_img = morphological_operate(morph_img.copy(),np.ones([5,5]),'erode')
    
    return morph_img
```


```python
filename = 'NGA_NGC3351-fd-int.fits'
NGA = fits.open(filename)
image = NGA[0].data
plt.subplot(1,2,1)
plt.imshow(image,cmap='gray')
plt.title("Original")
image = trim_image(image)
plt.subplot(1,2,2)
plt.imshow(image,cmap='gray')
plt.title("Zommed In")
plt.show()
```


    
![png](output_13_0.png)
    



```python
proc_image = preprocess(image.copy())
plt.subplot(1,2,1)
plt.imshow(image,cmap='gray')
plt.title("Zommed In")
plt.subplot(1,2,2)
plt.imshow(proc_image,cmap='gray')
plt.title("Preprocessed")
plt.show()
```

    Thresholding Value =  127



    
![png](output_14_1.png)
    



```python
plt.imshow(proc_image,cmap='gray')
plt.xticks([],[])
plt.yticks([],[])
plt.imsave('processedImage.png',proc_image)
```


    
![png](output_15_0.png)
    



```python
circles = get_circles('processedImage.png')
```


```python
morph_img = np.logical_xor(morphological_operate(proc_image.copy(),np.ones([3,3]),'erode'),proc_image)

circles_draw = np.zeros(proc_image.shape)
for (x,y,r) in circles.astype('int'):
    cv2.circle(circles_draw,(x,y),r,1,2)
plt.imshow(np.logical_or(circles_draw,morph_img),cmap='gray')
plt.title("Detected Circle")
plt.show()
```


    
![png](output_17_0.png)
    



```python
for (x,y,r) in circles:
    print("Diameter of the Circle = ",r*2)
```

    Diameter of the Circle =  96.12000274658203

