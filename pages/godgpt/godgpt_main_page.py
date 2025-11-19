from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger
from typing import Optional, List

logger = get_logger(__name__)

class GodGPTMainPage(BasePage):
    """GodGPT 主界面 Page Object"""
    
    # 顶部导航元素
    LOGO = "text=GodGPT"
    ANNUAL_BUTTON = "text=Annual"
    USER_AVATAR = "img[alt*='avatar'], [aria-label*='user'], button:has-text('user')"
    
    # 侧边栏元素
    MENU_TOGGLE = "button:has(img[alt*='menu']), [aria-label*='menu']"
    NEW_CHAT_BUTTON = "button:has(img[alt*='edit']), button:has-text('New'), [aria-label*='new chat']"
    GET_APP_BUTTON_SIDEBAR = "text=Get App"
    TODAY_SECTION = "text=Today"
    THIRTY_DAYS_SECTION = "text=30 Days Ago"
    
    # 主区域元素
    NO_READINGS_TEXT = "text=🔮 No Readings Yet"
    FUTURE_AWAITS_TEXT = "text=/Your future awaits/i"
    MAIN_INPUT = "textarea, input[placeholder*='Ask' i]"
    ATTACH_BUTTON = "button:has(img[alt*='attach']), button:has-text('+'), [aria-label*='attach']"
    VOICE_BUTTON = "button:has(img[alt*='mic']), button:has(img[alt*='voice']), [aria-label*='voice']"
    SEND_BUTTON = "button:has(img[alt*='send']), button[type='submit'], [aria-label*='send']"
    
    # 快捷功能卡片
    SOUL_LINK_CARD = "text=Soul Link"
    UNLOCK_PATH_CARD = "text=Unlock Your Path"
    FEELING_LOST_CARD = "text=Feeling Lost?"
    INNER_STILLNESS_CARD = "text=Find Inner Stillness"
    
    # 下载推广区域
    DOWNLOAD_SECTION = "text=download_now"
    DOWNLOAD_CLOSE_BUTTON = "button[aria-label*='close'], button:has-text('×')"
    APP_STORE_LINK = "img[alt*='App Store']"
    GOOGLE_PLAY_LINK = "img[alt*='Google Play']"
    QR_CODE = "img[alt*='QR'], img[alt*='qr']"
    
    # 页面加载指示器
    page_loaded_indicator = "textarea, input[placeholder*='Ask' i]"
    
    def __init__(self, page: Page):
        """
        初始化主界面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = "https://godgpt-ui-testnet.aelf.dev/"
    
    def navigate(self) -> None:
        """导航到主界面"""
        logger.info(f"导航到GodGPT主界面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查页面是否加载完成（已登录状态）
        
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 检查主输入框是否可见
            main_input_visible = self.is_element_visible(self.MAIN_INPUT, timeout=10000)
            
            # 检查 Annual 按钮是否存在（登录后才显示）
            annual_button_visible = self.is_element_visible(self.ANNUAL_BUTTON, timeout=5000)
            
            logger.info(f"主界面加载状态: 输入框={main_input_visible}, Annual按钮={annual_button_visible}")
            return main_input_visible and annual_button_visible
        except Exception as e:
            logger.error(f"检查页面加载失败: {str(e)}")
            return False
    
    def is_logged_in(self) -> bool:
        """
        检查是否已登录
        
        Returns:
            bool: 是否已登录
        """
        try:
            # 检查登录后才显示的元素
            annual_visible = self.is_element_visible(self.ANNUAL_BUTTON, timeout=3000)
            user_avatar_visible = self.is_element_visible(self.USER_AVATAR, timeout=3000)
            
            is_logged = annual_visible or user_avatar_visible
            logger.info(f"登录状态检查: {is_logged}")
            return is_logged
        except Exception as e:
            logger.error(f"检查登录状态失败: {str(e)}")
            return False
    
    def send_message(self, message: str, press_enter: bool = True) -> bool:
        """
        发送消息
        
        Args:
            message: 要发送的消息
            press_enter: 是否按Enter发送（默认True）
            
        Returns:
            bool: 是否发送成功
        """
        try:
            logger.info(f"输入消息: {message[:50]}...")  # 只记录前50个字符
            
            # 定位输入框
            input_locator = self.page.locator(self.MAIN_INPUT).first
            input_locator.click()
            input_locator.fill(message)
            
            # 发送消息
            if press_enter:
                input_locator.press("Enter")
                logger.info("通过Enter键发送消息")
            else:
                # 点击发送按钮
                if self.is_element_visible(self.SEND_BUTTON, timeout=2000):
                    self.page.click(self.SEND_BUTTON)
                    logger.info("通过发送按钮发送消息")
                else:
                    logger.warning("未找到发送按钮，尝试按Enter")
                    input_locator.press("Enter")
            
            # 等待消息发送
            self.page.wait_for_timeout(1000)
            logger.info("消息发送成功")
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            return False
    
    def click_new_chat(self) -> bool:
        """
        点击新建对话按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击新建对话按钮")
            self.page.click(self.NEW_CHAT_BUTTON)
            self.page.wait_for_timeout(1000)
            logger.info("新建对话按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击新建对话按钮失败: {str(e)}")
            return False
    
    def click_soul_link_card(self) -> bool:
        """
        点击 Soul Link 卡片
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Soul Link 卡片")
            self.page.click(self.SOUL_LINK_CARD)
            self.page.wait_for_timeout(1000)
            logger.info("Soul Link 卡片点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Soul Link 卡片失败: {str(e)}")
            return False
    
    def click_unlock_path_card(self) -> bool:
        """
        点击 Unlock Your Path 卡片
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Unlock Your Path 卡片")
            self.page.click(self.UNLOCK_PATH_CARD)
            self.page.wait_for_timeout(1000)
            logger.info("Unlock Your Path 卡片点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Unlock Your Path 卡片失败: {str(e)}")
            return False
    
    def click_feeling_lost_card(self) -> bool:
        """
        点击 Feeling Lost 卡片
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Feeling Lost 卡片")
            self.page.click(self.FEELING_LOST_CARD)
            self.page.wait_for_timeout(1000)
            logger.info("Feeling Lost 卡片点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Feeling Lost 卡片失败: {str(e)}")
            return False
    
    def click_inner_stillness_card(self) -> bool:
        """
        点击 Find Inner Stillness 卡片
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Find Inner Stillness 卡片")
            self.page.click(self.INNER_STILLNESS_CARD)
            self.page.wait_for_timeout(1000)
            logger.info("Find Inner Stillness 卡片点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Find Inner Stillness 卡片失败: {str(e)}")
            return False
    
    def click_annual_button(self) -> bool:
        """
        点击 Annual 按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Annual 按钮")
            self.page.click(self.ANNUAL_BUTTON)
            self.page.wait_for_timeout(1000)
            logger.info("Annual 按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Annual 按钮失败: {str(e)}")
            return False
    
    def click_user_avatar(self) -> bool:
        """
        点击用户头像
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击用户头像")
            self.page.click(self.USER_AVATAR)
            self.page.wait_for_timeout(1000)
            logger.info("用户头像点击成功")
            return True
        except Exception as e:
            logger.error(f"点击用户头像失败: {str(e)}")
            return False
    
    def click_voice_button(self) -> bool:
        """
        点击语音按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击语音按钮")
            self.page.click(self.VOICE_BUTTON)
            self.page.wait_for_timeout(500)
            logger.info("语音按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击语音按钮失败: {str(e)}")
            return False
    
    def click_attach_button(self) -> bool:
        """
        点击附件按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击附件按钮")
            self.page.click(self.ATTACH_BUTTON)
            self.page.wait_for_timeout(500)
            logger.info("附件按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击附件按钮失败: {str(e)}")
            return False
    
    def get_history_chat_titles(self) -> List[str]:
        """
        获取历史对话标题列表
        
        Returns:
            List[str]: 对话标题列表
        """
        try:
            # 查找历史对话项（可能需要根据实际DOM结构调整）
            chat_items = self.page.locator("[role='listitem'], .chat-item, .history-item").all()
            
            titles = []
            for item in chat_items:
                try:
                    title = item.text_content()
                    if title and title.strip():
                        titles.append(title.strip())
                except:
                    continue
            
            logger.info(f"找到 {len(titles)} 个历史对话")
            return titles
        except Exception as e:
            logger.error(f"获取历史对话列表失败: {str(e)}")
            return []
    
    def click_history_chat(self, title: str) -> bool:
        """
        点击指定标题的历史对话
        
        Args:
            title: 对话标题
            
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info(f"点击历史对话: {title}")
            self.page.click(f"text={title}")
            self.page.wait_for_timeout(1000)
            logger.info(f"历史对话 '{title}' 点击成功")
            return True
        except Exception as e:
            logger.error(f"点击历史对话失败: {str(e)}")
            return False
    
    def close_download_promotion(self) -> bool:
        """
        关闭下载推广区域
        
        Returns:
            bool: 是否关闭成功
        """
        try:
            if self.is_element_visible(self.DOWNLOAD_CLOSE_BUTTON, timeout=2000):
                logger.info("关闭下载推广区域")
                self.page.click(self.DOWNLOAD_CLOSE_BUTTON)
                self.page.wait_for_timeout(500)
                logger.info("下载推广区域已关闭")
                return True
            else:
                logger.info("下载推广区域不存在或已关闭")
                return True
        except Exception as e:
            logger.error(f"关闭下载推广区域失败: {str(e)}")
            return False
    
    def is_no_readings_displayed(self) -> bool:
        """
        检查是否显示 "No Readings Yet" 提示
        
        Returns:
            bool: 是否显示
        """
        return self.is_element_visible(self.NO_READINGS_TEXT, timeout=3000)
    
    def toggle_sidebar(self) -> bool:
        """
        切换侧边栏展开/收起
        
        Returns:
            bool: 是否切换成功
        """
        try:
            logger.info("切换侧边栏")
            self.page.click(self.MENU_TOGGLE)
            self.page.wait_for_timeout(500)
            logger.info("侧边栏切换成功")
            return True
        except Exception as e:
            logger.error(f"切换侧边栏失败: {str(e)}")
            return False
    
    def is_annual_button_visible(self) -> bool:
        """
        检查 Annual 按钮是否可见
        
        Returns:
            bool: Annual 按钮是否可见
        """
        return self.is_element_visible(self.ANNUAL_BUTTON, timeout=3000)
    
    def is_user_avatar_visible(self) -> bool:
        """
        检查用户头像是否可见
        
        Returns:
            bool: 用户头像是否可见
        """
        return self.is_element_visible(self.USER_AVATAR, timeout=3000)

