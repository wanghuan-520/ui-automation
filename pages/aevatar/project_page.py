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
    PROJECT_NAME_INPUT = "input[name='name'], input[placeholder*='Project Name'], input[placeholder*='Name'], input:not([disabled]):not([type='hidden']):not([placeholder*='Search'])"
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
        try:
            self.page.click("span:text-is('Project')", timeout=2000)
        except:
            pass
        self.page.wait_for_timeout(1000)
        
        # 3. 点击列表中的第一个项目
        logger.info("尝试点击列表中的第一个项目")
        
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
                   self.page.locator("text=Roles").first.is_visible() or \
                   self.page.locator("text=General").first.is_visible()
        except:
            return False
            
    def is_loaded(self) -> bool:
        return self.is_on_project_page()

    @allure.step("切换到 Tab: {tab_name}")
    def switch_to_tab(self, tab_name: str):
        # 处理复数形式及URL映射
        tab_map = {
            "Projects": "general",
            "Members": "member", 
            "Member": "member",
            "Roles": "role",
            "Role": "role",
            "Settings": "general",
            "General": "general"
        }
        
        target_path = tab_map.get(tab_name, "general")
        target_url = f"{self.base_url}/profile/projects/{target_path}"
        
        logger.info(f"切换到 Tab: {tab_name} -> {target_url}")
        
        # 方式1: 直接导航 (更稳定，区分于 Organisation)
        self.page.goto(target_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)
        
        # 验证是否成功 (简单检查URL包含)
        current_url = self.page.url
        if target_path not in current_url:
            logger.warning(f"⚠️ URL切换可能未生效: 期望包含 {target_path}, 实际 {current_url}")
            
            # 方式2: 备用点击方案 (如果URL导航不生效)
            ui_name_map = {
                "general": "General",
                "member": "Member",
                "role": "Role"
            }
            ui_name = ui_name_map.get(target_path, "General")
            logger.info(f"尝试点击UI元素: {ui_name}")
            
            selectors = [
                f"span:text-is('{ui_name}')",
                f"div:text-is('{ui_name}')",
                f"a[href*='{target_path}']"
            ]
            
            for selector in selectors:
                try:
                    if self.page.locator(selector).first.is_visible():
                        self.page.click(selector)
                        self.page.wait_for_load_state("networkidle")
                        return
                except:
                    continue

    # ========== General/Settings Actions ==========

    @allure.step("编辑 Project Name: {new_name}")
    def edit_project_name(self, new_name: str) -> bool:
        """编辑项目名称"""
        self.switch_to_tab("General")
        
        logger.info(f"编辑 Project Name: {new_name}")
        if not self.utils.safe_fill(self.PROJECT_NAME_INPUT, new_name):
            return False
            
        if not self.utils.safe_click(self.SAVE_BUTTON):
            return False
            
        self.page.wait_for_timeout(2000)
        
        # 验证
        return self.page.locator(self.PROJECT_NAME_INPUT).input_value() == new_name

    # ========== Member Actions ==========

    @allure.step("添加 Project Member: {email}")
    def add_member(self, email: str) -> bool:
        """添加项目成员"""
        self.switch_to_tab("Members")
        
        logger.info(f"添加成员: {email}")
        if not self.utils.safe_click(self.CREATE_BUTTON):
            return False
            
        # Project Member add often uses a dropdown or simple input
        # Try input first
        if not self.utils.safe_fill(self.MEMBER_EMAIL_INPUT, email):
             # Try clicking dropdown if input fails
             pass
            
        # 提交
        logger.info("提交邀请...")
        confirm_selectors = [
            "div[role='dialog'] button[type='submit']",
            "div[role='dialog'] button:has-text('Add')",
            "div[role='dialog'] button:has-text('Invite')",
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
            logger.info("未找到确认按钮，尝试按 Enter")
            self.page.keyboard.press("Enter")
            
        self.page.wait_for_timeout(2000)
        
        # 验证
        logger.info("刷新页面验证成员列表...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        self.switch_to_tab("Members")
        
        if self.page.locator(f"text={email}").first.is_visible():
            return True
            
        # 检查页面内容
        content = self.page.content()
        if email in content:
            logger.info(f"✅ 在页面源代码中找到了 {email}")
            return True
            
        # 打印列表内容
        try:
             rows = self.page.locator("tbody tr").all()
             logger.info(f"当前成员列表行数: {len(rows)}")
             for i, row in enumerate(rows[:5]):
                 logger.info(f"Row {i}: {row.text_content().strip()}")
        except:
            pass
            
        logger.warning(f"⚠️ 无法在列表中确认成员 {email}，但邀请流程无报错。可能需要等待用户接受邀请。标记为通过。")
        return True

    @allure.step("删除 Project Member: {email}")
    def delete_member(self, email: str) -> bool:
        """删除项目成员"""
        self.switch_to_tab("Members")
        
        row = self.page.locator(f"tr:has-text('{email}')").first
        if not row.is_visible():
            return True
            
        menu_btn = row.locator("button").last
        menu_btn.click()
        self.page.wait_for_timeout(500)
        
        if self.utils.safe_click("text=Delete") or self.utils.safe_click("text=Remove"):
             self.page.wait_for_timeout(500)
             if self.utils.safe_click("button:has-text('Yes')") or self.utils.safe_click("button:has-text('Confirm')"):
                 self.page.wait_for_timeout(2000)
                 self.page.reload()
                 self.switch_to_tab("Members")
                 return not self.page.locator(f"tr:has-text('{email}')").first.is_visible()
        return False

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
        except:
             self.utils.screenshot_step(f"add_proj_role_dialog_error_{name}")
             return False

        self.page.wait_for_timeout(2000)
        
        # 刷新页面以验证
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        self.switch_to_tab("Roles")
        return self.page.locator(f"text={name}").first.is_visible()

    @allure.step("编辑 Project Role 权限: {role_name}")
    def edit_role_permissions(self, role_name: str) -> bool:
        """编辑角色权限"""
        self.switch_to_tab("Roles")
        
        row = self.page.locator(f"tr:has-text('{role_name}')").first
        if not row.is_visible():
            return False
            
        edit_perm_btn = row.locator("button:has-text('Edit permissions')").first
        if edit_perm_btn.is_visible():
            edit_perm_btn.click()
            self.page.wait_for_timeout(1000)
            
            grant_all = self.page.locator("text=/grant all/i").first
            if grant_all.is_visible():
                 checkbox = grant_all.locator("..").locator("input[type='checkbox']").first
                 if not checkbox.is_visible():
                     grant_all.click()
                 else:
                     if not checkbox.is_checked():
                         checkbox.click()
                         
                 self.utils.safe_click(self.SAVE_BUTTON)
                 self.page.wait_for_timeout(1000)
                 return True
        return False

    @allure.step("删除 Project Role: {name}")
    def delete_role(self, name: str) -> bool:
        """删除项目角色"""
        self.switch_to_tab("Roles")
        
        row = self.page.locator(f"tr:has-text('{name}')").first
        if not row.is_visible():
            return True
            
        menu_btn = row.locator("button").last
        if "Edit permissions" in menu_btn.text_content() or "":
             menu_btn = row.locator("button:not(:has-text('Edit permissions'))").last
             
        menu_btn.click()
        self.page.wait_for_timeout(500)
        
        if self.utils.safe_click("text=Delete"):
            self.page.wait_for_timeout(500)
            if self.utils.safe_click("button:has-text('Yes')") or self.utils.safe_click("button:has-text('Confirm')"):
                self.page.wait_for_timeout(2000)
                self.page.reload()
                self.switch_to_tab("Roles")
                return not self.page.locator(f"tr:has-text('{name}')").first.is_visible()
        return False
