import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestGodGPTWisdomDrop(unittest.TestCase):
    """
    测试GodGPT应用的Today's Wisdom Drop功能
    """
    
    def setUp(self):
        """
        测试前的设置，包括启动Appium会话
        """
        # Appium服务器配置
        desired_caps = {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': 'fd8331f8',  # 设备ID
            'appPackage': 'com.gpt.god',
            'appActivity': 'com.gpt.god.MainActivity',  # 主活动名称可能需要确认
            'noReset': True  # 保持应用数据不重置
        }
        
        # 连接到Appium服务器
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, 10)
        
    def test_wisdom_drop_flow(self):
        """
        测试Today's Wisdom Drop功能的完整流程
        """
        try:
            # 等待主页面加载
            time.sleep(3)  # 给应用一些启动时间
            
            # 查找并点击Today's Wisdom Drop卡片
            wisdom_card = self.wait.until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH, 
                    "//android.widget.TextView[@text='Today's Wisdom Drop']"
                ))
            )
            wisdom_card.click()
            
            # 验证进入Wisdom页面
            wisdom_title = self.wait.until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH,
                    "//android.widget.TextView[contains(@text, 'What message do I need to hear today')]"
                ))
            )
            self.assertTrue(wisdom_title.is_displayed())
            
            # 验证页面关键元素存在
            whisper_section = self.wait.until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH,
                    "//android.widget.TextView[contains(@text, 'Whisper of the Day')]"
                ))
            )
            self.assertTrue(whisper_section.is_displayed())
            
            # 验证呼吸练习部分存在
            breathe_section = self.wait.until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH,
                    "//android.widget.TextView[contains(@text, 'Breathe:')]"
                ))
            )
            self.assertTrue(breathe_section.is_displayed())
            
            # 验证底部输入框存在
            ask_input = self.wait.until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH,
                    "//android.widget.EditText[@text='Ask anything']"
                ))
            )
            self.assertTrue(ask_input.is_displayed())
            
        except Exception as e:
            self.driver.save_screenshot('error_screenshot.png')
            raise e
            
    def tearDown(self):
        """
        测试后清理
        """
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main() 