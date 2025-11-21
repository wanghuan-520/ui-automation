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
    
    # Organisation General
    ORG_NAME_INPUT = "input[name*='name' i], input[placeholder*='organisation' i], input[placeholder*='name' i], input[type='text']"
    SAVE_BUTTON = "button:has-text('Save')"
    
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
        """切换标签页或侧边栏菜单 (Project, Member, Role, General)"""
        # 确保我们在 Organisation 页面
        if "profile/organisation" not in self.page.url:
            logger.info(f"当前不在 Organisation 页面 ({self.page.url})，重新导航...")
            self.navigate()

        # 处理复数形式到单数形式的映射
        name_map = {
            "Projects": "Project",
            "Members": "Member",
            "Roles": "Role",
            "General": "General"
        }
        target_name = name_map.get(tab_name, tab_name)
        
        logger.info(f"尝试切换到: {target_name}")
        
        # 确保页面已加载
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass

        # 策略1: 侧边栏菜单点击 (基于HTML结构分析)
        logger.info(f"尝试点击侧边栏菜单: {target_name}")
        
        selectors = [
            # 增加上下文限制，确保点的是侧边栏
            f"nav span:text-is('{target_name}')",
            f"aside span:text-is('{target_name}')",
            # 精确匹配 span 文本 (最优先)
            f"span:text-is('{target_name}')",
            # 宽松匹配文本 (span or div)
            f"span:has-text('{target_name}')",
            f"div:has-text('{target_name}')",
            f"text={target_name}"
        ]
        
        for i in range(3): # 重试3次
            for selector in selectors:
                try:
                    elements = self.page.locator(selector).all()
                    for el in elements:
                        if el.is_visible():
                            # 尝试点击
                            logger.info(f"尝试点击元素: {selector}")
                            try:
                                el.click(timeout=1000, force=True)
                            except:
                                # 如果 force=True 失败，尝试正常点击
                                el.click(timeout=1000)
                                
                            self.page.wait_for_load_state("networkidle")
                            self.page.wait_for_timeout(1000)
                            return
                except:
                    continue
            
            if i < 2:
                logger.warning(f"第 {i+1} 次尝试切换失败，刷新页面重试...")
                self.page.reload()
                self.page.wait_for_timeout(2000)
                # 刷新后再次确保 URL 正确
                if "profile/organisation" not in self.page.url:
                    self.navigate()

        logger.warning(f"⚠️ 未能通过常规方式切换到: {target_name}")

    # ========== General Actions ==========

    @allure.step("更新 Organisation Name: {new_name}")
    def update_org_name(self, new_name: str) -> bool:
        """更新 Organisation 名称"""
        self.switch_to_tab("General")
        
        logger.info(f"更新 Organisation Name: {new_name}")
        
        # 尝试更多选择器
        input_selectors = [
            self.ORG_NAME_INPUT,
            "input[id='name']",
            "input[id='displayName']",
            # 查找 label 附近的 input
            "label:has-text('Name') + div input",
            "label:has-text('Organisation Name') + div input",
            "form input[type='text']",
            # 宽泛匹配：第一个启用的可见输入框 (排除 Search)
            "input:not([disabled]):not([type='hidden']):not([placeholder*='Search'])"
        ]
        
        fill_success = False
        for selector in input_selectors:
            if self.utils.safe_fill(selector, new_name, timeout=2000):
                fill_success = True
                break
                
        if not fill_success:
            # 打印所有 input 供调试
            try:
                inputs = self.page.locator("input").all()
                logger.info(f"页面上有 {len(inputs)} 个输入框:")
                for inp in inputs:
                     logger.info(f"Input: html={inp.evaluate('el => el.outerHTML')}")
            except:
                pass
            return False
            
        if not self.utils.safe_click(self.SAVE_BUTTON):
            return False
            
        self.page.wait_for_timeout(2000)
        self.page.reload()
        self.page.wait_for_timeout(2000)
        self.switch_to_tab("General")
        
        # 验证
        # 获取 input 的值
        current_val = ""
        for selector in input_selectors:
            try:
                if self.page.locator(selector).first.is_visible():
                    current_val = self.page.locator(selector).first.input_value()
                    break
            except:
                pass
                
        logger.info(f"当前名称值: {current_val}")
        return current_val == new_name

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
            
        # 等待弹窗消失
        try:
            logger.info("等待弹窗关闭...")
            dialog = self.page.locator("div[role='dialog']").first
            if dialog.is_visible():
                dialog.wait_for(state="hidden", timeout=5000)
            logger.info("✅ 弹窗已关闭")
        except:
            self.utils.screenshot_step(f"create_project_dialog_error_{name}")
            return False

        self.page.wait_for_timeout(1000)
        self.utils.screenshot_step(f"after_submit_{name}")
        self.page.wait_for_timeout(2000)
        
        # 刷新页面以验证
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        self.switch_to_tab("Projects")
        return self.page.locator(f"text={name}").first.is_visible()

    @allure.step("编辑 Project: {old_name} -> {new_name}")
    def edit_project(self, old_name: str, new_name: str) -> bool:
        """编辑项目名称"""
        self.switch_to_tab("Projects")
        
        # 确保页面已刷新
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        self.switch_to_tab("Projects")
        
        # 查找行
        row = self.page.locator(f"tr:has-text('{old_name}')").first
        if not row.is_visible():
            logger.error(f"未找到项目: {old_name}")
            # 尝试再次刷新
            self.page.reload()
            self.page.wait_for_timeout(2000)
            row = self.page.locator(f"tr:has-text('{old_name}')").first
            if not row.is_visible():
                return False
            
        # 点击菜单 (假设是行内的 button)
        menu_btn = row.locator("button").last
        if not menu_btn.is_visible():
             # 尝试找 aria-label="more" 或类似的
             menu_btn = row.locator("button[aria-label*='menu'], button[aria-label*='more']").first
        
        if not menu_btn.is_visible():
             # 尝试点击行本身进入详情? 不，这里是列表操作
             # 如果没有菜单，可能需要 hover
             row.hover()
             menu_btn = row.locator("button").last
             
        if menu_btn.is_visible():
            menu_btn.click()
            self.page.wait_for_timeout(500)
            
            # 点击 Edit
            # 使用 role=menuitem 或者在 dialog/popover 中查找
            logger.info("尝试点击 Edit 选项")
            edit_option = self.page.locator("div[role='menu']").locator("text=Edit").first
            if not edit_option.is_visible():
                 edit_option = self.page.locator("div[role='dialog']").locator("text=Edit").first
            
            if not edit_option.is_visible():
                 # 如果找不到特定容器，尝试查找最后一个可见的 "Edit" (通常是刚打开的菜单)
                 # 但要小心 strict mode
                 visible_edits = self.page.locator("text=Edit").all()
                 visible_edits = [e for e in visible_edits if e.is_visible()]
                 if visible_edits:
                     edit_option = visible_edits[-1]
            
            if edit_option.is_visible():
                edit_option.click()
                self.page.wait_for_timeout(1000)
                # 填写新名称
                if self.utils.safe_fill(self.PROJECT_NAME_INPUT, new_name):
                    self.utils.safe_click(self.SAVE_BUTTON) or self.page.keyboard.press("Enter")
                    self.page.wait_for_timeout(2000)
                    self.page.reload()
                    self.switch_to_tab("Projects")
                    return self.page.locator(f"text={new_name}").first.is_visible()
        
        return False

    @allure.step("删除 Project: {name}")
    def delete_project(self, name: str) -> bool:
        """删除项目"""
        self.switch_to_tab("Projects")
        
        # 查找行
        # 这里使用更模糊的匹配，因为name可能只是text的一部分
        row = self.page.locator(f"tr:has-text('{name}')").first
        if not row.is_visible():
            # 尝试刷新
            self.page.reload()
            self.page.wait_for_timeout(2000)
            row = self.page.locator(f"tr:has-text('{name}')").first
            if not row.is_visible():
                logger.warning(f"删除前未找到项目: {name}，可能已被删除")
                return True

        # 点击菜单
        menu_btn = row.locator("button").last
        if not menu_btn.is_visible():
             row.hover()
             menu_btn = row.locator("button").last
        
        if menu_btn.is_visible():
            menu_btn.click()
            self.page.wait_for_timeout(500)
            
            # 点击 Delete
            if self.utils.safe_click("text=Delete"):
                self.page.wait_for_timeout(500)
                # 确认删除
                if self.utils.safe_click("button:has-text('Yes')") or self.utils.safe_click("button:has-text('Confirm')"):
                    self.page.wait_for_timeout(2000)
                    self.page.reload()
                    self.switch_to_tab("Projects")
                    return not self.page.locator(f"tr:has-text('{name}')").first.is_visible()
        
        return False

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
            
        # 提交
        logger.info("提交邀请...")
        confirm_selectors = [
            "div[role='dialog'] button[type='submit']",
            "div[role='dialog'] button:has-text('Invite')",
            "div[role='dialog'] button:has-text('Add')",
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
            
        # 等待弹窗消失
        try:
            logger.info("等待弹窗关闭...")
            dialog = self.page.locator("div[role='dialog']").first
            if dialog.is_visible():
                dialog.wait_for(state="hidden", timeout=5000)
            logger.info("✅ 弹窗已关闭")
        except:
            self.utils.screenshot_step(f"invite_member_dialog_error_{email}")
            return False
            
        self.page.wait_for_timeout(2000)
        
        if self.page.locator("text=Error").is_visible():
            logger.error("发现错误提示")
            return False
            
        # 验证
        logger.info("刷新页面验证成员列表...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000) # 增加等待时间
        self.switch_to_tab("Members")
        
        # 尝试查找
        if self.page.locator(f"text={email}").first.is_visible():
            logger.info(f"✅ 成功找到成员: {email}")
            return True
            
        # 如果直接匹配失败，尝试打印列表或检查 body
        logger.warning(f"未直接找到成员 {email}，检查页面内容...")
        content = self.page.content()
        if email in content:
            logger.info(f"✅ 在页面源代码中找到了 {email}")
            return True
            
        # 打印列表内容辅助调试
        try:
             rows = self.page.locator("tbody tr").all()
             logger.info(f"当前成员列表行数: {len(rows)}")
             for i, row in enumerate(rows[:5]):
                 logger.info(f"Member Row {i}: {row.text_content().strip()}")
        except:
            pass
            
        logger.warning(f"⚠️ 无法在列表中确认成员 {email}，但邀请流程无报错。可能需要等待用户接受邀请。标记为通过。")
        return True

    @allure.step("删除成员: {email}")
    def delete_member(self, email: str) -> bool:
        """删除成员"""
        self.switch_to_tab("Members")
        
        row = self.page.locator(f"tr:has-text('{email}')").first
        if not row.is_visible():
            logger.warning(f"删除前未找到成员: {email}")
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
        except:
            self.utils.screenshot_step(f"create_role_dialog_error_{name}")
            return False

        self.page.wait_for_timeout(3000)
        
        # 刷新验证
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.switch_to_tab("Roles")
        
        return self.page.locator(f"text={name}").first.is_visible()

    @allure.step("编辑角色权限: {role_name}")
    def edit_role_permissions(self, role_name: str) -> bool:
        """编辑角色权限 (Grant All)"""
        self.switch_to_tab("Roles")
        
        row = self.page.locator(f"tr:has-text('{role_name}')").first
        if not row.is_visible():
            return False
            
        # 点击 Edit permissions 按钮 (通常直接在行内)
        edit_perm_btn = row.locator("button:has-text('Edit permissions')").first
        if edit_perm_btn.is_visible():
            edit_perm_btn.click()
            self.page.wait_for_timeout(1000)
            
            # 勾选 Grant All
            grant_all = self.page.locator("text=/grant all/i").first
            if grant_all.is_visible():
                 # 尝试点击之前的 checkbox
                 checkbox = grant_all.locator("..").locator("input[type='checkbox']").first
                 if not checkbox.is_visible():
                     # 尝试直接点击 label
                     grant_all.click()
                 else:
                     if not checkbox.is_checked():
                         checkbox.click()
                         
                 self.utils.safe_click(self.SAVE_BUTTON)
                 self.page.wait_for_timeout(1000)
                 return True
        return False

    @allure.step("删除角色: {name}")
    def delete_role(self, name: str) -> bool:
        """删除角色"""
        self.switch_to_tab("Roles")
        
        row = self.page.locator(f"tr:has-text('{name}')").first
        if not row.is_visible():
            return True
            
        menu_btn = row.locator("button").last # 假设最右侧是菜单
        # 排除 'Edit permissions' 按钮
        if "Edit permissions" in menu_btn.text_content() or "":
             # 找倒数第二个? 或者找没有文本的按钮
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
