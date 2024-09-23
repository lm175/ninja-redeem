from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from ddddocr import DdddOcr

from io import BytesIO
import time, base64, json
import requests


class RedeemCode():
    def __init__(self, dhm: str) -> None:
        self.dhm=dhm
        self.driver=self.creat_driver()
    
    @classmethod
    def creat_driver(cls) -> Edge:
        options = Options()
        options.add_argument('--headless')
        driver = Edge(options=options)
        driver.implicitly_wait(2)
        driver.get("https://statistics.pandadastudio.com/")
        return driver


    def dhm_checker(self) -> bool:
        tip_text, _ = self.redeem_for_user("634431781")
        if tip_text == "领取失败，礼包不存在" or tip_text == "领取失败，礼包未到生效时间或已过期":
            return False
        return True


    def redeem_for_user(self, uid: str) -> str:
        """执行一次兑换，返回提示信息"""
        driver = self.driver

        uid_input = driver.find_element(By.ID, "uid")
        uid_input.clear()
        uid_input.send_keys(uid)
        time.sleep(0.2)
        dhm_input = driver.find_element(By.ID, "dhm")
        dhm_input.clear()
        dhm_input.send_keys(self.dhm)

        submit = driver.find_element(By.CLASS_NAME, "submit")
        submit.click()

        self._pass_captcha(50)
        while True:
            try:
                tip_msg = driver.find_element(By.CLASS_NAME, "tip-msg").text
                confirm = driver.find_element(By.CLASS_NAME, "confirm")
                confirm.click()
                return tip_msg
            except:
                self._pass_captcha(60)


    def _pass_captcha(self, fix: int):
        driver = self.driver
        time.sleep(1)
        try:
            # 碎片
            sp_element = driver.find_element(By.CLASS_NAME, "dx-captcha-body-slider")
            image_url = sp_element.get_attribute("src")
            if not image_url:
                return
            res = requests.get(image_url)
            sp_bytes = res.content

            # 背景
            bg_element = driver.find_element(By.CLASS_NAME, "dx-captcha-body")
            bg_BytesIo = BytesIO(base64.b64decode(bg_element.screenshot_as_base64))
            bg_image = Image.open(bg_BytesIo)
            bg_image = bg_image.crop((60, 0, 300, 150))
            bg_BytesIo = BytesIO()
            bg_image.save(bg_BytesIo, "PNG")

            # 识图
            det = DdddOcr(ocr=False, det=False, show_ad=False)
            position = det.slide_match(sp_bytes, bg_BytesIo.getvalue(), simple_target=True)
            value = position['target'][0] + fix

            # 滑块
            slider = driver.find_element(By.CLASS_NAME, "dx-captcha-bar-slider")
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()
            action.move_by_offset(value, 0)
            action.release().perform()
        except Exception as e:
            print(e)
            return
    

    def close(self):
        self.driver.quit()
