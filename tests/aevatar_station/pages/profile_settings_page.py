"""
ProfileSettingsPage - 个人设置页面对象
路径: /admin/profile
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ProfileSettingsPage(BasePage):
    """个人设置页面对象"""
    
    # 元素定位器（简化并使用更精确的选择器）
    PERSONAL_SETTINGS_TAB = "a[role='tab']:has-text('Personal Settings')"
    CHANGE_PASSWORD_TAB = "a[role='tab']:has-text('Change Password')"
    USERNAME_INPUT = "input[name='userName']"
    NAME_INPUT = "input[name='name']"
    SURNAME_INPUT = "input[name='surname']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_INPUT = "input[name='phoneNumber']"
    SAVE_BUTTON = "button:has-text('Save')"
    SUCCESS_MESSAGE = ".alert-success, .text-success, [role='alert']"
    
    def navigate(self):
        """导航到个人设置页面"""
        logger.info("导航到个人设置页面")
        self.navigate_to("/admin/profile")
        # ⚡ 优化：先等待页面基本加载
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)  # ⚡ 优化：缩短等待时间
        
        # 显式等待关键元素加载
        logger.info("等待页面关键元素加载...")
        try:
            # ⚡ 优化：尝试多个选择器，增加容错性
            selectors = [self.NAME_INPUT, self.SAVE_BUTTON, self.PERSONAL_SETTINGS_TAB]
            loaded = False
            for selector in selectors:
                try:
                    self.page.wait_for_selector(selector, state="visible", timeout=10000)
                    loaded = True
                    break
                except:
                    continue
            if not loaded:
                raise Exception("无法找到任何关键元素")
            logger.info("页面加载完成")
        except Exception as e:
            logger.error(f"页面加载超时: {e}")
            logger.error(f"当前URL: {self.page.url}")
            logger.error(f"页面标题: {self.page.title()}")
            # ⚡ 优化：如果新注册账号无权限，尝试等待更长时间或检查权限
            if "/admin/profile" not in self.page.url:
                logger.warning("可能没有权限访问profile页面，尝试等待...")
                self.page.wait_for_timeout(2000)
                if "/admin/profile" not in self.page.url:
                    raise Exception(f"无法访问profile页面，当前URL: {self.page.url}")
            raise
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        try:
            # 尝试等待 Personal Settings 标签页出现，超时 5 秒
            self.page.wait_for_selector(self.PERSONAL_SETTINGS_TAB, state="visible", timeout=5000)
            return True
        except:
            # 如果主元素未找到，检查是否至少有 Save 按钮
            return self.is_visible(self.SAVE_BUTTON)
    
    def update_profile(self, name=None, surname=None, phone=None):
        """更新个人信息"""
        logger.info("更新个人信息")
        
        if name:
            self.fill_input(self.NAME_INPUT, name)
        
        if surname:
            self.fill_input(self.SURNAME_INPUT, surname)
        
        if phone:
            self.fill_input(self.PHONE_INPUT, phone)
        
        self.click_element(self.SAVE_BUTTON)
        
        # 等待网络请求完成
        logger.info("等待保存操作完成...")
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # 尝试等待成功消息，确保后端处理完成
        try:
            self.page.wait_for_selector(self.SUCCESS_MESSAGE, state="visible", timeout=5000)
            logger.info("成功消息已出现")
        except Exception:
            logger.warning("未检测到成功消息，但这可能不影响功能")
            
        # 额外等待确保后端数据落盘
        self.page.wait_for_timeout(5000)
        logger.info("保存操作已完成")
    
    def get_name_value(self):
        """获取Name字段的值"""
        return self.page.input_value(self.NAME_INPUT)
    
    def get_surname_value(self):
        """获取Surname字段的值"""
        return self.page.input_value(self.SURNAME_INPUT)
    
    def get_phone_value(self):
        """获取Phone字段的值"""
        return self.page.input_value(self.PHONE_INPUT)
    
    def get_email_value(self):
        """获取Email字段的值"""
        return self.page.input_value(self.EMAIL_INPUT)
    
    def get_username_value(self):
        """获取UserName字段的值"""
        return self.page.input_value(self.USERNAME_INPUT)
    
    def is_field_readonly(self, locator):
        """检查字段是否只读"""
        element = self.page.locator(locator)
        return element.get_attribute("readonly") is not None or element.get_attribute("disabled") is not None
    
    def is_field_required(self, locator):
        """检查字段是否有required属性"""
        element = self.page.locator(locator)
        return element.get_attribute("required") is not None
    
    def get_field_validation_message(self, locator):
        """获取字段的HTML5验证消息"""
        return self.page.evaluate(f"""
            document.querySelector("{locator}").validationMessage
        """)
    
    def is_field_valid(self, locator):
        """检查字段是否通过HTML5验证"""
        return self.page.evaluate(f"""
            document.querySelector("{locator}").checkValidity()
        """)
    
    def get_field_max_length(self, locator):
        """获取字段的最大长度限制"""
        element = self.page.locator(locator)
        max_length = element.get_attribute("maxlength")
        return int(max_length) if max_length else None
    
    def is_success_message_visible(self):
        """检查成功消息是否可见"""
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=3000)
    
    def click_change_password_tab(self):
        """点击Change Password标签页"""
        logger.info("切换到Change Password标签页")
        self.click_element(self.CHANGE_PASSWORD_TAB)
        self.page.wait_for_timeout(1000)

