import os
import hsrCAPTCHA
from selenium import webdriver
from PIL import Image

driver = webdriver.Chrome()
driver.get('http://irs.thsrc.com.tw/IMINT/')

try:
    xPath = "//*[@id='btn-confirm']"
    driver.find_element_by_xpath(xPath).click()
except:
    pass

driver.save_screenshot('temp.png')

element = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')

left = element.location['x']
right = element.location['x'] + element.size['width']
top = element.location['y']
bottom = element.location['y'] + element.size['height']

img = Image.open('temp.png')
img = img.crop((left, top, right, bottom))
img.save('captcha.png', 'png')
os.remove('temp.png')
driver.close()

print(hsrCAPTCHA.captchaOCR('captcha.png'))