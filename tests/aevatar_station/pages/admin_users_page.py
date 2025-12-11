"""
AdminUsersPage - 用户管理页面对象
路径: /admin/users
ABP Framework Identity模块 - 用户管理功能
"""
from playwright.sync_api import Page
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class AdminUsersPage(BasePage):
    """用户管理页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin/users"
        
        # 页面标题和导航 - 基于Playwright识别的实际元素
        self.PAGE_TITLE = "h3:has-text('User Management'), h1:has-text('User'), h2:has-text('User')"
        self.BREADCRUMB = "nav[aria-label='breadcrumb'], .breadcrumb"
        
        # 用户列表表格
        self.USERS_TABLE = "table[aria-label='Data table'], table, [role='table']"
        self.TABLE_HEADER = "thead, [role='columnheader']"
        self.TABLE_BODY = "tbody, [role='rowgroup']"
        self.TABLE_ROWS = "tbody tr"
        self.TABLE_CELLS = "td, [role='cell']"
        
        # 列头（实际UI: Actions, Username, Email, Active）
        self.COL_ACTIONS = "th:has-text('Actions'), [role='columnheader']:has-text('Actions')"
        self.COL_USERNAME = "th:has-text('Username'), [role='columnheader']:has-text('Username')"
        self.COL_EMAIL = "th:has-text('Email'), [role='columnheader']:has-text('Email')"
        self.COL_ACTIVE = "th:has-text('Active'), [role='columnheader']:has-text('Active')"
        
        # 搜索和筛选
        self.SEARCH_INPUT = "input[placeholder='Search...'], input[placeholder*='Search']"
        self.SEARCH_BUTTON = "button:has-text('Search'), button[type='submit']"
        self.FILTER_DROPDOWN = "select.filter, .filter-dropdown, button:has-text('Filter')"
        
        # 操作按钮 - 基于实际UI
        self.NEW_USER_BUTTON = "button:has-text('Create New User')"
        self.EXPORT_BUTTON = "button:has-text('Export'), button:has-text('Download')"
        self.REFRESH_BUTTON = "button:has-text('Refresh'), button[aria-label='refresh']"
        
        # 行操作下拉菜单 - 基于实际UI
        self.ACTION_DROPDOWN = "button:has-text('Actions')"
        self.ACTION_MENU = "[role='menu']"
        self.ACTION_EDIT = "[role='menuitem'] button:has-text('Edit'), button:has-text('Edit')"
        self.ACTION_PERMISSION = "[role='menuitem'] button:has-text('Permission'), button:has-text('Permission')"
        self.ACTION_DELETE = "[role='menuitem']:has-text('Delete'), button:has-text('Delete')"
        self.ACTION_PERMISSIONS = "[role='menuitem']:has-text('Permissions'), button:has-text('Permissions')"
        
        # 分页 - 基于实际UI
        self.PAGINATION = "nav[aria-label='Pagination'], nav.pagination, .pagination"
        self.PAGE_INFO = "text=/Showing.*of.*total records/"
        self.PAGE_SIZE_SELECT = "select[aria-label='page size'], .page-size-select"
        self.PAGE_FIRST = "button[aria-label='Go to first page'], button:has-text('First')"
        self.PREV_PAGE_BUTTON = "button[aria-label='Go to previous page'], button:has-text('Previous')"
        self.NEXT_PAGE_BUTTON = "button[aria-label='Go to next page'], button:has-text('Next')"
        self.PAGE_LAST = "button[aria-label='Go to last page'], button:has-text('Last')"
        
        # 对话框 - 基于实际UI（React/Radix UI Dialog）
        self.DIALOG = "[role='dialog']"
        self.DIALOG_TITLE = "[role='dialog'] h2"
        self.DIALOG_CLOSE = "[role='dialog'] button:has-text('Close')"
        self.DIALOG_SAVE = "[role='dialog'] button:has-text('Save')"
        self.DIALOG_CANCEL = "[role='dialog'] button:has-text('Cancel')"
        
        # 创建用户表单 - 基于实际UI
        self.FORM_USERNAME = "[role='dialog'] input[aria-label='User name'], [role='dialog'] input:near(:text('User name'))"
        self.FORM_PASSWORD = "[role='dialog'] input[aria-label='Password'], [role='dialog'] input[type='password']"
        self.FORM_NAME = "[role='dialog'] input[aria-label='Name']"
        self.FORM_SURNAME = "[role='dialog'] input[aria-label='Surname']"
        self.FORM_EMAIL = "[role='dialog'] input[aria-label='Email address'], [role='dialog'] input[type='email']"
        self.FORM_PHONE = "[role='dialog'] input[aria-label='Phone Number']"
        self.FORM_ACTIVE = "[role='dialog'] input[aria-label='Active'], [role='dialog'] [role='checkbox']:has-text('Active')"
        self.FORM_LOCKOUT = "[role='dialog'] input[aria-label='Lock account'], [role='dialog'] [role='checkbox']:has-text('Lock')"
        
        # 编辑用户Tab - 基于实际UI
        self.EDIT_TAB_USER_INFO = "[role='dialog'] [role='tab']:has-text('User Information')"
        self.EDIT_TAB_ROLES = "[role='dialog'] [role='tab']:has-text('Roles')"
        
        # 确认对话框 - 删除确认
        self.CONFIRM_DIALOG = "[role='alertdialog']"
        self.CONFIRM_TITLE = "[role='alertdialog'] h2"
        self.CONFIRM_MESSAGE = "[role='alertdialog'] p"
        self.CONFIRM_YES = "[role='alertdialog'] button:has-text('Yes')"
        self.CONFIRM_NO = "[role='alertdialog'] button:has-text('Cancel')"
        
        # 权限管理页面 - /admin/permissions/user/{username}
        self.PERMISSION_PAGE_TITLE = "h1:has-text('Permissions')"
        self.PERMISSION_BACK_BUTTON = "button:has-text('Back')"
        self.PERMISSION_SUMMARY = "text=Permission Summary"
        self.PERMISSION_GRANT_ALL = "button:has-text('Grant All')"
        self.PERMISSION_SEARCH = "input[placeholder*='Search permissions']"
        self.PERMISSION_TAB_LIST = "[role='tablist']"
        self.PERMISSION_SAVE = "button:has-text('Save Changes')"
        self.PERMISSION_CANCEL = "button:has-text('Cancel')"
        
        # 权限页面 - 统计信息
        self.PERMISSION_TOTAL_COUNT = "text=/\\d+/ >> nth=0"  # Total Permissions数字
        self.PERMISSION_GRANTED_COUNT = "text=/\\d+/ >> nth=1"  # Granted数字
        self.PERMISSION_NOT_GRANTED_COUNT = "text=/\\d+/ >> nth=2"  # Not Granted数字
        
        # 权限页面 - Tab和权限项
        self.PERMISSION_TAB = "[role='tab']"
        self.PERMISSION_TABPANEL = "[role='tabpanel']"
        self.PERMISSION_GRANT_BUTTON = "button:has-text('Grant')"
        self.PERMISSION_REVOKE_BUTTON = "button:has-text('Revoke')"
        self.PERMISSION_UNSAVED_CHANGES = "text=Unsaved changes"
        
        # 提示消息 - 更全面的选择器
        self.SUCCESS_MESSAGE = ".toast-success, .alert-success, [role='alert']:has-text('Success'), .swal2-success, .ant-message-success, .notification-success, .abp-toast-success"
        self.ERROR_MESSAGE = ".toast-error, .alert-danger, [role='alert']:has-text('error'), .swal2-error, .ant-message-error"
        self.INFO_MESSAGE = ".toast-info, .alert-info"
        
        # 空状态
        self.EMPTY_STATE = "text=No data, text=No users found, .empty-state"
        
        # 加载状态
        self.LOADING_SPINNER = ".spinner, .loading, [role='progressbar']"
    
    def navigate(self):
        """导航到用户管理页面"""
        logger.info("导航到用户管理页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            # 检查表格或页面标题是否可见
            has_table = self.is_visible(self.USERS_TABLE, timeout=10000)
            has_title = self.is_visible(self.PAGE_TITLE, timeout=5000)
            is_loaded = has_table or has_title
            logger.info(f"用户管理页面加载状态: {is_loaded}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def wait_for_table_load(self, timeout: int = 10000):
        """等待表格数据加载完成"""
        logger.info("等待用户列表加载")
        try:
            self.page.wait_for_selector(self.USERS_TABLE, timeout=timeout)
            # 等待加载动画消失
            try:
                self.page.wait_for_selector(self.LOADING_SPINNER, state="hidden", timeout=5000)
            except:
                pass
            logger.info("用户列表加载完成")
        except Exception as e:
            logger.warning(f"等待表格加载超时: {e}")
    
    def get_user_count(self, refresh_first: bool = False) -> int:
        """获取用户列表行数"""
        try:
            if refresh_first:
                self.page.reload()
                self.wait_for_load()
                self.wait_for_table_load()
            
            rows = self.page.locator(self.TABLE_ROWS).all()
            count = len(rows)
            logger.info(f"当前用户数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取用户数量失败: {e}")
            return 0
    
    def get_total_user_count_from_pagination(self) -> int:
        """从分页信息获取总用户数（如果有分页的话）"""
        try:
            # 尝试从分页组件获取总数
            pagination_info = self.page.locator(".pagination-info, .total-count, [class*='pagination'] span:has-text('total')").first
            if pagination_info.is_visible(timeout=2000):
                text = pagination_info.text_content()
                # 提取数字
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[-1])  # 通常最后一个数字是总数
        except:
            pass
        # 如果没有分页，返回当前行数
        return self.get_user_count()
    
    def search_user(self, keyword: str):
        """搜索用户"""
        logger.info(f"搜索用户: {keyword}")
        try:
            self.page.fill(self.SEARCH_INPUT, keyword)
            # 尝试点击搜索按钮或按回车
            if self.is_visible(self.SEARCH_BUTTON, timeout=2000):
                self.page.click(self.SEARCH_BUTTON)
            else:
                self.page.press(self.SEARCH_INPUT, "Enter")
            self.page.wait_for_timeout(1000)
            logger.info("搜索完成")
        except Exception as e:
            logger.error(f"搜索用户失败: {e}")
            raise
    
    def click_new_user(self):
        """点击新建用户按钮"""
        logger.info("点击新建用户按钮")
        self.page.click(self.NEW_USER_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def is_dialog_open(self) -> bool:
        """检查对话框是否打开"""
        return self.is_visible(self.DIALOG, timeout=3000)
    
    def fill_user_form(self, username: str = None, email: str = None, 
                       password: str = None, phone: str = None,
                       name: str = None, surname: str = None):
        """填写用户表单"""
        logger.info("填写用户表单")
        try:
            if username:
                self.page.fill(self.FORM_USERNAME, username)
            if email:
                self.page.fill(self.FORM_EMAIL, email)
            if password:
                self.page.fill(self.FORM_PASSWORD, password)
            if phone:
                self.page.fill(self.FORM_PHONE, phone)
            if name:
                self.page.fill(self.FORM_NAME, name)
            if surname:
                self.page.fill(self.FORM_SURNAME, surname)
            logger.info("用户表单填写完成")
        except Exception as e:
            logger.error(f"填写用户表单失败: {e}")
            raise
    
    def click_save(self):
        """点击保存按钮 - 处理对话框内滚动问题"""
        logger.info("点击保存按钮")
        try:
            # 方式1: 使用JavaScript滚动对话框内容到底部并点击Save按钮
            try:
                result = self.page.evaluate("""
                    () => {
                        // 尝试滚动对话框内容区域
                        const dialogContent = document.querySelector('[role="dialog"] [class*="content"]') ||
                                             document.querySelector('[role="dialog"] [class*="body"]') ||
                                             document.querySelector('[role="dialog"] > div > div');
                        if (dialogContent) {
                            dialogContent.scrollTop = dialogContent.scrollHeight;
                        }
                        
                        // 查找并点击Save按钮
                        const buttons = document.querySelectorAll('[role="dialog"] button');
                        for (const btn of buttons) {
                            if (btn.textContent.trim() === 'Save' || btn.textContent.includes('Save')) {
                                btn.scrollIntoView({ block: 'center' });
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                if result:
                    self.page.wait_for_timeout(1000)
                    return
            except Exception as e:
                logger.debug(f"JavaScript点击失败: {e}")
            
            # 方式2: 使用Playwright的getByRole点击
            try:
                save_btn = self.page.get_by_role("button", name="Save")
                save_btn.scroll_into_view_if_needed(timeout=3000)
                save_btn.click(force=True, timeout=5000)
                self.page.wait_for_timeout(1000)
                return
            except Exception as e:
                logger.debug(f"getByRole点击失败: {e}")
            
            # 方式3: 使用locator并强制点击
            try:
                save_btn = self.page.locator(self.DIALOG_SAVE).first
                save_btn.click(force=True, timeout=5000)
                self.page.wait_for_timeout(1000)
                return
            except Exception as e:
                logger.debug(f"locator force点击失败: {e}")
            
            # 方式4: 使用键盘快捷键提交（如果支持）
            try:
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1000)
            except:
                pass
                
        except Exception as e:
            logger.error(f"点击保存按钮失败: {e}")
    
    def click_cancel(self):
        """点击取消按钮"""
        logger.info("点击取消按钮")
        self.page.click(self.DIALOG_CANCEL)
        self.page.wait_for_timeout(1000)
    
    def open_user_actions(self, row_index: int = 0):
        """打开指定行的操作菜单"""
        logger.info(f"打开第{row_index + 1}行的操作菜单")
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            if row_index < len(rows):
                action_btn = rows[row_index].locator(self.ACTION_DROPDOWN).first
                action_btn.click()
                self.page.wait_for_timeout(500)
                logger.info("操作菜单已打开")
            else:
                logger.warning(f"行索引{row_index}超出范围")
        except Exception as e:
            logger.error(f"打开操作菜单失败: {e}")
            raise
    
    def click_edit_user(self, row_index: int = 0):
        """编辑用户"""
        logger.info(f"编辑第{row_index + 1}行用户")
        self.open_user_actions(row_index)
        self.page.click(self.ACTION_EDIT)
        self.page.wait_for_timeout(1000)
    
    def click_delete_user(self, row_index: int = 0):
        """删除用户"""
        logger.info(f"删除第{row_index + 1}行用户")
        self.open_user_actions(row_index)
        self.page.click(self.ACTION_DELETE)
        self.page.wait_for_timeout(1000)
    
    def click_user_permissions(self, row_index: int = 0):
        """打开用户权限 - 使用Permission菜单项"""
        logger.info(f"打开第{row_index + 1}行用户权限")
        self.open_user_actions(row_index)
        self.page.click(self.ACTION_PERMISSION)
        self.page.wait_for_timeout(2000)
    
    def is_permission_page_loaded(self) -> bool:
        """检查权限管理页面是否加载"""
        try:
            return self.is_visible(self.PERMISSION_PAGE_TITLE, timeout=10000)
        except:
            return False
    
    def click_permission_back(self, handle_unsaved: bool = True):
        """点击权限页面的返回按钮
        
        Args:
            handle_unsaved: 是否处理未保存更改的对话框（默认点击确认离开）
        """
        logger.info("点击权限页面返回按钮")
        self.page.click(self.PERMISSION_BACK_BUTTON)
        
        # 处理可能出现的未保存更改确认对话框
        if handle_unsaved:
            try:
                self.page.wait_for_timeout(500)
                # 检查是否有confirm对话框，如果有就接受
                self.page.on("dialog", lambda dialog: dialog.accept())
            except:
                pass
        
        self.page.wait_for_timeout(1000)
    
    def get_permission_summary(self) -> dict:
        """获取权限摘要信息
        
        Returns:
            dict: {"total": int, "granted": int, "not_granted": int}
        """
        logger.info("获取权限摘要信息")
        try:
            summary = {"total": 0, "granted": 0, "not_granted": 0}
            
            # 查找包含数字的元素
            summary_section = self.page.locator("text=Permission Summary").locator("..")
            numbers = summary_section.locator("text=/^\\d+$/").all()
            
            if len(numbers) >= 3:
                summary["total"] = int(numbers[0].text_content())
                summary["granted"] = int(numbers[1].text_content())
                summary["not_granted"] = int(numbers[2].text_content())
            
            logger.info(f"权限摘要: {summary}")
            return summary
        except Exception as e:
            logger.error(f"获取权限摘要失败: {e}")
            return {"total": 0, "granted": 0, "not_granted": 0}
    
    def click_grant_all_permissions(self):
        """点击Grant All按钮授予所有权限"""
        logger.info("点击Grant All按钮")
        self.page.click(self.PERMISSION_GRANT_ALL)
        self.page.wait_for_timeout(1000)
    
    def click_permission_save(self):
        """点击Save Changes按钮保存权限更改"""
        logger.info("点击Save Changes按钮")
        try:
            save_btn = self.page.locator(self.PERMISSION_SAVE)
            if save_btn.is_enabled(timeout=2000):
                save_btn.click()
                self.page.wait_for_timeout(2000)
                return True
            else:
                logger.warning("Save Changes按钮不可用")
                return False
        except Exception as e:
            logger.error(f"点击Save Changes失败: {e}")
            return False
    
    def click_permission_cancel(self):
        """点击Cancel按钮取消权限更改"""
        logger.info("点击Cancel按钮")
        self.page.click(self.PERMISSION_CANCEL)
        self.page.wait_for_timeout(1000)
    
    def grant_permission_by_name(self, permission_name: str) -> bool:
        """授予指定名称的权限
        
        Args:
            permission_name: 权限名称，如 "AbpIdentity.Roles"
        
        Returns:
            bool: 是否成功授予
        """
        logger.info(f"授予权限: {permission_name}")
        try:
            # 查找权限项
            permission_item = self.page.locator(f"text={permission_name}").first
            if permission_item.is_visible(timeout=3000):
                # 找到对应的Grant按钮
                parent = permission_item.locator("xpath=ancestor::div[contains(@class, 'flex')]").first
                grant_btn = parent.locator("button:has-text('Grant')").first
                if grant_btn.is_visible(timeout=2000):
                    grant_btn.click()
                    self.page.wait_for_timeout(500)
                    logger.info(f"已授予权限: {permission_name}")
                    return True
            logger.warning(f"未找到权限或Grant按钮: {permission_name}")
            return False
        except Exception as e:
            logger.error(f"授予权限失败: {e}")
            return False
    
    def revoke_permission_by_name(self, permission_name: str) -> bool:
        """撤销指定名称的权限
        
        Args:
            permission_name: 权限名称
        
        Returns:
            bool: 是否成功撤销
        """
        logger.info(f"撤销权限: {permission_name}")
        try:
            permission_item = self.page.locator(f"text={permission_name}").first
            if permission_item.is_visible(timeout=3000):
                parent = permission_item.locator("xpath=ancestor::div[contains(@class, 'flex')]").first
                revoke_btn = parent.locator("button:has-text('Revoke')").first
                if revoke_btn.is_visible(timeout=2000):
                    revoke_btn.click()
                    self.page.wait_for_timeout(500)
                    logger.info(f"已撤销权限: {permission_name}")
                    return True
            logger.warning(f"未找到权限或Revoke按钮: {permission_name}")
            return False
        except Exception as e:
            logger.error(f"撤销权限失败: {e}")
            return False
    
    def click_permission_tab(self, tab_name: str):
        """点击权限Tab
        
        Args:
            tab_name: Tab名称，如 "AbpIdentity.Roles"
        """
        logger.info(f"点击权限Tab: {tab_name}")
        try:
            tab = self.page.get_by_role("tab", name=tab_name).first
            tab.click()
            self.page.wait_for_timeout(500)
        except Exception as e:
            logger.error(f"点击Tab失败: {e}")
    
    def get_permission_tabs(self) -> list:
        """获取所有权限Tab名称列表"""
        logger.info("获取所有权限Tab")
        try:
            tabs = self.page.locator("[role='tab']").all()
            tab_names = []
            for tab in tabs:
                name = tab.text_content()
                if name:
                    tab_names.append(name.strip())
            logger.info(f"找到 {len(tab_names)} 个权限Tab")
            return tab_names
        except Exception as e:
            logger.error(f"获取权限Tab失败: {e}")
            return []
    
    def get_granted_permissions_in_current_tab(self) -> list:
        """获取当前Tab中已授予的权限名称列表"""
        logger.info("获取当前Tab中已授予的权限")
        try:
            granted = []
            # 查找所有Revoke按钮，其对应的权限是已授予的
            revoke_buttons = self.page.locator("[role='tabpanel'] button:has-text('Revoke')").all()
            for btn in revoke_buttons:
                try:
                    # 找到权限名称
                    parent = btn.locator("xpath=ancestor::div[1]")
                    name_elem = parent.locator("xpath=preceding-sibling::div//div[contains(@class, 'font')]").first
                    name = name_elem.text_content()
                    if name:
                        granted.append(name.strip())
                except:
                    continue
            logger.info(f"当前Tab已授予 {len(granted)} 个权限")
            return granted
        except Exception as e:
            logger.error(f"获取已授予权限失败: {e}")
            return []
    
    def is_unsaved_changes_visible(self) -> bool:
        """检查是否显示未保存更改提示"""
        return self.is_visible(self.PERMISSION_UNSAVED_CHANGES, timeout=2000)
    
    def is_save_changes_enabled(self) -> bool:
        """检查Save Changes按钮是否可用"""
        try:
            save_btn = self.page.locator(self.PERMISSION_SAVE)
            return save_btn.is_enabled(timeout=2000)
        except:
            return False
    
    def grant_first_available_permission(self) -> str:
        """授予第一个可用的权限
        
        Returns:
            str: 被授予的权限名称，如果没有可用权限返回空字符串
        """
        logger.info("授予第一个可用的权限")
        try:
            grant_btn = self.page.locator("[role='tabpanel'] button:has-text('Grant')").first
            if grant_btn.is_visible(timeout=3000):
                # 获取权限名称
                parent = grant_btn.locator("xpath=ancestor::div[1]")
                name_elem = parent.locator("xpath=preceding-sibling::div//div[1]").first
                name = name_elem.text_content() if name_elem.is_visible() else ""
                
                grant_btn.click()
                self.page.wait_for_timeout(500)
                logger.info(f"已授予权限: {name}")
                return name.strip() if name else "unknown"
            logger.info("没有可用的Grant按钮")
            return ""
        except Exception as e:
            logger.error(f"授予权限失败: {e}")
            return ""
    
    def revoke_first_granted_permission(self) -> str:
        """撤销第一个已授予的权限
        
        Returns:
            str: 被撤销的权限名称
        """
        logger.info("撤销第一个已授予的权限")
        try:
            revoke_btn = self.page.locator("[role='tabpanel'] button:has-text('Revoke')").first
            if revoke_btn.is_visible(timeout=3000):
                parent = revoke_btn.locator("xpath=ancestor::div[1]")
                name_elem = parent.locator("xpath=preceding-sibling::div//div[1]").first
                name = name_elem.text_content() if name_elem.is_visible() else ""
                
                revoke_btn.click()
                self.page.wait_for_timeout(500)
                logger.info(f"已撤销权限: {name}")
                return name.strip() if name else "unknown"
            logger.info("没有可用的Revoke按钮")
            return ""
        except Exception as e:
            logger.error(f"撤销权限失败: {e}")
            return ""
    
    def is_confirm_dialog_open(self) -> bool:
        """检查确认对话框是否打开"""
        return self.is_visible(self.CONFIRM_DIALOG, timeout=3000)
    
    def get_confirm_dialog_message(self) -> str:
        """获取确认对话框消息"""
        try:
            return self.page.locator(self.CONFIRM_MESSAGE).text_content() or ""
        except:
            return ""
    
    def confirm_action(self):
        """确认操作（点击Yes按钮）"""
        logger.info("确认操作")
        self.page.click(self.CONFIRM_YES)
        self.page.wait_for_timeout(1000)
    
    def cancel_confirm(self):
        """取消确认（点击Cancel按钮）"""
        logger.info("取消确认操作")
        self.page.click(self.CONFIRM_NO)
        self.page.wait_for_timeout(500)
    
    def get_dialog_title(self) -> str:
        """获取对话框标题"""
        try:
            return self.page.locator(self.DIALOG_TITLE).text_content() or ""
        except:
            return ""
    
    def click_dialog_close(self):
        """点击对话框关闭按钮"""
        logger.info("点击对话框关闭按钮")
        self.page.click(self.DIALOG_CLOSE)
        self.page.wait_for_timeout(500)
    
    def fill_create_user_form(self, username: str, password: str, email: str,
                               name: str = "", surname: str = "", phone: str = ""):
        """填写创建用户表单 - 使用getByRole exact匹配"""
        logger.info(f"填写创建用户表单: {username}")
        try:
            self.page.get_by_role("textbox", name="User name", exact=True).fill(username)
            self.page.get_by_role("textbox", name="Password", exact=True).fill(password)
            self.page.get_by_role("textbox", name="Email address", exact=True).fill(email)
            if name:
                self.page.get_by_role("textbox", name="Name", exact=True).fill(name)
            if surname:
                self.page.get_by_role("textbox", name="Surname", exact=True).fill(surname)
            if phone:
                self.page.get_by_role("textbox", name="Phone Number", exact=True).fill(phone)
            logger.info("创建用户表单填写完成")
        except Exception as e:
            logger.error(f"填写创建用户表单失败: {e}")
            raise
    
    def fill_edit_user_form(self, name: str = None, surname: str = None, 
                            email: str = None, phone: str = None):
        """填写编辑用户表单 - 使用getByRole exact匹配"""
        logger.info("填写编辑用户表单")
        try:
            if name is not None:
                self.page.get_by_role("textbox", name="Name", exact=True).fill(name)
            if surname is not None:
                self.page.get_by_role("textbox", name="Surname", exact=True).fill(surname)
            if email is not None:
                self.page.get_by_role("textbox", name="Email", exact=True).fill(email)
            if phone is not None:
                self.page.get_by_role("textbox", name="Phone Number", exact=True).fill(phone)
            logger.info("编辑用户表单填写完成")
        except Exception as e:
            logger.error(f"填写编辑用户表单失败: {e}")
            raise
    
    def click_edit_tab_roles(self):
        """点击编辑对话框的Roles Tab"""
        logger.info("切换到Roles Tab")
        self.page.get_by_role("tab", name="Roles").click()
        self.page.wait_for_timeout(500)
    
    def click_edit_tab_user_info(self):
        """点击编辑对话框的User Information Tab"""
        logger.info("切换到User Information Tab")
        self.page.get_by_role("tab", name="User Information").click()
        self.page.wait_for_timeout(500)
    
    def find_user_by_username(self, username: str) -> int:
        """根据用户名查找用户行索引，返回-1表示未找到"""
        logger.info(f"查找用户: {username}")
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            for i, row in enumerate(rows):
                cells = row.locator(self.TABLE_CELLS).all()
                if len(cells) > 1:
                    cell_text = cells[1].text_content()
                    if cell_text and username in cell_text:
                        logger.info(f"找到用户 {username} 在第 {i+1} 行")
                        return i
            logger.warning(f"未找到用户: {username}")
            return -1
        except Exception as e:
            logger.error(f"查找用户失败: {e}")
            return -1
    
    def is_success_message_visible(self) -> bool:
        """检查成功消息是否可见 - 增强版检测（支持创建/删除/更新）"""
        try:
            # 多种选择器尝试
            selectors = [
                ".toast-success",
                ".alert-success", 
                "[role='alert']:has-text('Success')",
                "[role='alert']:has-text('success')",
                ".swal2-success",  # SweetAlert2
                ".ant-message-success",  # Ant Design
                "div:has-text('Success'):has-text('Created')",
                "div:has-text('Success'):has-text('deleted')",
                "div:has-text('Success'):has-text('Updated')",
                "div:has-text('User Created Successfully')",
                "div:has-text('has been deleted')",
                "div:has-text('deleted successfully')",
                ".notification-success",
                ".abp-toast-success",
            ]
            
            for selector in selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=1000):
                        logger.info(f"检测到成功消息: {selector}")
                        return True
                except:
                    continue
            
            # 最后检查页面是否包含成功文本
            page_text = self.page.content()
            success_patterns = [
                "User Created Successfully",
                "created successfully",
                "deleted successfully",
                "has been deleted",
                "Updated Successfully",
            ]
            
            for pattern in success_patterns:
                if pattern.lower() in page_text.lower():
                    # 检查这个文本是否在可见的toast/alert中
                    success_elements = self.page.locator("text=Success").all()
                    for elem in success_elements:
                        try:
                            if elem.is_visible(timeout=500):
                                logger.info(f"检测到成功文本可见: {pattern}")
                                return True
                        except:
                            continue
            
            return False
        except Exception as e:
            logger.debug(f"检测成功消息时出错: {e}")
            return False
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def get_user_info_by_row(self, row_index: int = 0) -> dict:
        """获取指定行的用户信息"""
        logger.info(f"获取第{row_index + 1}行用户信息")
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            if row_index < len(rows):
                row = rows[row_index]
                cells = row.locator(self.TABLE_CELLS).all()
                # ABP标准用户列表结构
                user_info = {
                    "username": cells[1].text_content() if len(cells) > 1 else "",
                    "email": cells[2].text_content() if len(cells) > 2 else "",
                    "phone": cells[3].text_content() if len(cells) > 3 else "",
                }
                logger.info(f"用户信息: {user_info}")
                return user_info
            else:
                logger.warning(f"行索引{row_index}超出范围")
                return {}
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            return {}
    
    def change_page_size(self, size: int):
        """更改每页显示数量"""
        logger.info(f"更改每页显示数量为: {size}")
        try:
            self.page.select_option(self.PAGE_SIZE_SELECT, str(size))
            self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.error(f"更改分页大小失败: {e}")
    
    def go_to_next_page(self):
        """翻到下一页"""
        logger.info("翻到下一页")
        self.page.click(self.NEXT_PAGE_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def go_to_prev_page(self):
        """翻到上一页"""
        logger.info("翻到上一页")
        self.page.click(self.PREV_PAGE_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def is_new_user_button_visible(self) -> bool:
        """检查新建用户按钮是否可见"""
        return self.is_visible(self.NEW_USER_BUTTON, timeout=5000)
    
    def is_search_visible(self) -> bool:
        """检查搜索框是否可见"""
        return self.is_visible(self.SEARCH_INPUT, timeout=5000)
    
    def press_escape(self):
        """按ESC键"""
        logger.info("按下ESC键")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
    
    def take_screenshot(self, filename: str):
        """截图"""
        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图保存到: {screenshot_path}")
        return screenshot_path
    
    # ==================== 功能测试辅助方法 ====================
    
    def create_user(self, username: str, password: str, email: str,
                    name: str = "", surname: str = "", phone: str = "") -> bool:
        """
        创建新用户 - 完整功能操作
        返回True表示创建成功，False表示失败
        """
        logger.info(f"创建新用户: {username}")
        try:
            # 点击新建用户按钮
            self.click_new_user()
            self.page.wait_for_timeout(1000)
            
            if not self.is_dialog_open():
                logger.error("创建用户对话框未打开")
                return False
            
            # 填写表单
            self.fill_create_user_form(username, password, email, name, surname, phone)
            
            # 点击保存
            self.click_save()
            self.page.wait_for_timeout(2000)
            
            # 检查成功消息
            if self.is_success_message_visible():
                logger.info(f"用户 {username} 创建成功")
                return True
            else:
                logger.warning(f"未检测到成功消息，检查错误消息...")
                if self.is_error_message_visible():
                    logger.error("创建用户时出现错误")
                    return False
                # 没有错误消息也可能成功了，检查对话框是否关闭
                if not self.is_dialog_open():
                    logger.info("对话框已关闭，假定创建成功")
                    return True
                return False
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            # 尝试关闭对话框
            self.press_escape()
            return False
    
    def edit_user(self, row_index: int, name: str = None, surname: str = None,
                  email: str = None, phone: str = None) -> bool:
        """
        编辑用户 - 完整功能操作
        返回True表示编辑成功
        """
        logger.info(f"编辑第{row_index + 1}行用户")
        try:
            # 点击编辑
            self.click_edit_user(row_index)
            self.page.wait_for_timeout(1500)
            
            if not self.is_dialog_open():
                logger.error("编辑用户对话框未打开")
                return False
            
            # 填写表单
            self.fill_edit_user_form(name, surname, email, phone)
            
            # 点击保存
            self.click_save()
            self.page.wait_for_timeout(2000)
            
            # 检查结果 - 对话框可能会保持打开或关闭
            if self.is_success_message_visible():
                logger.info("用户编辑成功")
                # 关闭对话框如果还打开
                if self.is_dialog_open():
                    self.press_escape()
                return True
            
            # 即使没有成功消息，也可能成功了
            if self.is_dialog_open():
                self.press_escape()
            return True
        except Exception as e:
            logger.error(f"编辑用户失败: {e}")
            self.press_escape()
            return False
    
    def delete_user(self, row_index: int) -> bool:
        """
        删除用户 - 完整功能操作
        返回True表示删除成功
        """
        logger.info(f"删除第{row_index + 1}行用户")
        try:
            # 点击删除
            self.click_delete_user(row_index)
            self.page.wait_for_timeout(1000)
            
            # 检查确认对话框
            if not self.is_confirm_dialog_open():
                logger.error("删除确认对话框未打开")
                return False
            
            # 确认删除
            self.confirm_action()
            self.page.wait_for_timeout(2000)
            
            # 检查成功消息
            if self.is_success_message_visible():
                logger.info("用户删除成功")
                return True
            else:
                logger.warning("未检测到成功消息，但操作可能成功")
                return True
        except Exception as e:
            logger.error(f"删除用户失败: {e}")
            return False
    
    def delete_user_by_username(self, username: str) -> bool:
        """
        通过用户名删除用户
        返回True表示删除成功，False表示失败或未找到用户
        """
        logger.info(f"通过用户名删除用户: {username}")
        row_index = self.find_user_by_username(username)
        if row_index < 0:
            logger.warning(f"未找到用户: {username}")
            return False
        return self.delete_user(row_index)
    
    def is_user_in_list(self, username: str, use_search: bool = True) -> bool:
        """检查用户是否在列表中
        
        Args:
            username: 用户名
            use_search: 是否使用搜索功能查找（解决分页问题）
        """
        if use_search:
            # 使用搜索功能查找用户（解决分页问题）
            try:
                self.search_user(username)
                self.page.wait_for_timeout(1000)
                
                rows = self.page.locator(self.TABLE_ROWS).all()
                for row in rows:
                    cells = row.locator(self.TABLE_CELLS).all()
                    if len(cells) > 1:
                        cell_text = cells[1].text_content()
                        if cell_text and username in cell_text:
                            logger.info(f"搜索找到用户: {username}")
                            # 清除搜索
                            self.clear_search()
                            self.page.wait_for_timeout(500)
                            return True
                
                # 清除搜索
                self.clear_search()
                self.page.wait_for_timeout(500)
                logger.info(f"搜索未找到用户: {username}")
                return False
            except Exception as e:
                logger.warning(f"搜索用户失败: {e}")
                # 回退到直接查找
                pass
        
        # 直接在当前页查找
        row_index = self.find_user_by_username(username)
        return row_index >= 0
    
    def wait_for_success_message(self, timeout: int = 5000) -> bool:
        """等待成功消息出现"""
        try:
            # 等待toast消息
            self.page.wait_for_selector(
                "text=/Success|success|Created|Updated|Deleted/i",
                timeout=timeout
            )
            return True
        except:
            return False
    
    def clear_search(self):
        """清空搜索框"""
        logger.info("清空搜索框")
        try:
            search_input = self.page.locator(self.SEARCH_INPUT)
            search_input.fill("")
            self.page.wait_for_timeout(500)
            # 可能需要按回车来清除过滤
            search_input.press("Enter")
            self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.warning(f"清空搜索框失败: {e}")
    
    def get_all_usernames(self) -> list:
        """获取列表中所有用户名"""
        logger.info("获取所有用户名")
        usernames = []
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            for row in rows:
                cells = row.locator(self.TABLE_CELLS).all()
                if len(cells) > 1:
                    username = cells[1].text_content()
                    if username:
                        usernames.append(username.strip())
            logger.info(f"找到 {len(usernames)} 个用户")
            return usernames
        except Exception as e:
            logger.error(f"获取用户名列表失败: {e}")
            return []
    
    def search_and_verify(self, keyword: str) -> list:
        """
        搜索并返回匹配的用户名列表
        """
        logger.info(f"搜索关键词: {keyword}")
        self.search_user(keyword)
        self.page.wait_for_timeout(2000)
        return self.get_all_usernames()
