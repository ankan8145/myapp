import cv2 #for image processing
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

def read_file(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.imshow(img)
    plt.axis('off')
    return img


#-- create Edge Mask --#
def edge_mask(img, line_size, blur_value):
    """Input : Input Image
       Output : Edges of Image"""
    
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    
    return edges



# -- Reduce The Color Palettev -- #
def color_quantization( img, k):
    
    # Transform the image 
    data = np.float32(img).reshape((-1,3))
    
    # Determine Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    
    #Implementing K-means
    
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    
    result = center [label.flatten()]
    result = result.reshape(img.shape)
    
    return result





def cartoon(file):

    filename = file

    img = read_file(filename)

    line_size, blur_value = 9, 9
    edges = edge_mask(img, line_size, blur_value)
    plt.imshow(edges, cmap="binary")

    img_quantiz = color_quantization(img, k=4)
    plt.imshow(img_quantiz)
    plt.axis('off')
    blurred = cv2.bilateralFilter(img_quantiz, d=3, sigmaColor = 200, sigmaSpace=200)
    plt.imshow(blurred)
    plt.axis('off')


    c = cv2.bitwise_and(blurred, blurred, mask = edges)
    
    plt.imshow(c)
    plt.title("Cartoonified image")
    plt.axis('off')
    # plt.show()

    #-- Convert array to image --#
    array = np.array(c, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(str(filename))
    
# cartoon("img.jpg")