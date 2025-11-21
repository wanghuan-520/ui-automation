from playwright.sync_api import Page
import allure
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class ProjectPage(BasePage):
    """Project 管理页面对象 (针对当前选定的 Project)"""
    
    # 假设 URL
    PROJECT_URL_DIRECT = "/profile/projects"
    PROJECT_URL_SETTINGS = "/dashboard/settings/project"
    
    # 元素选择器
    TAB_MEMBERS = "div[role='tab']:has-text('Members')"
    TAB_ROLES = "div[role='tab']:has-text('Roles')"
    TAB_SETTINGS = "div[role='tab']:has-text('Settings')" # Project Name edit likely here
    
    # Common
    CREATE_BUTTON = "button:has-text('Create'), button:has-text('Add'), button:has-text('Invite'), button:has-text('New')"
    
    # Member
    MEMBER_EMAIL_INPUT = "input[type='email'], input[placeholder*='Email'], input[name='email']"
    
    # Role
    ROLE_NAME_INPUT = "input[placeholder*='Role Name'], input[name='roleName'], input[name='name']"
    
    # Project Settings
    PROJECT_NAME_INPUT = "input[name='name'], input[placeholder*='Project Name']"
    SAVE_BUTTON = "button:has-text('Save')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.PROJECT_URL_DIRECT}"

    @allure.step("导航到 Project 页面")
    def navigate(self) -> None:
        """导航到 Project Settings 页面 (通过 Organisation -> Project List -> Click Project)"""
        logger.info("尝试导航到 Project 页面")
        
        # 1. 先进入 Organisation 页面
        self.page.goto(f"{self.base_url}/profile/organisation")
        self.page.wait_for_load_state("networkidle")
        
        # 2. 确保在 Projects 列表
        # 复用 OrganisationPage 的逻辑，或者简单查找
        # 这里假设默认就是 Projects，或者点击 Project 侧边栏
        try:
            self.page.click("span:text-is('Project')", timeout=2000)
        except:
            pass
        self.page.wait_for_timeout(1000)
        
        # 3. 点击列表中的第一个项目
        # 假设项目名称是链接，或者所在的行是可点击的
        logger.info("尝试点击列表中的第一个项目")
        
        # 尝试点击 default project 或任意项目
        # 策略: 找 tbody tr first -> 找 a 标签 或 找 td first click
        try:
            # 尝试点击 explicit 'default project' if exists, otherwise first row
            project_link = self.page.locator("tbody tr td").first
            if project_link.is_visible():
                project_link.click()
            else:
                # 尝试点击 text="default project"
                self.page.click("text=default project", timeout=2000)
                
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)
            
            if self.is_on_project_page():
                logger.info("✅ 成功进入 Project 详情页")
                return
        except Exception as e:
            logger.warning(f"点击项目失败: {e}")

        logger.warning("⚠️ 无法确定 Project 页面位置，尝试截图")
        self.utils.screenshot_step("project_navigation_failed_final")

    def is_on_project_page(self) -> bool:
        try:
            return self.page.locator("text=Members").first.is_visible() or \
                   self.page.locator("text=Roles").first.is_visible()
        except:
            return False
            
    def is_loaded(self) -> bool:
        return self.is_on_project_page()

    @allure.step("切换到 Tab: {tab_name}")
    def switch_to_tab(self, tab_name: str):
        # 处理复数形式
        name_map = {
            "Projects": "Project",
            "Members": "Member",
            "Roles": "Role"
        }
        target_name = name_map.get(tab_name, tab_name)
        logger.info(f"切换到 Tab: {target_name}")
        
        selectors = [
            f"span:text-is('{target_name}')",
            f"div.cursor-pointer:has-text('{target_name}')",
            f"div[role='tab']:has-text('{target_name}')",
            f"text={target_name}"
        ]
        
        for selector in selectors:
            try:
                elements = self.page.locator(selector).all()
                for el in elements:
                    if el.is_visible():
                        el.click(timeout=1000)
                        self.page.wait_for_load_state("networkidle")
                        self.page.wait_for_timeout(1000)
                        return
            except:
                continue
        
        logger.warning(f"⚠️ 未能切换到: {target_name}")

    # ========== Member Actions ==========

    @allure.step("添加 Project Member: {email}")
    def add_member(self, email: str) -> bool:
        """添加项目成员"""
        self.switch_to_tab("Members")
        
        logger.info(f"添加成员: {email}")
        if not self.utils.safe_click(self.CREATE_BUTTON):
            return False
            
        if not self.utils.safe_fill(self.MEMBER_EMAIL_INPUT, email):
            return False
            
        # 提交
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000)
        
        # 简单验证
        return not self.page.locator("text=Error").is_visible()

    # ========== Role Actions ==========

    @allure.step("添加 Project Role: {name}")
    def add_role(self, name: str) -> bool:
        """添加项目角色"""
        self.switch_to_tab("Roles")
        
        logger.info(f"添加角色: {name}")
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
            self.utils.screenshot_step(f"add_proj_role_dialog_error_{name}")
            return False

        self.page.wait_for_timeout(2000)
        
        # 刷新页面以验证
        logger.info("刷新页面以验证列表更新...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        self.switch_to_tab("Roles")
        
        # 打印列表辅助调试
        try:
            rows = self.page.locator("tbody tr").all()
            if not rows:
                rows = self.page.locator("div[role='row']").all()
            logger.info(f"当前列表行数: {len(rows)}")
            for i, row in enumerate(rows[:10]):
                logger.info(f"Row {i}: {row.text_content().strip()}")
        except Exception as e:
            logger.warning(f"无法打印列表内容: {e}")

        return self.page.locator(f"text={name}").first.is_visible()

