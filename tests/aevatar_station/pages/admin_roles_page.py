"""
AdminRolesPage - 角色管理页面对象
路径: /admin/users/roles
ABP Framework Identity模块 - 角色管理功能
"""
from playwright.sync_api import Page
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class AdminRolesPage(BasePage):
    """角色管理页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin/users/roles"
        
        # 页面标题和导航 - 基于Playwright识别的实际元素
        self.PAGE_TITLE = "h3:has-text('Role Management'), h1:has-text('Role'), h2:has-text('Role')"
        self.BREADCRUMB = "nav[aria-label='breadcrumb'], .breadcrumb"
        
        # 导航链接（侧边栏）
        self.NAV_USERS = "a[href='/admin/users']:has-text('Users')"
        self.NAV_ROLES = "a[href='/admin/users/roles']:has-text('Roles')"
        
        # 角色列表表格 - 基于实际UI
        self.ROLES_TABLE = "table[aria-label='Data table'], table, [role='table']"
        self.TABLE_HEADER = "thead, [role='columnheader']"
        self.TABLE_BODY = "tbody, [role='rowgroup']"
        self.TABLE_ROWS = "tbody tr"
        self.TABLE_CELLS = "td, [role='cell']"
        
        # 列头（实际UI: Actions, Name, Is Default, Is Public）
        self.COL_ACTIONS = "th:has-text('Actions'), [role='columnheader']:has-text('Actions')"
        self.COL_NAME = "th:has-text('Name'), [role='columnheader']:has-text('Name')"
        self.COL_IS_DEFAULT = "th:has-text('Is Default'), [role='columnheader']:has-text('Is Default')"
        self.COL_IS_PUBLIC = "th:has-text('Is Public'), [role='columnheader']:has-text('Is Public')"
        
        # 搜索和筛选
        self.SEARCH_INPUT = "input[placeholder='Search...'], input[placeholder*='Search']"
        self.SEARCH_BUTTON = "button:has-text('Search'), button[type='submit']"
        
        # 操作按钮 - 基于实际UI
        self.NEW_ROLE_BUTTON = "button:has-text('Create New Role')"
        self.EXPORT_BUTTON = "button:has-text('Export')"
        self.REFRESH_BUTTON = "button:has-text('Refresh')"
        
        # 行操作下拉菜单 - 基于实际UI（Permission, Edit）
        self.ACTION_DROPDOWN = "button:has-text('Actions')"
        self.ACTION_MENU = "[role='menu']"
        self.ACTION_EDIT = "[role='menuitem'] button:has-text('Edit'), button:has-text('Edit')"
        self.ACTION_PERMISSION = "[role='menuitem'] button:has-text('Permission'), button:has-text('Permission')"
        self.ACTION_DELETE = "[role='menuitem']:has-text('Delete'), button:has-text('Delete')"
        self.ACTION_PERMISSIONS = "[role='menuitem'] button:has-text('Permission'), button:has-text('Permission')"
        
        # 对话框 - 基于实际UI（React/Radix UI Dialog）
        self.DIALOG = "[role='dialog']"
        self.DIALOG_TITLE = "[role='dialog'] h2"
        self.DIALOG_CLOSE = "[role='dialog'] button:has-text('Close')"
        self.DIALOG_SAVE = "[role='dialog'] button:has-text('Save')"
        self.DIALOG_CANCEL = "[role='dialog'] button:has-text('Cancel')"
        
        # 创建角色表单 - 基于实际UI
        self.FORM_ROLE_NAME = "[role='dialog'] input[aria-label='Role Name']"
        self.FORM_IS_DEFAULT = "[role='dialog'] [role='checkbox']:has-text('Is Default')"
        self.FORM_IS_PUBLIC = "[role='dialog'] [role='checkbox']:has-text('Is Public')"
        
        # 权限对话框 - 基于实际UI
        self.PERMISSIONS_DIALOG = "[role='dialog']:has-text('Permission'), [role='dialog']:has-text('Permissions')"
        self.PERMISSIONS_TREE = ".permission-tree, [role='tree']"
        self.PERMISSION_CHECKBOX = "input[type='checkbox']"
        self.PERMISSION_ITEM = ".permission-item, [role='treeitem']"
        self.SELECT_ALL_PERMISSIONS = "button:has-text('Select all')"
        self.GRANT_ALL = "button:has-text('Grant all')"
        
        # 分页 - 基于实际UI
        self.PAGINATION = "nav[aria-label='Pagination'], nav.pagination, .pagination"
        self.PAGE_INFO = "text=/Showing.*of.*total records/"
        self.PAGE_FIRST = "button[aria-label='Go to first page'], button:has-text('First')"
        self.PAGE_PREV = "button[aria-label='Go to previous page'], button:has-text('Previous')"
        self.PAGE_NEXT = "button[aria-label='Go to next page'], button:has-text('Next')"
        self.PAGE_LAST = "button[aria-label='Go to last page'], button:has-text('Last')"
        
        # 确认对话框
        self.CONFIRM_DIALOG = "[role='alertdialog'], .confirm-dialog"
        self.CONFIRM_YES = "button:has-text('Yes'), button:has-text('Confirm')"
        self.CONFIRM_NO = "button:has-text('No'), button:has-text('Cancel')"
        
        # 提示消息
        self.SUCCESS_MESSAGE = ".toast-success, .alert-success, [role='alert']:has-text('success')"
        self.ERROR_MESSAGE = ".toast-error, .alert-danger, [role='alert']:has-text('error')"
        
        # 空状态
        self.EMPTY_STATE = "text=No data, text=No roles found, .empty-state"
        
        # 加载状态
        self.LOADING_SPINNER = ".spinner, .loading, [role='progressbar']"
        
        # 默认/公开角色标签
        self.DEFAULT_BADGE = ".badge:has-text('Default'), span:has-text('Default')"
        self.PUBLIC_BADGE = ".badge:has-text('Public'), span:has-text('Public')"
    
    def navigate(self):
        """导航到角色管理页面"""
        logger.info("导航到角色管理页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            has_table = self.is_visible(self.ROLES_TABLE, timeout=10000)
            has_title = self.is_visible(self.PAGE_TITLE, timeout=5000)
            is_loaded = has_table or has_title
            logger.info(f"角色管理页面加载状态: {is_loaded}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def wait_for_table_load(self, timeout: int = 10000):
        """等待表格数据加载完成"""
        logger.info("等待角色列表加载")
        try:
            self.page.wait_for_selector(self.ROLES_TABLE, timeout=timeout)
            try:
                self.page.wait_for_selector(self.LOADING_SPINNER, state="hidden", timeout=5000)
            except:
                pass
            logger.info("角色列表加载完成")
        except Exception as e:
            logger.warning(f"等待表格加载超时: {e}")
    
    def click_users_tab(self):
        """点击Users Tab"""
        logger.info("点击Users Tab")
        self.page.click(self.USERS_TAB)
        self.page.wait_for_timeout(1000)
    
    def click_roles_tab(self):
        """点击Roles Tab"""
        logger.info("点击Roles Tab")
        self.page.click(self.ROLES_TAB)
        self.page.wait_for_timeout(1000)
    
    def get_role_count(self) -> int:
        """获取角色列表行数"""
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            count = len(rows)
            logger.info(f"当前角色数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取角色数量失败: {e}")
            return 0
    
    def search_role(self, keyword: str):
        """搜索角色"""
        logger.info(f"搜索角色: {keyword}")
        try:
            self.page.fill(self.SEARCH_INPUT, keyword)
            if self.is_visible(self.SEARCH_BUTTON, timeout=2000):
                self.page.click(self.SEARCH_BUTTON)
            else:
                self.page.press(self.SEARCH_INPUT, "Enter")
            self.page.wait_for_timeout(1000)
            logger.info("搜索完成")
        except Exception as e:
            logger.error(f"搜索角色失败: {e}")
            raise
    
    def click_new_role(self):
        """点击新建角色按钮"""
        logger.info("点击新建角色按钮")
        self.page.click(self.NEW_ROLE_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def is_dialog_open(self) -> bool:
        """检查对话框是否打开"""
        return self.is_visible(self.DIALOG, timeout=3000)
    
    def fill_role_form(self, name: str, is_default: bool = False, is_public: bool = False):
        """填写角色表单"""
        logger.info(f"填写角色表单: name={name}, is_default={is_default}, is_public={is_public}")
        try:
            self.page.fill(self.FORM_ROLE_NAME, name)
            
            default_checkbox = self.page.locator(self.FORM_IS_DEFAULT)
            if default_checkbox.is_visible():
                if is_default:
                    default_checkbox.check()
                else:
                    default_checkbox.uncheck()
            
            public_checkbox = self.page.locator(self.FORM_IS_PUBLIC)
            if public_checkbox.is_visible():
                if is_public:
                    public_checkbox.check()
                else:
                    public_checkbox.uncheck()
                    
            logger.info("角色表单填写完成")
        except Exception as e:
            logger.error(f"填写角色表单失败: {e}")
            raise
    
    def click_save(self):
        """点击保存按钮"""
        logger.info("点击保存按钮")
        self.page.click(self.DIALOG_SAVE)
        self.page.wait_for_timeout(1000)
    
    def click_cancel(self):
        """点击取消按钮"""
        logger.info("点击取消按钮")
        self.page.click(self.DIALOG_CANCEL)
        self.page.wait_for_timeout(1000)
    
    def open_role_actions(self, row_index: int = 0):
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
    
    def click_edit_role(self, row_index: int = 0):
        """编辑角色"""
        logger.info(f"编辑第{row_index + 1}行角色")
        self.open_role_actions(row_index)
        self.page.click(self.ACTION_EDIT)
        self.page.wait_for_timeout(1000)
    
    def click_delete_role(self, row_index: int = 0):
        """删除角色"""
        logger.info(f"删除第{row_index + 1}行角色")
        self.open_role_actions(row_index)
        self.page.click(self.ACTION_DELETE)
        self.page.wait_for_timeout(1000)
    
    def click_role_permissions(self, row_index: int = 0):
        """打开角色权限"""
        logger.info(f"打开第{row_index + 1}行角色权限")
        self.open_role_actions(row_index)
        self.page.click(self.ACTION_PERMISSIONS)
        self.page.wait_for_timeout(1000)
    
    def is_permissions_dialog_open(self) -> bool:
        """检查权限对话框是否打开"""
        return self.is_visible(self.PERMISSIONS_DIALOG, timeout=5000)
    
    def get_permission_count(self) -> int:
        """获取权限数量"""
        try:
            checkboxes = self.page.locator(f"{self.PERMISSIONS_DIALOG} {self.PERMISSION_CHECKBOX}").all()
            return len(checkboxes)
        except Exception as e:
            logger.error(f"获取权限数量失败: {e}")
            return 0
    
    def toggle_permission(self, index: int = 0):
        """切换权限"""
        logger.info(f"切换权限 #{index}")
        try:
            checkboxes = self.page.locator(f"{self.PERMISSIONS_DIALOG} {self.PERMISSION_CHECKBOX}").all()
            if index < len(checkboxes):
                checkboxes[index].click()
                self.page.wait_for_timeout(300)
        except Exception as e:
            logger.error(f"切换权限失败: {e}")
            raise
    
    def click_select_all_permissions(self):
        """点击全选权限"""
        logger.info("点击全选权限")
        self.page.click(self.SELECT_ALL_PERMISSIONS)
        self.page.wait_for_timeout(500)
    
    def confirm_action(self):
        """确认操作"""
        logger.info("确认操作")
        self.page.click(self.CONFIRM_YES)
        self.page.wait_for_timeout(1000)
    
    def cancel_confirm(self):
        """取消确认"""
        logger.info("取消确认操作")
        self.page.click(self.CONFIRM_NO)
        self.page.wait_for_timeout(500)
    
    def is_success_message_visible(self) -> bool:
        """检查成功消息是否可见"""
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5000)
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def get_role_info_by_row(self, row_index: int = 0) -> dict:
        """获取指定行的角色信息"""
        logger.info(f"获取第{row_index + 1}行角色信息")
        try:
            rows = self.page.locator(self.TABLE_ROWS).all()
            if row_index < len(rows):
                row = rows[row_index]
                cells = row.locator(self.TABLE_CELLS).all()
                role_info = {
                    "name": cells[1].text_content() if len(cells) > 1 else "",
                }
                # 检查是否有默认/公开标签
                role_info["is_default"] = row.locator(self.DEFAULT_BADGE).count() > 0
                role_info["is_public"] = row.locator(self.PUBLIC_BADGE).count() > 0
                logger.info(f"角色信息: {role_info}")
                return role_info
            else:
                logger.warning(f"行索引{row_index}超出范围")
                return {}
        except Exception as e:
            logger.error(f"获取角色信息失败: {e}")
            return {}
    
    def is_new_role_button_visible(self) -> bool:
        """检查新建角色按钮是否可见"""
        return self.is_visible(self.NEW_ROLE_BUTTON, timeout=5000)
    
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
