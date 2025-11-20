"""
aevatar.ai 登录页面对象
自动生成 - 基于test-case.md P0测试用例
使用同步Playwright API
"""
from pages.base_page import BasePage
from playwright.sync_api import expect
import allure


class AevatarLoginPage(BasePage):
    """aevatar.ai登录页面"""
    
    # 页面URL
    LOGIN_URL = "http://localhost:5173/"
    
    # 页面元素定位器
    PAGE_TITLE = "role=heading[name='aevatar.ai']"
    PAGE_SUBTITLE = "text=The future of on-chain"
    
    # 登录表单
    EMAIL_INPUT = "input[placeholder='Enter your email']"
    PASSWORD_INPUT = "input[type='password']"
    LOGIN_BUTTON = "button:has-text('Log in')"
    
    # 链接和按钮
    REGISTER_LINK = "text=Register"
    FORGOT_PASSWORD_LINK = "text=Forgot Password?"
    GOOGLE_LOGIN_BUTTON = "button:has-text('Google')"
    GITHUB_LOGIN_BUTTON = "button:has-text('Github')"
    
    # 错误提示
    ERROR_MESSAGE = ".error-message, [role='alert']"
    
    @allure.step("导航到登录页面")
    def navigate(self):
        """导航到登录页面"""
        self.page.goto(self.LOGIN_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查登录页面是否已加载"""
        try:
            self.page.wait_for_selector(self.PAGE_TITLE, timeout=5000)
            return True
        except:
            return False
    
    @allure.step("使用邮箱密码登录: {email}")
    def login_with_email(self, email: str, password: str):
        """
        使用邮箱和密码登录
        
        Args:
            email: 用户邮箱
            password: 用户密码
        """
        allure.attach(email, name="Login Email", attachment_type=allure.attachment_type.TEXT)
        
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        
        # 截图
        allure.attach(
            self.page.screenshot(),
            name="before_login_click",
            attachment_type=allure.attachment_type.PNG
        )
        
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(2000)  # 等待跳转或错误提示
    
    @allure.step("获取邮箱输入框的值")
    def get_email_value(self):
        """获取邮箱输入框当前值"""
        return self.page.input_value(self.EMAIL_INPUT)
    
    @allure.step("获取密码输入框的值")
    def get_password_value(self):
        """获取密码输入框当前值"""
        try:
            return self.page.input_value(self.PASSWORD_INPUT)
        except:
            return ""
    
    @allure.step("检查登录按钮是否可用")
    def is_login_button_enabled(self):
        """检查登录按钮是否可点击"""
        try:
            return self.page.is_enabled(self.LOGIN_BUTTON, timeout=3000)
        except:
            return False
    
    @allure.step("获取错误提示信息")
    def get_error_message(self):
        """获取页面错误提示信息"""
        try:
            # 尝试多种错误提示选择器
            selectors = [
                self.ERROR_MESSAGE,
                "text=Invalid",
                "text=Error",
                "[class*='error']",
                "[class*='alert']"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element:
                        text = element.text_content()
                        if text:
                            allure.attach(text, name="Error Message", attachment_type=allure.attachment_type.TEXT)
                            return text
                except:
                    continue
            
            return None
        except:
            return None
    
    @allure.step("获取当前页面URL")
    def get_current_url(self):
        """获取当前页面URL"""
        url = self.page.url
        allure.attach(url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
        return url
    
    @allure.step("检查是否跳转到Dashboard")
    def is_redirected_to_dashboard(self):
        """检查是否跳转到Dashboard页面"""
        self.page.wait_for_timeout(2000)
        current_url = self.get_current_url()
        return "/dashboard" in current_url or "/workflows" in current_url
    
    @allure.step("清空表单")
    def clear_form(self):
        """清空登录表单"""
        self.page.fill(self.EMAIL_INPUT, "")
        self.page.fill(self.PASSWORD_INPUT, "")
    
    @allure.step("点击登录按钮")
    def click_login_button(self):
        """点击登录按钮"""
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(1000)
    
    @allure.step("检查是否停留在登录页")
    def is_on_login_page(self) -> bool:
        """
        检查是否仍在登录页面（用于验证登录失败场景）
        
        Returns:
            bool: True表示在登录页，False表示已跳转
        """
        self.page.wait_for_timeout(2000)
        current_url = self.page.url
        allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
        return current_url == self.LOGIN_URL or "login" in current_url.lower()
