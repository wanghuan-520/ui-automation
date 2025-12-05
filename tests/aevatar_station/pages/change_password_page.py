"""
ChangePasswordPage - 修改密码页面对象
路径: /admin/profile/change-password
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ChangePasswordPage(BasePage):
    """修改密码页面对象"""
    
    # 元素定位器 - 优先使用placeholder
    CURRENT_PASSWORD_INPUT = "input[placeholder='Current password']"
    NEW_PASSWORD_INPUT = "input[placeholder='New password']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder='Confirm new password']"
    SAVE_BUTTON = "button:has-text('Save')"
    PAGE_HEADING = "h3:has-text('Change Password'), h2:has-text('Change Password')"
    ERROR_MESSAGE = ".text-danger, .alert-danger, [role='alert']"
    SUCCESS_MESSAGE = ".alert-success, .text-success"
    
    def navigate(self):
        """
        导航到修改密码页面
        ⚡ 修复：不直接访问44320端口，而是先进入/admin/profile，再点击Change Password标签
        """
        logger.info("导航到修改密码页面")
        
        # 方法1：先进入 /admin/profile，然后点击 Change Password 标签
        profile_url = f"{self.base_url}/admin/profile"
        logger.info(f"  步骤1：导航到Profile页面: {profile_url}")
        
        try:
            # 检查页面是否已关闭
            if self.page.is_closed():
                raise Exception("页面已关闭，无法导航")
            
            self.page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)
            self.handle_ssl_warning()
            
            # 等待页面加载
            self.page.wait_for_load_state("networkidle", timeout=15000)
            self.page.wait_for_timeout(1000)
            
            # 步骤2：点击 "Change Password" 标签页
            change_password_tab = "a[role='tab']:has-text('Change Password'), a:has-text('Change Password')"
            logger.info(f"  步骤2：查找并点击Change Password标签")
            
            if self.page.is_visible(change_password_tab, timeout=5000):
                logger.info(f"  ✅ 找到Change Password标签，点击...")
                self.page.click(change_password_tab)
                self.page.wait_for_timeout(2000)
                
                # 验证是否成功切换到Change Password标签
                current_url = self.page.url
                logger.info(f"  ✅ 已切换到Change Password标签，URL: {current_url}")
            else:
                # 标签不存在，尝试直接访问URL
                logger.warning(f"  ⚠️ 未找到Change Password标签，尝试直接访问...")
                target_url = f"{self.auth_url}/admin/profile/change-password"
                self.page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
                self.handle_ssl_warning()
                self.page.wait_for_load_state("networkidle", timeout=20000)
                self.page.wait_for_timeout(3000)
            
            # 🔍 诊断：检查页面是否有实际内容
            page_html = self.page.content()
            logger.info(f"  页面HTML长度: {len(page_html)} 字符")
            if len(page_html) < 100:
                logger.error(f"  ❌ 页面内容过少，可能未渲染！HTML: {page_html}")
            else:
                logger.info(f"  ✅ 页面已有实际内容")
            
            logger.info(f"✅ 页面已加载: {self.page.url}")
        except Exception as e:
            logger.error(f"❌ 导航失败: {url}")
            logger.error(f"   错误: {e}")
            
            # 诊断信息
            try:
                if not self.page.is_closed():
                    logger.error(f"   当前URL: {self.page.url}")
            except:
                pass
            
            raise
    
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

