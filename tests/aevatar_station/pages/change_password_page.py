"""
ChangePasswordPage - 修改密码页面对象
路径: /admin/profile/change-password
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ChangePasswordPage(BasePage):
    """修改密码页面对象"""
    
    # 元素定位器 - 使用placeholder定位（基于实际页面结构）
    CURRENT_PASSWORD_INPUT = "input[placeholder='Current password']"
    NEW_PASSWORD_INPUT = "input[placeholder='New password']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder='Confirm new password']"
    SAVE_BUTTON = "button:has-text('Save')"
    PAGE_HEADING = "h3:has-text('Change Password'), h2:has-text('Change Password')"
    ERROR_MESSAGE = ".text-danger, .alert-danger, [role='alert']"
    SUCCESS_MESSAGE = ".alert-success, .text-success"
    
    def navigate(self):
        """导航到修改密码页面"""
        logger.info("导航到修改密码页面")
        self.navigate_to("/admin/profile/change-password")
        # 等待页面加载
        self.page.wait_for_timeout(2000)
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.PAGE_HEADING) or self.is_visible(self.CURRENT_PASSWORD_INPUT)
    
    def change_password(self, current_password, new_password, confirm_password=None):
        """修改密码"""
        logger.info("修改密码")
        
        # 如果没有提供确认密码，则使用新密码
        if confirm_password is None:
            confirm_password = new_password
        
        # 填写当前密码
        self.fill_input(self.CURRENT_PASSWORD_INPUT, current_password)
        
        # 填写新密码
        self.fill_input(self.NEW_PASSWORD_INPUT, new_password)
        
        # 填写确认密码
        self.fill_input(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        
        # 点击保存按钮
        self.click_element(self.SAVE_BUTTON)
        
        # 等待处理完成
        self.page.wait_for_timeout(2000)
    
    def is_error_message_visible(self):
        """检查错误消息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def get_error_message(self):
        """获取错误消息文本"""
        if self.is_error_message_visible():
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_success_message_visible(self):
        """检查成功消息是否可见"""
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=3000)

