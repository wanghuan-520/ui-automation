import pytest
from playwright.sync_api import Page

def test_check_delete_dialog(page: Page):
    """详细检查删除确认对话框"""
    
    # 1. 登录
    print("\n=== 登录 ===")
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")
    
    if page.locator("input[type='email']").count() > 0:
        page.fill("input[type='email']", "haylee@test.com")
        page.fill("input[type='password']", "Wh520520!")
        page.click("button:has-text('Login')")
        page.wait_for_timeout(3000)
    
    # 2. 进入Workflows
    print("\n=== 进入Workflows ===")
    page.goto("http://localhost:5173/dashboard/workflows")
    page.wait_for_selector("role=table", timeout=10000)
    
    # 3. 打开删除对话框
    print("\n=== 打开删除对话框 ===")
    first_row = page.locator("table tbody tr", has_text="untitled_workflow").first
    menu_btn = first_row.locator("td:last-child button").first
    menu_btn.click()
    page.wait_for_timeout(1000)
    
    page.locator("text=Delete").first.click()
    page.wait_for_timeout(1000)
    
    # 4. 详细分析对话框
    print("\n=== 分析删除确认对话框 ===")
    dialog = page.locator("role=dialog")
    
    if not dialog.is_visible():
        print("❌ 对话框不可见!")
        return
    
    # 对话框文本
    dialog_text = dialog.inner_text()
    print(f"\n📝 对话框完整文本:\n{dialog_text}\n")
    
    # 对话框HTML结构
    print("\n🔍 对话框HTML结构:")
    dialog_html = dialog.evaluate("el => el.outerHTML")
    print(dialog_html[:1000])  # 打印前1000字符
    
    # 查找所有输入元素
    print("\n\n📋 查找所有输入元素:")
    input_types = ["input", "textarea", "select", "[contenteditable]"]
    for input_type in input_types:
        inputs = dialog.locator(input_type).all()
        print(f"  {input_type}: {len(inputs)} 个")
        for i, inp in enumerate(inputs):
            try:
                inp_type = inp.get_attribute("type") or "N/A"
                inp_visible = inp.is_visible()
                print(f"    [{i+1}] type={inp_type}, visible={inp_visible}")
            except:
                pass
    
    # 查找所有复选框相关元素
    print("\n\n☑️  查找复选框元素:")
    checkbox_selectors = [
        "input[type='checkbox']",
        "[role='checkbox']",
        ".checkbox",
        ".ant-checkbox",
        "label:has(input[type='checkbox'])",
        "*[class*='check']",
        "*[class*='Check']"
    ]
    
    for selector in checkbox_selectors:
        try:
            count = dialog.locator(selector).count()
            if count > 0:
                print(f"  ✅ {selector}: {count} 个")
                for i in range(count):
                    elem = dialog.locator(selector).nth(i)
                    visible = elem.is_visible()
                    enabled = not elem.is_disabled() if elem.count() > 0 else False
                    html = elem.evaluate("el => el.outerHTML")[:200]
                    print(f"      [{i+1}] visible={visible}, enabled={enabled}")
                    print(f"      HTML: {html}")
            else:
                print(f"  ❌ {selector}: 0 个")
        except Exception as e:
            print(f"  ⚠️  {selector}: 查询出错 - {e}")
    
    # 查找所有按钮
    print("\n\n🔘 对话框按钮:")
    buttons = dialog.locator("button").all()
    print(f"  总计: {len(buttons)} 个按钮")
    
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text()
            disabled = btn.is_disabled()
            visible = btn.is_visible()
            class_attr = btn.get_attribute("class") or ""
            
            print(f"\n  按钮 {i+1}:")
            print(f"    文本: '{text}'")
            print(f"    禁用: {disabled}")
            print(f"    可见: {visible}")
            print(f"    class: {class_attr}")
            
            # 尝试检查aria属性
            aria_disabled = btn.get_attribute("aria-disabled")
            if aria_disabled:
                print(f"    aria-disabled: {aria_disabled}")
                
        except Exception as e:
            print(f"  按钮 {i+1}: 读取失败 - {e}")
    
    # 特别检查Yes按钮
    print("\n\n🎯 特别检查Yes按钮:")
    yes_btn = dialog.locator("button:has-text('Yes')").first
    if yes_btn.count() > 0:
        print(f"  存在: True")
        print(f"  可见: {yes_btn.is_visible()}")
        print(f"  禁用: {yes_btn.is_disabled()}")
        print(f"  enabled: {yes_btn.is_enabled()}")
        
        # 检查是否有data-disabled等属性
        attrs = ["disabled", "aria-disabled", "data-disabled", "data-state"]
        for attr in attrs:
            val = yes_btn.get_attribute(attr)
            if val:
                print(f"  {attr}: {val}")
    else:
        print("  ❌ Yes按钮未找到")
    
    print("\n\n=== 分析完成 ===")
    page.wait_for_timeout(5000)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])
