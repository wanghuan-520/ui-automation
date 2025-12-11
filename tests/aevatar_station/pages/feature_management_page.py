"""
Feature Management 页面对象
定义Feature Management页面的元素和操作方法
"""
from playwright.sync_api import Page
import logging
from tests.aevatar_station.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class FeatureManagementPage(BasePage):
    """Feature Management页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin/settings/feature-management"
        
        # Tab导航
        self.FEATURE_MANAGEMENT_TAB = "button[role='tab']:has-text('Feature'), [role='tab']:has-text('Feature')"
        self.EMAILING_TAB = "button[role='tab']:has-text('Emailing'), [role='tab']:has-text('Emailing')"
        
        # 页面主要元素 - 基于实际UI
        self.PAGE_DESCRIPTION = "text=You can manage the host side features, p:has-text('host side features')"
        self.MANAGE_BUTTON = "button:has-text('Manage Host Features')"
        
        # Features对话框元素 - 基于实际UI
        self.DIALOG = "[role='dialog']"
        self.DIALOG_TITLE = "[role='dialog'] h2:has-text('Features')"
        self.DIALOG_BACKDROP = "[role='dialog'] + div, .modal-backdrop"
        
        # 对话框内容 - 基于实际UI
        self.EMPTY_STATE_MESSAGE = "text=There isn't any available feature"
        self.FEATURE_LIST = "[role='dialog'] ul, [role='dialog'] .feature-list"
        
        # 对话框按钮 - 基于实际UI
        self.SAVE_BUTTON = "[role='dialog'] button:has-text('Save')"
        self.CANCEL_BUTTON = "[role='dialog'] button:has-text('Cancel')"
        self.CLOSE_BUTTON = "[role='dialog'] button:has-text('Close')"
        
        # 功能开关（如果有Features）
        self.FEATURE_TOGGLE = "input[type='checkbox'][role='switch']"
        self.FEATURE_INPUT = "input[type='number']"
    
    def navigate(self):
        """导航到Feature Management页面"""
        logger.info("导航到Feature Management页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
        # 等待Tab加载
        try:
            self.page.wait_for_selector(self.FEATURE_MANAGEMENT_TAB, timeout=10000)
        except Exception as e:
            logger.warning(f"等待Feature Management Tab失败: {e}")
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            self.page.wait_for_selector(self.MANAGE_BUTTON, timeout=10000)
            logger.info("Feature Management页面加载完成")
            return True
        except Exception as e:
            logger.error(f"Feature Management页面加载失败: {e}")
            return False
    
    def click_feature_management_tab(self):
        """点击Feature Management Tab"""
        logger.info("点击Feature Management Tab")
        self.page.locator(self.FEATURE_MANAGEMENT_TAB).first.click()
        self.page.wait_for_timeout(1000)
    
    def click_emailing_tab(self):
        """点击Emailing Tab"""
        logger.info("点击Emailing Tab")
        self.page.locator(self.EMAILING_TAB).first.click()
        self.page.wait_for_timeout(1000)
    
    def is_manage_button_visible(self) -> bool:
        """检查Manage Host Features按钮是否可见"""
        try:
            is_visible = self.page.locator(self.MANAGE_BUTTON).is_visible(timeout=5000)
            logger.info(f"Manage Host Features按钮可见性: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"检查按钮可见性失败: {e}")
            return False
    
    def click_manage_host_features(self):
        """点击Manage Host Features按钮"""
        logger.info("点击Manage Host Features按钮")
        try:
            self.page.locator(self.MANAGE_BUTTON).click()
            # 等待对话框出现
            self.page.wait_for_timeout(1000)
            logger.info("Manage Host Features按钮已点击")
        except Exception as e:
            logger.error(f"点击按钮失败: {e}")
            raise
    
    def is_dialog_open(self) -> bool:
        """检查Features对话框是否打开"""
        try:
            # 尝试多种选择器
            selectors = [
                "[role='dialog']",
                ".modal.show",
                ".dialog[open]",
                "div[class*='modal'][style*='display']"
            ]
            
            for selector in selectors:
                try:
                    if self.page.locator(selector).is_visible(timeout=2000):
                        logger.info(f"对话框已打开（使用选择器: {selector}）")
                        return True
                except:
                    continue
            
            logger.warning("未找到打开的对话框")
            return False
        except Exception as e:
            logger.error(f"检查对话框状态失败: {e}")
            return False
    
    def is_dialog_title_visible(self) -> bool:
        """检查对话框标题是否显示"""
        try:
            is_visible = self.page.locator(self.DIALOG_TITLE).is_visible(timeout=3000)
            if is_visible:
                title = self.page.locator(self.DIALOG_TITLE).text_content()
                logger.info(f"对话框标题: {title}")
            return is_visible
        except Exception as e:
            logger.error(f"检查对话框标题失败: {e}")
            return False
    
    def is_empty_state_message_visible(self) -> bool:
        """检查空状态提示是否显示"""
        try:
            is_visible = self.page.locator(self.EMPTY_STATE_MESSAGE).is_visible(timeout=3000)
            if is_visible:
                message = self.page.locator(self.EMPTY_STATE_MESSAGE).text_content()
                logger.info(f"空状态提示: {message}")
            return is_visible
        except Exception as e:
            logger.info("未找到空状态提示（可能有Features定义）")
            return False
    
    def click_save(self):
        """点击Save按钮"""
        logger.info("点击Save按钮")
        try:
            self.page.locator(self.SAVE_BUTTON).first.click()
            self.page.wait_for_timeout(1000)
            logger.info("Save按钮已点击")
        except Exception as e:
            logger.error(f"点击Save按钮失败: {e}")
            raise
    
    def click_cancel(self):
        """点击Cancel按钮"""
        logger.info("点击Cancel按钮")
        try:
            self.page.locator(self.CANCEL_BUTTON).first.click()
            self.page.wait_for_timeout(1000)
            logger.info("Cancel按钮已点击")
        except Exception as e:
            logger.error(f"点击Cancel按钮失败: {e}")
            raise
    
    def click_close_button(self):
        """点击对话框关闭按钮"""
        logger.info("点击关闭按钮")
        try:
            # 优先使用Close文本按钮
            if self.page.locator(self.CLOSE_BUTTON).is_visible(timeout=2000):
                self.page.locator(self.CLOSE_BUTTON).first.click()
                logger.info("关闭按钮已点击")
                self.page.wait_for_timeout(1000)
                return
            
            # 备选：尝试其他关闭按钮选择器
            close_selectors = [
                "[role='dialog'] button[aria-label*='close' i]",
                "[role='dialog'] .close",
                "[role='dialog'] button.btn-close"
            ]
            
            for selector in close_selectors:
                try:
                    if self.page.locator(selector).is_visible(timeout=1000):
                        self.page.locator(selector).first.click()
                        logger.info(f"关闭按钮已点击（使用选择器: {selector}）")
                        self.page.wait_for_timeout(1000)
                        return
                except:
                    continue
            
            logger.warning("未找到关闭按钮")
        except Exception as e:
            logger.error(f"点击关闭按钮失败: {e}")
    
    def press_escape(self):
        """按ESC键关闭对话框"""
        logger.info("按ESC键")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(1000)
    
    def click_dialog_backdrop(self):
        """点击对话框外部遮罩层"""
        logger.info("点击对话框外部")
        try:
            backdrop = self.page.locator(self.DIALOG_BACKDROP).first
            if backdrop.is_visible(timeout=2000):
                backdrop.click(position={"x": 10, "y": 10})
                self.page.wait_for_timeout(1000)
            else:
                logger.warning("未找到遮罩层")
        except Exception as e:
            logger.error(f"点击遮罩层失败: {e}")
    
    def get_feature_count(self) -> int:
        """获取功能列表数量"""
        try:
            count = self.page.locator(self.FEATURE_TOGGLE).count()
            logger.info(f"功能数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取功能数量失败: {e}")
            return 0
    
    def toggle_feature(self, index: int = 0):
        """
        切换功能开关
        
        Args:
            index: 功能索引（从0开始）
        """
        logger.info(f"切换功能开关 #{index}")
        try:
            toggle = self.page.locator(self.FEATURE_TOGGLE).nth(index)
            toggle.click()
            self.page.wait_for_timeout(500)
            logger.info(f"功能开关 #{index} 已切换")
        except Exception as e:
            logger.error(f"切换功能开关失败: {e}")
            raise
    
    def is_feature_enabled(self, index: int = 0) -> bool:
        """
        检查功能是否启用
        
        Args:
            index: 功能索引（从0开始）
        """
        try:
            toggle = self.page.locator(self.FEATURE_TOGGLE).nth(index)
            is_checked = toggle.is_checked()
            logger.info(f"功能 #{index} 启用状态: {is_checked}")
            return is_checked
        except Exception as e:
            logger.error(f"检查功能状态失败: {e}")
            return False
    
    def set_feature_value(self, value: int, index: int = 0):
        """
        设置功能数值（配额）
        
        Args:
            value: 数值
            index: 功能索引（从0开始）
        """
        logger.info(f"设置功能 #{index} 数值: {value}")
        try:
            input_field = self.page.locator(self.FEATURE_INPUT).nth(index)
            input_field.fill(str(value))
            logger.info(f"功能 #{index} 数值已设置")
        except Exception as e:
            logger.error(f"设置功能数值失败: {e}")
            raise
    
    def get_feature_value(self, index: int = 0) -> int:
        """
        获取功能数值
        
        Args:
            index: 功能索引（从0开始）
        """
        try:
            input_field = self.page.locator(self.FEATURE_INPUT).nth(index)
            value = input_field.input_value()
            logger.info(f"功能 #{index} 数值: {value}")
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"获取功能数值失败: {e}")
            return 0
    
    def is_page_description_visible(self) -> bool:
        """检查页面描述是否可见"""
        try:
            is_visible = self.page.locator(self.PAGE_DESCRIPTION).is_visible(timeout=3000)
            if is_visible:
                desc = self.page.locator(self.PAGE_DESCRIPTION).text_content()
                logger.info(f"页面描述: {desc}")
            return is_visible
        except Exception as e:
            logger.info("未找到页面描述")
            return False
    
    def wait_for_dialog_close(self, timeout: int = 5000):
        """等待对话框关闭"""
        logger.info("等待对话框关闭")
        try:
            self.page.wait_for_selector(
                "[role='dialog']",
                state="hidden",
                timeout=timeout
            )
            logger.info("对话框已关闭")
        except Exception as e:
            logger.warning(f"等待对话框关闭超时: {e}")
    
    def take_screenshot(self, filename: str):
        """截图并保存"""
        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图保存到: {screenshot_path}")
        return screenshot_path

