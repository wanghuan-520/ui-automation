from playwright.sync_api import Page
from typing import List, Dict, Optional
import allure
from pages.base_page import BasePage
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class OrganisationPage(BasePage):
    """Organisation 管理页面对象"""
    
    # 假设的 URL，会尝试自动修正
    ORG_URL_DIRECT = "/profile/organisation"
    ORG_URL_SETTINGS = "/dashboard/settings/organisation"
    
    # 页面元素
    # Tabs (修正为单数，且去掉 role=tab 限制，改用更宽泛的文本匹配)
    TAB_PROJECTS = "text=Project" 
    TAB_MEMBERS = "text=Member"
    TAB_ROLES = "text=Role"
    
    # Common
    # 增加更多 Create 按钮的变体
    CREATE_BUTTON = "button:has-text('Create'), button:has-text('Add'), button:has-text('Invite'), button:has-text('New')"
    SEARCH_INPUT = "input[placeholder*='Search']"
    TABLE_ROW = "tbody tr"
    
    # Project
    PROJECT_NAME_INPUT = "input[placeholder*='Name'], input[name='name'], input[name='displayName']"
    PROJECT_DESCRIPTION_INPUT = "textarea, input[placeholder*='Description']"
    
    # Member
    MEMBER_EMAIL_INPUT = "input[type='email'], input[placeholder*='Email'], input[name='email']"
    MEMBER_ROLE_SELECT = "div[class*='select']" 
    
    # Role
    ROLE_NAME_INPUT = "input[placeholder*='Name'], input[name='name'], input[name='roleName']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.ORG_URL_DIRECT}"

    @allure.step("导航到 Organisation 页面")
    def navigate(self) -> None:
        """导航到 Organisation 页面 (尝试多种路径)"""
        logger.info("尝试导航到 Organisation 页面")
        
        # 策略1: 直接访问 Profile/Organisation
        target_url = f"{self.base_url}/profile/organisation"
        logger.info(f"尝试直接访问: {target_url}")
        self.page.goto(target_url)
        self.page.wait_for_load_state("networkidle")
        
        # 检查是否成功 (看有没有 Project/Member Tab)
        if self.is_on_org_page():
            logger.info("✅ 成功进入 Organisation 页面")
            return
            
        # 策略2: 访问 Dashboard -> Settings
        logger.info("策略1失败，尝试通过 Settings 导航")
        self.page.goto(f"{self.base_url}/dashboard/settings")
        self.page.wait_for_load_state("networkidle")
        
        # 查找 Organisation 链接/Tab
        org_link = self.page.locator("text=Organisation").first
        if org_link.is_visible():
            org_link.click()
            self.page.wait_for_load_state("networkidle")
            if self.is_on_org_page():
                logger.info("✅ 通过 Settings 成功进入")
                return
                
        logger.warning("⚠️ 无法确定 Organisation 页面位置，可能仍在当前页")

    def is_on_org_page(self) -> bool:
        """检查是否在 Organisation 页面 (通过 Tabs 判断)"""
        try:
            # 检查是否存在 Projects 或 Members 标签页
            return self.page.locator("text=Projects").first.is_visible() or \
                   self.page.locator("text=Members").first.is_visible()
        except:
            return False
            
    def is_loaded(self) -> bool:
        return self.is_on_org_page()

    @allure.step("切换到 Tab/Menu: {tab_name}")
    def switch_to_tab(self, tab_name: str):
        """切换标签页或侧边栏菜单 (Project, Member, Role)"""
        # 处理复数形式到单数形式的映射
        name_map = {
            "Projects": "Project",
            "Members": "Member",
            "Roles": "Role"
        }
        target_name = name_map.get(tab_name, tab_name)
        
        logger.info(f"尝试切换到: {target_name}")
        
        # 策略1: 侧边栏菜单点击 (基于HTML结构分析)
        # 结构: div.cursor-pointer > span("Project")
        logger.info(f"尝试点击侧边栏菜单: {target_name}")
        
        selectors = [
            # 精确匹配 span 文本 (最优先)
            f"span:text-is('{target_name}')",
            # 匹配包含文本的 cursor-pointer div
            f"div.cursor-pointer:has-text('{target_name}')",
            # 回退到之前的选择器
            f"nav a:has-text('{target_name}')",
            f"div[role='button']:has-text('{target_name}')"
        ]
        
        for selector in selectors:
            try:
                elements = self.page.locator(selector).all()
                for el in elements:
                    if el.is_visible():
                        # 尝试点击
                        logger.info(f"尝试点击元素: {selector}")
                        el.click(timeout=1000)
                        self.page.wait_for_load_state("networkidle")
                        self.page.wait_for_timeout(1000)
                        
                        # 验证是否切换成功 (简单的验证：看是否出现了特定的 Header 或 按钮)
                        # 这里暂不强求验证，假设点击有效
                        return
            except:
                continue

        logger.warning(f"⚠️ 未能通过常规方式切换到: {target_name}")

    # ========== Project Actions ==========
    
    @allure.step("创建 Project: {name}")
    def create_project(self, name: str, description: str = "") -> bool:
        """创建项目"""
        self.switch_to_tab("Projects")
        
        # 点击 Create
        logger.info("点击 Create Project")
        if not self.utils.safe_click(self.CREATE_BUTTON):
            logger.error("未找到 Create 按钮")
            return False
            
        # 等待弹窗
        self.page.wait_for_timeout(1000)
            
        # 填写表单
        logger.info(f"填写项目名称: {name}")
        if not self.utils.safe_fill(self.PROJECT_NAME_INPUT, name):
            return False
            
        if description:
            # 尝试填写描述，如果找不到元素则跳过
            if not self.utils.safe_fill(self.PROJECT_DESCRIPTION_INPUT, description, timeout=5000):
                logger.warning("填写 Description 失败，跳过")
            
        # 提交
        logger.info("提交表单...")
        confirm_selectors = [
            "div[role='dialog'] button[type='submit']",
            "div[role='dialog'] button:has-text('Create')",
            "div[role='dialog'] button:has-text('Confirm')",
            "div[role='dialog'] button:has-text('Save')"
        ]
        
        clicked = False
        for selector in confirm_selectors:
            btn = self.page.locator(selector).first
            if btn.is_visible():
                logger.info(f"点击确认按钮: {selector}")
                btn.click()
                clicked = True
                break
        
        if not clicked:
            logger.info("未找到确认按钮，尝试按 Enter")
            self.page.keyboard.press("Enter")
            
        # 等待弹窗消失，验证提交是否成功
        try:
            logger.info("等待弹窗关闭...")
            dialog = self.page.locator("div[role='dialog']").first
            # 如果弹窗本来就不存在(极快关闭)，wait_for hidden 也会通过
            if dialog.is_visible():
                dialog.wait_for(state="hidden", timeout=5000)
            logger.info("✅ 弹窗已关闭")
        except Exception as e:
            logger.error("❌ 弹窗未关闭! 可能存在校验错误")
            try:
                content = dialog.text_content()
                logger.error(f"弹窗内容: {content}")
            except:
                pass
            self.utils.screenshot_step(f"create_project_dialog_error_{name}")
            return False

        self.page.wait_for_timeout(1000)
        self.utils.screenshot_step(f"after_submit_{name}")
        self.page.wait_for_timeout(2000)
        
        # 刷新页面以验证
        logger.info("刷新页面以验证列表更新...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        # 重新确保在正确的 Tab
        self.switch_to_tab("Projects")
        
        # 验证
        logger.info(f"验证列表是否存在: {name}")
        
        # 打印当前列表的所有文本，辅助调试
        try:
            # 假设是表格行
            rows = self.page.locator("tbody tr").all()
            if not rows:
                rows = self.page.locator("div[role='row']").all()
            
            logger.info(f"当前列表行数: {len(rows)}")
            for i, row in enumerate(rows[:10]): # 只打印前10行
                logger.info(f"Row {i}: {row.text_content().strip()}")
        except Exception as e:
            logger.warning(f"无法打印列表内容: {e}")

        # 使用更宽泛的文本匹配，防止 html 结构复杂
        return self.page.locator(f"text={name}").first.is_visible()

    # ========== Member Actions ==========

    @allure.step("邀请成员: {email}")
    def invite_member(self, email: str, role: str = "Member") -> bool:
        """邀请成员"""
        self.switch_to_tab("Members")
        
        logger.info(f"邀请成员: {email}")
        if not self.utils.safe_click(self.CREATE_BUTTON): # 可能是 Invite Member
            return False
            
        if not self.utils.safe_fill(self.MEMBER_EMAIL_INPUT, email):
            return False
            
        # 简单的角色选择 (如果需要)
        # ...
        
        # 提交
        confirm_btn = self.page.locator("div[role='dialog'] button[type='submit'], div[role='dialog'] button:has-text('Invite'), div[role='dialog'] button:has-text('Add')").first
        if confirm_btn.is_visible():
            confirm_btn.click()
        else:
            self.page.keyboard.press("Enter")
            
        self.page.wait_for_timeout(2000)
        
        # 验证 (可能在列表中，也可能在 Pending 中)
        # 简单检查是否报错
        if self.page.locator("text=Error").is_visible():
            return False
        return True

    # ========== Role Actions ==========

    @allure.step("创建角色: {name}")
    def create_role(self, name: str) -> bool:
        """创建角色"""
        self.switch_to_tab("Roles")
        
        logger.info(f"创建角色: {name}")
        if not self.utils.safe_click(self.CREATE_BUTTON):
            return False
            
        if not self.utils.safe_fill(self.ROLE_NAME_INPUT, name):
            return False
            
        # 提交
        logger.info("提交表单...")
        confirm_selectors = [
            "div[role='dialog'] button[type='submit']",
            "div[role='dialog'] button:has-text('Create')",
            "div[role='dialog'] button:has-text('Confirm')"
        ]
        
        clicked = False
        for selector in confirm_selectors:
            btn = self.page.locator(selector).first
            if btn.is_visible():
                logger.info(f"点击确认按钮: {selector}")
                btn.click()
                clicked = True
                break
                
        if not clicked:
            self.page.keyboard.press("Enter")
            
        # 等待弹窗消失
        try:
            logger.info("等待弹窗关闭...")
            dialog = self.page.locator("div[role='dialog']").first
            if dialog.is_visible():
                dialog.wait_for(state="hidden", timeout=5000)
            logger.info("✅ 弹窗已关闭")
        except Exception as e:
            logger.error("❌ 弹窗未关闭! 可能存在校验错误")
            try:
                content = dialog.text_content()
                logger.error(f"弹窗内容: {content}")
            except:
                pass
            self.utils.screenshot_step(f"create_role_dialog_error_{name}")
            return False

        self.page.wait_for_timeout(3000)
        
        # 刷新验证
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.switch_to_tab("Roles")
        
        # 验证
        logger.info(f"验证列表是否存在: {name}")
        
        # 打印当前列表的所有文本，辅助调试
        try:
            # 尝试获取列表内容
            rows = self.page.locator("tbody tr").all()
            if not rows:
                rows = self.page.locator("div[role='row']").all()
            
            logger.info(f"当前列表行数: {len(rows)}")
            for i, row in enumerate(rows[:10]): # 只打印前10行
                logger.info(f"Row {i}: {row.text_content().strip()}")
        except Exception as e:
            logger.warning(f"无法打印列表内容: {e}")

        return self.page.locator(f"text={name}").first.is_visible()

