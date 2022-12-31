import numpy as np
import fitz
from PIL import Image
from io import BytesIO, StringIO
import cv2
import matplotlib.pyplot as plt
import math
from scipy import ndimage
from zipfile import ZipFile

class Methods:

    def __init__(self, mode: str="main", image: any=None, rotation_flag: bool=False, noise_flag: bool=False):
        self.__image = image
        self.rotation_flag = rotation_flag
        self.remove_noise_flag = noise_flag
        #self.zoom = fitz.Matrix(300 / 72, 300 / 72)

    def get_image(self) -> any:
        return self.__image
    
    def set_image(self, image: any) -> None:
        self.__image = image

    def remove_noise(self, image):
        
        imgray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        ret, masked_img = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
        ret, masked_img = cv2.threshold(masked_img, 127, 255, cv2.THRESH_BINARY_INV)

        return masked_img
    
    def rotation_table(self, output_dir, name, image):

        imgray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        width, height = image.shape[:-1]
        length = width * height
        
        image_np = np.array(image)

        ret, masked_img = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((7, 7), np.uint8)
        img_dilation = cv2.dilate(masked_img, kernel, iterations=8)
        ret, masked_img = cv2.threshold(img_dilation, 127, 255, cv2.THRESH_BINARY_INV)

        img_contours = image_np.copy()
        contours, hierarchy = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        residual = cv2.drawContours(img_contours, contours[1:], -1, color=(0, 255, 0))
        
        cont = 1
        for c in contours:

            img_box = image_np.copy()
            area = cv2.contourArea(c)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            if area > 2000 and 0.95 > area / length:
                
                center = (int(rect[0][0]),int(rect[0][1])) 
                width = int(rect[1][0])
                height = int(rect[1][1])
                angle = int(rect[2])

                
                if width < height:
                    angle = 90 - angle
                else:
                    angle = -angle
                
                output_img = image_np.copy()
                
                output_img = ndimage.rotate(image, -angle, cval=255)

                
                name_file = output_dir + '\\' + name[:-4]+'_rotation{}.png'.format(cont)
                
                cont += 1
                cv2.imwrite(name_file, output_img)

    def rotation_table_streamlit(self, image):

        imgray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        images = []
        width, height = image.shape[:-1]
        length = width * height
        
        image_np = np.array(image)

        ret, masked_img = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((7, 7), np.uint8)
        img_dilation = cv2.dilate(masked_img, kernel, iterations=8)
        ret, masked_img = cv2.threshold(img_dilation, 127, 255, cv2.THRESH_BINARY_INV)

        img_contours = image_np.copy()
        contours, hierarchy = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        residual = cv2.drawContours(img_contours, contours[1:], -1, color=(0, 255, 0))
        
        
        for c in contours:

            img_box = image_np.copy()
            area = cv2.contourArea(c)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            if area > 2000 and 0.95 > area / length:
                
                center = (int(rect[0][0]),int(rect[0][1])) 
                width = int(rect[1][0])
                height = int(rect[1][1])
                angle = int(rect[2])

                
                if width < height:
                    angle = 90 - angle
                else:
                    angle = -angle
                
                output_img = image_np.copy()
                
                output_img = ndimage.rotate(image, -angle, cval=255)
                #images.append(np.array(output_img))
                images.append(Image.fromarray(np.uint8(output_img)).convert('RGB'))
        return images

    def run(self, path_files, name_files, output_dir):
        
        for path, name in zip(path_files, name_files):
            print(path)
            img = Image.open(path)
            img = np.array(img)
            if self.rotation_flag:
                img = self.rotation_table(output_dir, name, img)       
    
    def run_streamlit(self):

        #for page_i, page in enumerate(self.__image):

        #pix = page.get_pixmap(matrix=self.zoom)
        #img = Image.open(BytesIO(pix.tobytes()))
        img_np = np.array(self.get_image())
        #if self.remove_noise_flag:
            #img_np = self.remove_noise(img_np)
        if self.rotation_flag:
            img_np = self.rotation_table_streamlit(img_np)
        print(img_np)
        return img_np

    def run_methods(self, objects):
        
        if 'Rotation' in objects:
            self.rotation_flag = True 
        if 'Remove Noise' in objects:
            self.remove_noise_flag = True