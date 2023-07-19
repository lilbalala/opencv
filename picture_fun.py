import math

import cv2
import numpy as np


###############图像翻转####################################################
def flipfun(image,x):    #图像  水平翻转:0   垂直翻转:1  沿xy轴翻转:-1
    image = cv2.flip(image,x)
    return image


####################灰度图和二值化########################################


def gray_picture(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_gray


def erzhihua(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rst = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return rst[1]

################图像锐化#####################


def lap_9(image):                                               #拉普拉斯变化
    lap_9 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # 拉普拉斯9的锐化
    image = cv2.filter2D(image, cv2.CV_8U, lap_9)
    return image


def gama_transfer(img,power1=1.5):                              #伽马变化
    if len(img.shape) == 3:
         img= cv2.cvtColor(img,cv2.CV_8U)
    img = 255*np.power(img/255,power1)
    img = np.around(img)
    img[img>255] = 255
    out_img = img.astype(np.uint8)
    return out_img


def cal_equalhist(img):                       #直方图均衡化
    # 如果输入图像是彩色图像，则转换为灰度图像
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.CV_8U)
    # 获取图像的高度和宽度
    h, w = img.shape[:2]
    # 计算图像的直方图
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # 计算累积直方图
    cumulative_hist = hist.cumsum()
    # 归一化累积直方图
    normalized_hist = cumulative_hist / (h * w)
    # 映射到0-255范围内
    output_q = (normalized_hist * 255).astype(np.uint8)
    # 创建均衡化后的图像
    equalized_image = np.zeros_like(img)
    # 对每个像素进行映射
    for i in range(h):
        for j in range(w):
            equalized_image[i, j] = output_q[img[i, j]]

    return equalized_image

################图像滤波####################################################
def boxFilterfun(image):       #方波滤波
    image=cv2.boxFilter(image,-1,(1,1),normalize=0)
    return image



def medianBlurfun(image):      #中值滤波
    image=cv2.medianBlur(image,3)
    return image



def bilateralFilterfun(image):   #双边滤波
    image=cv2.bilateralFilter(image,25,100,100)
    return image


def GaussianBlurfun(image):      #高斯滤波
    image=cv2.GaussianBlur(image,(5,5),0,0)
    return image


def blurfun(image):              #均值滤波
    image=cv2.blur(image,(5,5))
    return image

##############轮廓检测####################################################
def morphologyExfun(image):
    kernel = np.ones((3, 3), dtype=np.uint8)
    image_gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    return image_gradient


#############sobel检测#######################################################
def sobel_fun(image):
    # sift = cv2.SIFT_create()
    # kps = sift.detect(image)
    # image_sift = cv2.drawKeypoints(image, kps, None, -1, cv2.DrawMatchesFlags_DEFAULT)
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # 将边缘强度图像转换为无符号8位整型
    sobelx = cv2.convertScaleAbs(sobelx)
    sobely = cv2.convertScaleAbs(sobely)

    # 将水平和垂直边缘强度图像合并为一个图像
    sobel = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    return sobel
#####################图像特征检测###############################


def halisi_fun(image):               #哈里斯角检测
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 设置Harris角检测参数
    blockSize = 2
    ksize = 3
    k = 0.04
    # 计算Harris角响应值
    dst = cv2.cornerHarris(gray, blockSize, ksize, k)

    # 对角点进行标记
    image[dst > 0.01 * dst.max()] = [0, 0, 255]

    return image
    # 将图像转换为灰度图像
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    # windowSize = (5, 5)
    # zeroZone = (-1, -1)
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.001)
    # # 使用cv2.cornerSubPix()函数进行亚像素级角点检测和定位
    # cv2.cornerSubPix(gray, corners, windowSize, zeroZone, criteria)
    #
    # # 绘制检测到的角点
    # for corner in corners:
    #     x, y = corner.ravel()
    #     cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
    #
    # return image


def ORB_fun(image):
    # 创建ORB特征检测器
    orb = cv2.ORB_create()

    # 检测关键点和计算描述符
    keypoints, descriptors = orb.detectAndCompute(image, None)

    # 在图像上绘制关键点
    img_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)

    return img_with_keypoints


# if __name__ == '__main__':
#     # image = cv2.imread("Lena.bmp")
#     # cv2.imshow(' ',image)
#     # newimage=xiufu(image)
#     # cv2.imshow(' ',newimage)
#     cv2.waitKey(0)