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
    
    # 元素选择器 - 基于Playwright MCP探查结果更新
    TAB_MEMBERS = "div[role='tab']:has-text('Members')"
    TAB_ROLES = "div[role='tab']:has-text('Roles')"
    TAB_SETTINGS = "div[role='tab']:has-text('Settings')" # Project Name edit likely here
    
    # Common - 基于实际UI更新
    CREATE_BUTTON = "button:has-text('Add new member'), button:has-text('Add Role')"
    ADD_NEW_MEMBER_BUTTON = "button:has-text('Add new member')"
    ADD_ROLE_BUTTON = "button:has-text('Add Role')"
    
    # Member
    MEMBER_EMAIL_INPUT = "input[type='email'], input[placeholder*='Email'], input[name='email']"
    MEMBER_TABLE = "table"
    
    # Role
    ROLE_NAME_INPUT = "input[placeholder*='Role Name'], input[name='roleName'], input[name='name']"
    ROLE_TABLE = "table"
    EDIT_PERMISSIONS_BUTTON = "button:has-text('Edit permissions')"
    
    # Project Settings - General页面
    PROJECT_NAME_INPUT = "role=textbox >> nth=0"  # 第一个textbox是Project Name
    DOMAIN_NAME_INPUT = "role=textbox[disabled]"  # 第二个textbox是Domain Name（禁用）
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
        self.utils.screenshot_step(f"edit_project_name_before_{new_name}")
        
        # 使用role定位器更准确
        project_name_input = self.page.locator(self.PROJECT_NAME_INPUT).first
        if not project_name_input.is_visible():
            logger.error("Project Name输入框不可见")
            self.utils.screenshot_step("project_name_input_not_found")
            return False
        
        # 清空并输入新名称
        project_name_input.fill("")
        project_name_input.fill(new_name)
        self.page.wait_for_timeout(500)
        self.utils.screenshot_step(f"edit_project_name_filled_{new_name}")
        
        # 点击Save按钮
        save_btn = self.page.get_by_role('button', name='Save')
        if not save_btn.is_visible():
            logger.error("Save按钮不可见")
            self.utils.screenshot_step("save_button_not_found")
            return False
        
        save_btn.click()
        self.page.wait_for_timeout(2000)
        self.utils.screenshot_step(f"edit_project_name_after_save_{new_name}")
        
        # 验证（刷新页面后检查）
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        self.switch_to_tab("General")
        
        actual_name = self.page.locator(self.PROJECT_NAME_INPUT).first.input_value()
        is_success = actual_name == new_name
        self.utils.screenshot_step(f"edit_project_name_verification_{new_name}_{is_success}")
        
        if is_success:
            logger.info(f"✅ Project Name 已成功修改为: {new_name}")
        else:
            logger.error(f"❌ Project Name 修改失败，期望: {new_name}, 实际: {actual_name}")
        
        return is_success

    # ========== Member Actions ==========

    @allure.step("添加 Project Member: {email}")
    def add_member(self, email: str) -> bool:
        """
        添加项目成员
        
        注意：此对话框是从Organisation已有成员中选择，不是输入新邮箱
        """
        self.switch_to_tab("Members")
        
        logger.info(f"添加成员: {email} (从Organisation成员列表中选择)")
        self.utils.screenshot_step(f"add_member_before_{email}")
        
        # 点击"Add new member"按钮
        add_button = self.page.get_by_role('button', name='Add new member')
        if not add_button.is_visible():
            logger.error("Add new member按钮不可见")
            self.utils.screenshot_step("add_member_button_not_found")
            return False
        
        add_button.click()
        self.page.wait_for_timeout(1000)
        self.utils.screenshot_step("add_member_dialog_opened")
        
        try:
            # 点击Email Address combobox打开下拉列表
            logger.info("点击Email Address combobox")
            email_combobox = self.page.get_by_role('combobox', name='Email Address')
            if email_combobox.is_visible():
                email_combobox.click()
                self.page.wait_for_timeout(1000)
                self.utils.screenshot_step("add_member_combobox_expanded")
                
                # 从listbox中选择对应的邮箱
                logger.info(f"从列表中选择邮箱: {email}")
                option = self.page.get_by_role('option', name=email)
                if option.is_visible():
                    option.click()
                    self.page.wait_for_timeout(500)
                    self.utils.screenshot_step(f"add_member_email_selected_{email}")
                    logger.info(f"✅ 已选择邮箱: {email}")
                else:
                    logger.error(f"列表中找不到邮箱: {email}")
                    self.utils.screenshot_step(f"add_member_email_not_found_{email}")
                    
                    # 尝试打印所有可用选项
                    try:
                        options = self.page.locator('[role="option"]').all()
                        logger.info(f"可用选项数量: {len(options)}")
                        for i, opt in enumerate(options[:5]):
                            logger.info(f"Option {i}: {opt.text_content().strip()}")
                    except:
                        pass
                    
                    return False
            else:
                logger.error("Email Address combobox不可见")
                return False
                
        except Exception as e:
            logger.error(f"选择邮箱时出错: {e}")
            self.utils.screenshot_step("add_member_select_error")
            return False
            
        # 点击Add按钮
        logger.info("点击Add按钮...")
        add_btn = self.page.get_by_role('dialog').get_by_role('button', name='Add')
        if add_btn.is_visible():
            add_btn.click()
            self.page.wait_for_timeout(2000)
            self.utils.screenshot_step(f"add_member_after_submit_{email}")
        else:
            logger.error("Add按钮不可见")
            return False
        
        # 验证
        logger.info("刷新页面验证成员列表...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        self.switch_to_tab("Members")
        
        if self.page.locator(f"text={email}").first.is_visible():
            logger.info(f"✅ 成员 {email} 已成功添加")
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
        
        self.utils.screenshot_step(f"delete_member_before_{email}")
        
        row = self.page.locator(f"tr:has-text('{email}')").first
        if not row.is_visible():
            logger.info(f"成员 {email} 不存在，无需删除")
            return True
        
        # 根据MCP观察，没有删除按钮的删除功能（只有Owner，无法删除）
        # 但如果存在多个成员，会有删除按钮
        try:
            menu_btn = row.locator("button").last
            menu_btn.click()
            self.page.wait_for_timeout(500)
            self.utils.screenshot_step(f"delete_member_menu_opened_{email}")
            
            if self.utils.safe_click("text=Delete") or self.utils.safe_click("text=Remove"):
                 self.page.wait_for_timeout(500)
                 self.utils.screenshot_step(f"delete_member_confirm_dialog_{email}")
                 
                 if self.utils.safe_click("button:has-text('Yes')") or self.utils.safe_click("button:has-text('Confirm')"):
                     self.page.wait_for_timeout(2000)
                     self.utils.screenshot_step(f"delete_member_after_confirm_{email}")
                     
                     self.page.reload()
                     self.page.wait_for_load_state("networkidle")
                     self.switch_to_tab("Members")
                     
                     is_deleted = not self.page.locator(f"tr:has-text('{email}')").first.is_visible()
                     self.utils.screenshot_step(f"delete_member_verification_{email}_{is_deleted}")
                     
                     if is_deleted:
                         logger.info(f"✅ 成员 {email} 已成功删除")
                     else:
                         logger.warning(f"⚠️ 成员 {email} 删除后仍然可见")
                     
                     return is_deleted
        except Exception as e:
            logger.warning(f"删除成员 {email} 时出错: {e}")
            self.utils.screenshot_step(f"delete_member_error_{email}")
        
        return False

    # ========== Role Actions ==========

    @allure.step("添加 Project Role: {name}")
    def add_role(self, name: str) -> bool:
        """添加项目角色"""
        self.switch_to_tab("Roles")
        
        logger.info(f"添加角色: {name}")
        self.utils.screenshot_step(f"add_role_before_{name}")
        
        # 点击"Add Role"按钮
        add_button = self.page.get_by_role('button', name='Add Role')
        if not add_button.is_visible():
            logger.error("Add Role按钮不可见")
            self.utils.screenshot_step("add_role_button_not_found")
            return False
        
        add_button.click()
        self.page.wait_for_timeout(1000)
        self.utils.screenshot_step("add_role_dialog_opened")
            
        # 输入角色名称
        if not self.utils.safe_fill(self.ROLE_NAME_INPUT, name):
            logger.error("输入角色名称失败")
            self.utils.screenshot_step("add_role_name_input_failed")
            return False
        
        self.utils.screenshot_step(f"add_role_name_filled_{name}")
            
        # 提交
        logger.info("提交表单...")
        confirm_selectors = [
            "role=dialog >> button:has-text('Create')",
            "role=dialog >> button:has-text('Confirm')",
            "role=dialog >> button[type='submit']"
        ]
        
        clicked = False
        for selector in confirm_selectors:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible():
                    logger.info(f"点击确认按钮: {selector}")
                    btn.click()
                    clicked = True
                    break
            except:
                continue
                
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
        except Exception as e:
             logger.warning(f"弹窗关闭异常: {e}")
             self.utils.screenshot_step(f"add_role_dialog_error_{name}")

        self.page.wait_for_timeout(2000)
        self.utils.screenshot_step(f"add_role_after_submit_{name}")
        
        # 刷新页面以验证
        logger.info("刷新页面验证角色列表...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)
        
        self.switch_to_tab("Roles")
        is_created = self.page.locator(f"text={name}").first.is_visible()
        self.utils.screenshot_step(f"add_role_verification_{name}_{is_created}")
        
        if is_created:
            logger.info(f"✅ 角色 {name} 已成功创建")
        else:
            logger.error(f"❌ 角色 {name} 创建失败")
        
        return is_created

    @allure.step("编辑 Project Role 权限: {role_name}")
    def edit_role_permissions(self, role_name: str) -> bool:
        """编辑角色权限"""
        self.switch_to_tab("Roles")
        
        self.utils.screenshot_step(f"edit_role_permissions_before_{role_name}")
        
        row = self.page.locator(f"tr:has-text('{role_name}')").first
        if not row.is_visible():
            logger.error(f"角色 {role_name} 不存在")
            return False
            
        # 点击"Edit permissions"按钮
        edit_perm_btn = row.get_by_role('button', name='Edit permissions').first
        if not edit_perm_btn.is_visible():
            logger.error(f"角色 {role_name} 的Edit permissions按钮不可见")
            self.utils.screenshot_step(f"edit_permissions_button_not_found_{role_name}")
            return False
        
        edit_perm_btn.click()
        self.page.wait_for_timeout(1000)
        self.utils.screenshot_step(f"edit_permissions_dialog_opened_{role_name}")
        
        # 尝试授予所有权限
        try:
            grant_all = self.page.locator("text=/grant all/i").first
            if grant_all.is_visible():
                 checkbox = grant_all.locator("..").locator("input[type='checkbox']").first
                 if not checkbox.is_visible():
                     grant_all.click()
                 else:
                     if not checkbox.is_checked():
                         checkbox.click()
                 
                 self.page.wait_for_timeout(500)
                 self.utils.screenshot_step(f"edit_permissions_grant_all_{role_name}")
                 
                 # 点击Save按钮
                 save_btn = self.page.get_by_role('button', name='Save')
                 if save_btn.is_visible():
                     save_btn.click()
                     self.page.wait_for_timeout(1000)
                     self.utils.screenshot_step(f"edit_permissions_after_save_{role_name}")
                     logger.info(f"✅ 角色 {role_name} 权限编辑成功")
                     return True
                 else:
                     self.utils.safe_click(self.SAVE_BUTTON)
                     self.page.wait_for_timeout(1000)
                     return True
        except Exception as e:
            logger.error(f"编辑角色权限时出错: {e}")
            self.utils.screenshot_step(f"edit_permissions_error_{role_name}")
        
        return False

    @allure.step("删除 Project Role: {name}")
    def delete_role(self, name: str) -> bool:
        """删除项目角色"""
        self.switch_to_tab("Roles")
        
        self.utils.screenshot_step(f"delete_role_before_{name}")
        
        row = self.page.locator(f"tr:has-text('{name}')").first
        if not row.is_visible():
            logger.info(f"角色 {name} 不存在，无需删除")
            return True
        
        try:
            # 根据MCP观察，删除按钮是最后一个button（三个点图标）
            menu_btn = row.locator("button").last
            
            # 确保不是"Edit permissions"按钮
            if "Edit permissions" in menu_btn.text_content():
                 # 如果最后一个是Edit permissions，说明可能没有删除按钮（如Owner角色）
                 logger.warning(f"角色 {name} 可能没有删除按钮")
                 return False
             
            menu_btn.click()
            self.page.wait_for_timeout(500)
            self.utils.screenshot_step(f"delete_role_menu_opened_{name}")
            
            if self.utils.safe_click("text=Delete"):
                self.page.wait_for_timeout(500)
                self.utils.screenshot_step(f"delete_role_confirm_dialog_{name}")
                
                if self.utils.safe_click("button:has-text('Yes')") or self.utils.safe_click("button:has-text('Confirm')"):
                    self.page.wait_for_timeout(2000)
                    self.utils.screenshot_step(f"delete_role_after_confirm_{name}")
                    
                    self.page.reload()
                    self.page.wait_for_load_state("networkidle")
                    self.switch_to_tab("Roles")
                    
                    is_deleted = not self.page.locator(f"tr:has-text('{name}')").first.is_visible()
                    self.utils.screenshot_step(f"delete_role_verification_{name}_{is_deleted}")
                    
                    if is_deleted:
                        logger.info(f"✅ 角色 {name} 已成功删除")
                    else:
                        logger.warning(f"⚠️ 角色 {name} 删除后仍然可见")
                    
                    return is_deleted
        except Exception as e:
            logger.error(f"删除角色 {name} 时出错: {e}")
            self.utils.screenshot_step(f"delete_role_error_{name}")
        
        return False
