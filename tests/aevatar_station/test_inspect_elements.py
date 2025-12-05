import pytest
import logging
import json
from tests.aevatar_station.pages.profile_settings_page import ProfileSettingsPage

logger = logging.getLogger(__name__)

@pytest.mark.profile
def test_inspect_profile_elements(logged_in_profile_page):
    """
    探测 Profile 页面元素，用于补充测试用例
    """
    profile_page = logged_in_profile_page
    page = profile_page.page
    
    logger.info("开始探测 Profile 页面元素...")
    
    # 确保页面加载
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    elements_info = []
    
    # 定义感兴趣的元素选择器
    selectors = [
        "input", 
        "button", 
        "a[role='tab']", 
        "select",
        "textarea",
        ".alert",
        "[role='alert']",
        "form"
    ]
    
    for selector in selectors:
        # 使用 page.locator().all() 获取所有匹配元素
        elements = page.locator(selector).all()
        for i, el in enumerate(elements):
            if el.is_visible():
                try:
                    info = {
                        "tag": selector,
                        "id": el.get_attribute("id") or "",
                        "name": el.get_attribute("name") or "",
                        "type": el.get_attribute("type") or "",
                        "class": el.get_attribute("class") or "",
                        "placeholder": el.get_attribute("placeholder") or "",
                        "text": (el.inner_text()).strip()[:50] if selector != "input" else "", # 截断长文本
                        "value": el.input_value() if selector == "input" else "",
                        "role": el.get_attribute("role") or "",
                        "outerHTML": el.evaluate("el => el.outerHTML")
                    }
                    elements_info.append(info)
                except Exception as e:
                    logger.warning(f"获取元素信息失败: {e}")

    # 打印结果
    print("\n=== 页面元素扫描结果 ===")
    print(json.dumps(elements_info, indent=2, ensure_ascii=False))
    print("========================")
    
    # 同时也检查 Change Password tab 下的元素
    # 假设有这个 tab
    change_pwd_tab = page.locator("a[role='tab']:has-text('Change Password')")
    if change_pwd_tab.is_visible():
        logger.info("发现 Change Password tab，尝试切换...")
        change_pwd_tab.click()
        page.wait_for_timeout(2000)
        
        # 扫描 Change Password 页面的 input
        pwd_inputs = page.locator("input[type='password']").all()
        for el in pwd_inputs:
             if el.is_visible():
                info = {
                    "tag": "input[type='password']",
                    "id": el.get_attribute("id") or "",
                    "name": el.get_attribute("name") or "",
                    "placeholder": el.get_attribute("placeholder") or "",
                    "outerHTML": el.evaluate("el => el.outerHTML")
                }
                print(f"密码输入框: {json.dumps(info, ensure_ascii=False)}")

