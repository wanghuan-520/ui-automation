"""
WorkflowPage - 工作流页面对象
路径: /workflow
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class WorkflowPage(BasePage):
    """工作流页面对象"""
    
    # 元素定位器
    USER_MENU_BUTTON = "button:has-text('Toggle user menu')"
    FILE_INPUT = "input[type='file']"
    IMPORT_BUTTON = "button:has-text('Import Workflow')"
    NEW_WORKFLOW_BUTTON = "button:has-text('New Workflow')"
    WORKFLOW_TABLE = "table"
    EMPTY_STATE = "text=No workflows created yet"
    PAGE_TITLE = "p:has-text('Workflows')"
    
    def navigate(self):
        """导航到工作流页面"""
        logger.info("导航到工作流页面")
        self.navigate_to("/workflow")
        # 等待页面加载
        self.page.wait_for_timeout(3000)
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.PAGE_TITLE) or self.is_visible(self.NEW_WORKFLOW_BUTTON)
    
    def create_new_workflow(self):
        """创建新工作流"""
        logger.info("点击创建新工作流按钮")
        self.click_element(self.NEW_WORKFLOW_BUTTON)
    
    def import_workflow(self, file_path):
        """导入工作流"""
        logger.info(f"导入工作流文件: {file_path}")
        self.page.set_input_files(self.FILE_INPUT, file_path)
        self.click_element(self.IMPORT_BUTTON)
    
    def is_workflow_table_visible(self):
        """检查工作流表格是否可见"""
        return self.is_visible(self.WORKFLOW_TABLE)
    
    def is_empty_state_visible(self):
        """检查空状态提示是否可见"""
        return self.is_visible(self.EMPTY_STATE)

