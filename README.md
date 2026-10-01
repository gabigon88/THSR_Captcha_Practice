# THSR_Captcha_Practice
練習爬取高鐵訂票頁面的驗證碼，並進行OCR  

## 執行指令
本專案使用 RapidOCR，不需另外安裝語言資料庫。
首次安裝會下載 Python 套件與 ONNX Runtime，之後辨識可在本機執行。
```python
  pipenv install
  pipenv shell
  python hsrIMINT.py
```

## 流程概念
1.用Selenium開高鐵的訂票頁面，把驗證碼圖片存在captcha_samples資料夾  
2.用OpenCV做去雜訊  
3.用numpy.linalg.lstsq 擬合拋物線並修正圖片  
4.將前處理後的圖片直接交給 RapidOCR 取得文字

## 2026後記
2026年了，現在AI寫code這麼強。  
所幸就把當年這個失敗的舊專案翻出來，全權交由AI優化。  
當年圖片辨識是用Tesseract，使用前要在本地端安裝資料庫。  
跟AI抱怨完這點後，它一鍵改接RapidOCR，我也不需要知道太細節。  
再次體會到AI改變世界的能力，也拿這專案做一次和AI協作的練習。  

## 2019舊後記
第一次實作影像處理，目前自己測試還沒有成功辨識過XD  
圖像辨識還是需要靠機器學習建立的資料庫比較可靠ˊ_>ˋ...  
基本上程式碼是一系列的抄作業寫的，串連起來而已  
[[爬蟲實戰] 如何使用Selenium 抓取驗證碼?](https://www.youtube.com/watch?v=hF-dJj559ug)  
[[爬蟲實戰] 如何破解高鐵驗證碼 (1) - 去除圖片噪音點?](https://www.youtube.com/watch?v=6HGbKdB4kVY)  
[[爬蟲實戰] 如何破解高鐵驗證碼 (2) - 使用迴歸方法去除多餘弧線?](https://www.youtube.com/watch?v=4DHcOPSfC4c)  