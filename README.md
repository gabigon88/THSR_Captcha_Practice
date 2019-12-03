# THSR_Captcha_Practice
練習爬取高鐵訂票頁面的驗證碼，並進行OCR  
***程式碼目前沒有成功辨識過!***  
***程式碼目前沒有成功辨識過!***  
***程式碼目前沒有成功辨識過!***  
很重要先說三遍，基本上只是練習性質，無實用性

## 執行指令
使用的套件非常多，pipenv install 配置環境時可能會等很久  
另外，Tesseract的圖像辨識資料庫要自己安裝到電腦  
詳細看[tesseract ocr 圖像辨識安裝](https://jasonlee.xyz/tesseract-ocr-tu-xiang-bian-shi-an-zhuang/)  
```python
  pipenv install
  pipenv shell
  python hsrIMINT.py
```

## 流程概念
1.用Selenium開高鐵的訂票頁面並螢幕截圖，然後計算驗證碼的位子切割出來  
2.用OpenCV做去雜訊  
3.用matplotlib、scikit-learn簡單的計算驗證圖上拋物線並修正圖片  
4.將圖片丟進tesseract ocr取得驗證碼  

## 後記
第一次實作影像處理，目前自己測試還沒有成功辨識過XD  
圖像辨識還是需要靠機器學習建立的資料庫比較可靠ˊ_>ˋ...  
基本上程式碼是一系列的抄作業寫的，串連起來而已  
[[爬蟲實戰] 如何使用Selenium 抓取驗證碼?](https://www.youtube.com/watch?v=hF-dJj559ug)  
[[爬蟲實戰] 如何破解高鐵驗證碼 (1) - 去除圖片噪音點?](https://www.youtube.com/watch?v=6HGbKdB4kVY)  
[[爬蟲實戰] 如何破解高鐵驗證碼 (2) - 使用迴歸方法去除多餘弧線?](https://www.youtube.com/watch?v=4DHcOPSfC4c)  