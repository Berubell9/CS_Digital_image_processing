from PIL import Image
import numpy as np
import cmath
import sys

class ImageManager:
    
    #attributes
    width = None
    height = None
    bitDepth = None
    
    img = None
    data = None
    original = None
    
    def read(self, fileName):
        global img
        global data
        global original
        global width
        global height
        global bitDepth
        img = Image.open(fileName)
        data = np.array(img)
        original = np.copy(data)
        width = data.shape[0]
        height = data.shape[1]
        mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32,"YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
        bitDepth = mode_to_bpp[img.mode]
        print("Image %s width %s x %s pixels (%s bits per pixel) has been read!" % (img, width, height, bitDepth))

    def write(self, fileName):
        global img
        img = Image.fromarray(data)
        try:
            img.save(fileName)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileName))
    
    # Gray Scale
    def convertToGrayscale(self):
        global data
        for y in range(height):
            for x in range(width):
                r = data[x, y, 0]
                g = data[x, y, 1]
                b = data[x, y, 2]
                gray = (int)((0.2126*r) + int(0.7152*g) + int(0.0722*b))
                data[x, y, 0] = gray  
                data[x, y, 1] = gray  
                data[x, y, 2] = gray  
    
    # Erosion
    def erosion(self, se):
        
        global data
        
        self.convertToGrayscale()
        
        data_zeropaded = np.zeros([width + se.width * 2, height + se.height * 2, 3])
        data_zeropaded[se.width - 1:width + se.width - 1, se.height - 1:height + se.height - 1, :] = data
        
        for y in range(se.height - 1, se.height + height - 1):
            for x in range(se.width - 1, se.width + width - 1):
                
                subData = data_zeropaded[x - int(se.origin.real):x - int(se.origin.real) + se.width, y - int(se.origin.imag):y - int(se.origin.imag) + se.height, 0:1]
                
                subData = subData.reshape(3, -1)
                
                for point in se.ignoreElements:
                    
                    subData[int(point.real), int(point.imag)] = se.elements[int(point.real),int(point.imag)]
                    
                min = np.amin(se.elements[se.elements > 0])
                
                if (0 <= x - int(se.origin.real) - 1 < width and 0 <= y - int(se.origin.imag) - 1 < height):
                    if (np.array_equal(subData, se.elements)):
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = min
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = min
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = min
                    else:
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = 0
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = 0
                        data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = 0
                        
    
    
    
class StructuringElement:
    elements = None
    width = 0
    height = 0
    origin = None
    ignoreElements = None
    
    def __init__(self, width, height, origin):
        self.width = width
        self.height = height
        
        if (origin.real < 0 or origin.real >= width or origin.imag < 0 or origin.imag >= height):
            self.origin = complex(0, 0)
        else:
            self.origin = origin
            
        self.elements = np.zeros([width, height])
        self.ignoreElements = []
   