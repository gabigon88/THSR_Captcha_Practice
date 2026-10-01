from datetime import datetime
from pathlib import Path

import hsrCAPTCHA
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = PROJECT_DIR / "captcha_samples"
WAIT_SECONDS = 10

driver = webdriver.Chrome()
try:
    driver.get('http://irs.thsrc.com.tw/IMINT/')

    try:
        driver.find_element(By.XPATH, "//*[@id='cookieAccpetBtn']").click()
    except NoSuchElementException:
        pass

    wait = WebDriverWait(driver, WAIT_SECONDS)
    element = wait.until(
        EC.visibility_of_element_located((By.ID, 'BookingS1Form_homeCaptcha_passCode'))
    )
    wait.until(lambda _: element.size["width"] > 0 and element.size["height"] > 0)
    wait.until(
        lambda browser: browser.execute_script(
            "return arguments[0].complete === undefined || "
            "(arguments[0].complete && arguments[0].naturalWidth > 0);",
            element,
        )
    )

    SAMPLES_DIR.mkdir(exist_ok=True)
    sample_path = SAMPLES_DIR / f"captcha_{datetime.now():%Y%m%d_%H%M%S_%f}.png"
    element.screenshot(str(sample_path))

    print(f"驗證碼樣本已儲存：{sample_path.relative_to(PROJECT_DIR)}")
    print(hsrCAPTCHA.captchaOCR(str(sample_path)))
finally:
    driver.quit()
