import cv2
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
from PIL import Image
from sklearn.preprocessing import binarize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def preprocess(filePath):
    img = cv2.imread(filePath)
    dst = cv2.fastNlMeansDenoisingColored(img, None, 30, 30, 7, 21) # 去雜點，30為去雜點的力度

    ''' Debug，預覽雜點效果 
    plt.subplot(121) # 畫到gird為1*2的子畫布，1號位子上
    plt.imshow(img)
    plt.subplot(122) # 畫到gird為1*2的子畫布，2號位子上
    plt.imshow(dst)
    plt.show() # 比較去雜點前後的圖片
    '''

    # 將圖片顏色二元化(黑白)，127為門檻值，亮度高於127的設為255，低於127的設為0
    ret, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY_INV) 

    ''' Debug，預覽黑白化效果
    plt.imshow(thresh)
    plt.show() # 預覽黑白化的圖片
    '''

    imgArr = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    yPixelLen, xPixelLen = imgArr.shape # 取得圖片的長*寬
    imgArr[:,5:-5] = 0 # 只取X軸頭尾各5單位長內的像素點，其他都設為0
    imageData = np.where(imgArr == 255) # 找出所有白色像素的x, y座標，imageData是二維陣列

    ''' Debug，預覽拋物線的起點、終點
    plt.scatter(imageData[1], yPixelLen - imageData[0], s = 100, c = 'red', label = 'Cluster 1')
    plt.ylim(ymin=0, ymax=yPixelLen) # 設定畫布的Y軸高度
    plt.show() # 預覽拋物線的起點、終點
    '''

    X = np.array([imageData[1]])
    Y = yPixelLen - imageData[0]
    poly_reg= PolynomialFeatures(degree = 2) # 計算拋物線，指數設為2
    X_ = poly_reg.fit_transform(X.T)
    regr = LinearRegression()
    regr.fit(X_, Y) # 自動補齊拋物線

    X2 = np.array([[i for i in range(0, xPixelLen)]])
    X2_ = poly_reg.fit_transform(X2.T)

    ''' Debug，預覽計算出的拋物線
    plt.scatter(X, Y, color="black")
    plt.ylim(ymin=0, ymax=yPixelLen) # 設定畫布的Y軸高度
    plt.plot(X2.T, regr.predict(X2_), color= "blue", linewidth = 3)
    plt.show() # 預覽計算的拋物線
    '''

    ''' 印出拋物線資訊
    print('Coefficient:{}'.format(regr.coef_))
    print('Intercept:{}'.format(regr.intercept_))
    '''

    # 藉由算出的拋物線，修正驗證碼圖片
    newImg =  cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    for ele in np.column_stack([regr.predict(X2_).round(0), X2[0],] ):
        pos = yPixelLen - int(ele[0])
        # yUp, yDown = 0, 0
        # while newImg[pos, int(ele[1])] == newImg[pos+yUp, int(ele[1])] and pos+yUp < yPixelLen-1:
        #     yUp += 1
        # while newImg[pos, int(ele[1])] == newImg[pos-yDown, int(ele[1])] and pos-yDown > 0:
        #     yDown += 1
        # newImg[pos-yDown:pos+yUp, int(ele[1])] = 255 - newImg[pos-yDown:pos+yUp, int(ele[1])]
        newImg[pos-3:pos+3, int(ele[1])] = 255 - newImg[pos-3:pos+3, int(ele[1])]

    ''' Debug，比對修正圖片前後
    plt.subplot(121)
    plt.imshow(thresh)
    plt.subplot(122)
    plt.imshow(newImg)
    plt.show() # 比對效果
    '''

    # 儲存檔案
    plt.figure(figsize = (xPixelLen, yPixelLen))
    plt.imshow(newImg)
    plt.savefig("captcha_temp.jpg")
    plt.cla()

def captchaOCR(filePath):
    preprocess(filePath)
    img = Image.open('captcha_temp.jpg')
    text = pytesseract.image_to_string(img)
    if text == "":
        print('無法辨識')
        return None
    else:
        return text