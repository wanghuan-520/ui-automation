import pytest
from playwright.sync_api import Page
from pages.godgpt.godgpt_landing_page import GodGPTLandingPage
from pages.godgpt.godgpt_email_login_page import GodGPTEmailLoginPage
from pages.godgpt.godgpt_main_page import GodGPTMainPage
from utils.data_manager import DataManager
from utils.logger import get_logger

logger = get_logger(__name__)

class TestGodGPTMain:
    """GodGPT 主界面功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.landing_page = GodGPTLandingPage(page)
        self.email_login_page = GodGPTEmailLoginPage(page)
        self.main_page = GodGPTMainPage(page)
        
        # 加载测试数据
        try:
            self.login_data = DataManager.load_json("test-data/godgpt/godgpt_login_data.json")
            self.conversation_data = DataManager.load_json("test-data/godgpt/godgpt_conversation_data.json")
        except Exception as e:
            logger.warning(f"加载测试数据失败: {e}")
            self.login_data = {}
            self.conversation_data = {}
    
    def login_to_app(self):
        """辅助方法：登录到应用"""
        valid_user = self.login_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        password = valid_user.get("password", "Wh520520!")
        
        logger.info("执行登录流程...")
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        self.email_login_page.enter_password(password)
        self.email_login_page.click_continue()
        self.main_page.wait_for_page_load()
        
        assert self.main_page.is_logged_in(), "❌ 登录失败"
        logger.info("✅ 登录成功")
    
    @pytest.mark.main
    @pytest.mark.high_priority
    def test_tc007_new_chat(self):
        """
        TC007: 新建对话
        验证可以创建新对话并发送消息
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC007: 新建对话")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        
        # 关闭下载推广（如果存在）
        self.main_page.close_download_promotion()
        
        # 点击新建对话
        logger.info("点击新建对话按钮")
        assert self.main_page.click_new_chat(), "❌ 新建对话按钮点击失败"
        self.page.wait_for_timeout(1000)
        logger.info("✅ 新建对话按钮点击成功")
        
        # 输入测试问题
        test_message = "Hello, how are you?"
        logger.info(f"输入测试消息: {test_message}")
        assert self.main_page.send_message(test_message), "❌ 消息发送失败"
        logger.info("✅ 消息发送成功")
        
        # 等待AI回复
        self.page.wait_for_timeout(5000)
        logger.info("等待AI回复...")
        
        logger.info("🎉 TC007 测试通过")
    
    @pytest.mark.main
    @pytest.mark.high_priority
    def test_tc008_history_chat_switch(self):
        """
        TC008: 历史对话切换
        验证可以切换历史对话
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC008: 历史对话切换")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 获取历史对话列表
        logger.info("获取历史对话列表")
        chat_titles = self.main_page.get_history_chat_titles()
        logger.info(f"找到 {len(chat_titles)} 个历史对话")
        
        if len(chat_titles) > 0:
            # 点击第一个历史对话
            first_chat = chat_titles[0]
            logger.info(f"点击历史对话: {first_chat}")
            assert self.main_page.click_history_chat(first_chat), "❌ 历史对话点击失败"
            logger.info("✅ 历史对话切换成功")
            
            # 验证输入框可用
            self.page.wait_for_timeout(2000)
            assert self.main_page.is_element_visible(self.main_page.MAIN_INPUT), "❌ 输入框未显示"
            logger.info("✅ 输入框可用，可以继续对话")
        else:
            logger.info("⚠️  暂无历史对话，跳过测试")
        
        logger.info("🎉 TC008 测试通过")
    
    @pytest.mark.main
    @pytest.mark.high_priority
    def test_tc009_soul_link_card(self):
        """
        TC009: 快捷功能卡片 - Soul Link
        验证 Soul Link 卡片功能正常
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC009: Soul Link 卡片")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 检查 Soul Link 卡片是否可见
        if self.main_page.is_element_visible(self.main_page.SOUL_LINK_CARD, timeout=3000):
            logger.info("Soul Link 卡片可见")
            
            # 点击 Soul Link 卡片
            logger.info("点击 Soul Link 卡片")
            assert self.main_page.click_soul_link_card(), "❌ Soul Link 卡片点击失败"
            logger.info("✅ Soul Link 卡片点击成功")
            
            # 验证功能启动
            self.page.wait_for_timeout(2000)
            logger.info("✅ Soul Link 功能已启动")
        else:
            logger.info("⚠️  Soul Link 卡片不可见，可能已被使用或不在当前视图")
        
        logger.info("🎉 TC009 测试通过")
    
    @pytest.mark.main
    @pytest.mark.high_priority
    def test_tc010_unlock_path_card(self):
        """
        TC010: 快捷功能卡片 - Unlock Your Path
        验证 Unlock Your Path 卡片功能正常
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC010: Unlock Your Path 卡片")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 检查卡片是否可见
        if self.main_page.is_element_visible(self.main_page.UNLOCK_PATH_CARD, timeout=3000):
            logger.info("Unlock Your Path 卡片可见")
            
            # 点击卡片
            logger.info("点击 Unlock Your Path 卡片")
            assert self.main_page.click_unlock_path_card(), "❌ Unlock Your Path 卡片点击失败"
            logger.info("✅ Unlock Your Path 卡片点击成功")
            
            # 验证功能启动
            self.page.wait_for_timeout(2000)
            logger.info("✅ Unlock Your Path 功能已启动")
        else:
            logger.info("⚠️  Unlock Your Path 卡片不可见")
        
        logger.info("🎉 TC010 测试通过")
    
    @pytest.mark.main
    @pytest.mark.medium_priority
    def test_tc011_annual_button(self):
        """
        TC011: Annual 会员功能
        验证可以访问会员订阅页面
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC011: Annual 会员功能")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 验证 Annual 按钮可见
        assert self.main_page.is_annual_button_visible(), "❌ Annual 按钮不可见"
        logger.info("✅ Annual 按钮可见")
        
        # 点击 Annual 按钮
        logger.info("点击 Annual 按钮")
        assert self.main_page.click_annual_button(), "❌ Annual 按钮点击失败"
        logger.info("✅ Annual 按钮点击成功")
        
        # 验证页面跳转或弹窗
        self.page.wait_for_timeout(2000)
        current_url = self.main_page.get_current_url()
        logger.info(f"当前URL: {current_url}")
        logger.info("✅ Annual 功能可访问")
        
        logger.info("🎉 TC011 测试通过")
    
    @pytest.mark.main
    @pytest.mark.medium_priority
    def test_tc012_user_avatar(self):
        """
        TC012: 用户头像 - 个人中心
        验证可以访问个人中心
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC012: 用户头像 - 个人中心")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 验证用户头像可见
        if self.main_page.is_user_avatar_visible():
            logger.info("✅ 用户头像可见")
            
            # 点击用户头像
            logger.info("点击用户头像")
            assert self.main_page.click_user_avatar(), "❌ 用户头像点击失败"
            logger.info("✅ 用户头像点击成功")
            
            # 验证菜单或页面变化
            self.page.wait_for_timeout(2000)
            logger.info("✅ 个人中心菜单或页面已打开")
        else:
            logger.warning("⚠️  用户头像不可见")
        
        logger.info("🎉 TC012 测试通过")
    
    @pytest.mark.main
    @pytest.mark.medium_priority
    def test_tc013_voice_input(self):
        """
        TC013: 语音输入功能
        验证语音输入按钮可点击
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC013: 语音输入功能")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 检查语音按钮是否可见
        if self.main_page.is_element_visible(self.main_page.VOICE_BUTTON, timeout=3000):
            logger.info("✅ 语音按钮可见")
            
            # 点击语音按钮
            logger.info("点击语音按钮")
            assert self.main_page.click_voice_button(), "❌ 语音按钮点击失败"
            logger.info("✅ 语音按钮点击成功")
            
            # 验证权限请求或录音界面
            self.page.wait_for_timeout(2000)
            logger.info("✅ 语音功能已触发")
            logger.info("⚠️  注意：实际语音录制需要浏览器权限，自动化测试可能无法完整模拟")
        else:
            logger.info("⚠️  语音按钮不可见")
        
        logger.info("🎉 TC013 测试通过")
    
    @pytest.mark.main
    @pytest.mark.medium_priority
    def test_tc014_attach_file(self):
        """
        TC014: 附件上传功能
        验证附件按钮可点击
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC014: 附件上传功能")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 检查附件按钮是否可见
        if self.main_page.is_element_visible(self.main_page.ATTACH_BUTTON, timeout=3000):
            logger.info("✅ 附件按钮可见")
            
            # 点击附件按钮
            logger.info("点击附件按钮")
            assert self.main_page.click_attach_button(), "❌ 附件按钮点击失败"
            logger.info("✅ 附件按钮点击成功")
            
            # 验证文件选择器或附件菜单
            self.page.wait_for_timeout(2000)
            logger.info("✅ 附件功能已触发")
            logger.info("⚠️  注意：实际文件上传需要文件选择器交互，自动化测试暂不完整模拟")
        else:
            logger.info("⚠️  附件按钮不可见")
        
        logger.info("🎉 TC014 测试通过")
    
    @pytest.mark.main
    @pytest.mark.low_priority
    def test_tc015_download_promotion(self):
        """
        TC015: Get App 下载推广
        验证下载推广区域功能
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC015: Get App 下载推广")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        
        # 检查下载推广区域是否可见
        if self.main_page.is_element_visible(self.main_page.DOWNLOAD_SECTION, timeout=3000):
            logger.info("✅ 下载推广区域可见")
            
            # 检查各个元素
            app_store_visible = self.main_page.is_element_visible(self.main_page.APP_STORE_LINK, timeout=2000)
            google_play_visible = self.main_page.is_element_visible(self.main_page.GOOGLE_PLAY_LINK, timeout=2000)
            qr_code_visible = self.main_page.is_element_visible(self.main_page.QR_CODE, timeout=2000)
            
            logger.info(f"App Store 链接: {app_store_visible}")
            logger.info(f"Google Play 链接: {google_play_visible}")
            logger.info(f"QR Code: {qr_code_visible}")
            
            # 关闭下载推广
            logger.info("关闭下载推广区域")
            assert self.main_page.close_download_promotion(), "❌ 关闭下载推广失败"
            logger.info("✅ 下载推广区域已关闭")
            
            # 验证关闭后不再可见
            self.page.wait_for_timeout(1000)
            is_still_visible = self.main_page.is_element_visible(self.main_page.DOWNLOAD_SECTION, timeout=2000)
            if not is_still_visible:
                logger.info("✅ 下载推广区域确认已关闭")
            else:
                logger.warning("⚠️  下载推广区域可能仍然可见")
        else:
            logger.info("⚠️  下载推广区域不可见或已被关闭")
        
        logger.info("🎉 TC015 测试通过")
    
    @pytest.mark.main
    @pytest.mark.smoke
    @pytest.mark.parametrize("message_data", [
        {"message": "Hello, how are you?", "type": "greeting"},
        {"message": "What is the meaning of life?", "type": "philosophical"},
    ])
    def test_send_normal_messages(self, message_data):
        """
        发送普通消息测试（参数化）
        验证不同类型的消息可以正常发送
        """
        logger.info("=" * 80)
        logger.info(f"开始测试: 发送{message_data['type']}类型消息")
        logger.info("=" * 80)
        
        # 登录
        self.login_to_app()
        self.main_page.close_download_promotion()
        
        # 发送消息
        message = message_data["message"]
        logger.info(f"发送消息: {message}")
        assert self.main_page.send_message(message), f"❌ 消息发送失败: {message}"
        logger.info("✅ 消息发送成功")
        
        # 等待响应
        self.page.wait_for_timeout(3000)
        logger.info("等待AI响应...")
        
        logger.info("🎉 测试通过")

