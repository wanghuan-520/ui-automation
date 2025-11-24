import pytest
from playwright.sync_api import Page
import sys

def test_delete_workflow_with_agents(page: Page):
    """测试删除包含Agent的Workflow"""
    
    print("\n=== 步骤1: 登录 ===", file=sys.stderr)
    page.goto("http://localhost:5173")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    
    # 检查登录
    if page.locator("input[type='email']").count() > 0:
        page.fill("input[type='email']", "haylee@test.com")
        page.fill("input[type='password']", "Wh520520!")
        page.click("button:has-text('Login')")
        page.wait_for_timeout(3000)
    
    print(f"\n当前URL: {page.url}", file=sys.stderr)
    
    # 步骤2: 进入Workflows列表
    print("\n=== 步骤2: 进入Workflows列表 ===", file=sys.stderr)
    page.goto("http://localhost:5173/dashboard/workflows")
    page.wait_for_timeout(2000)
    page.wait_for_selector("role=table", timeout=10000)
    
    # 步骤3: 找一个包含Agent的workflow (通常是有Last run时间的)
    print("\n=== 步骤3: 查找包含Agent的Workflow ===", file=sys.stderr)
    rows = page.locator("table tbody tr").all()
    print(f"找到 {len(rows)} 个workflow", file=sys.stderr)
    
    # 尝试找第一个有Last run的workflow (说明运行过,应该包含Agent)
    target_workflow = None
    for row in rows[:5]:  # 只检查前5个
        try:
            last_run = row.locator("td").nth(2).inner_text()
            if last_run and last_run != "-":
                workflow_name = row.locator("td").first.inner_text()
                target_workflow = workflow_name
                print(f"找到包含执行记录的workflow: {workflow_name}", file=sys.stderr)
                break
        except:
            pass
    
    if not target_workflow:
        # 如果没找到,就用第一个untitled_workflow
        target_workflow = "untitled_workflow"
        print(f"未找到有执行记录的workflow,使用: {target_workflow}", file=sys.stderr)
    
    page.screenshot(path="reports/screenshots/mcp_workflow_list.png")
    
    # 步骤4: 点击操作菜单
    print(f"\n=== 步骤4: 打开 '{target_workflow}' 的操作菜单 ===", file=sys.stderr)
    target_row = page.locator("table tbody tr", has_text=target_workflow).first
    menu_btn = target_row.locator("td:last-child button").first
    menu_btn.click()
    page.wait_for_timeout(1000)
    page.screenshot(path="reports/screenshots/mcp_menu.png")
    
    # 步骤5: 点击Delete
    print("\n=== 步骤5: 点击Delete ===", file=sys.stderr)
    page.locator("text=Delete").first.click()
    page.wait_for_timeout(1500)
    page.screenshot(path="reports/screenshots/mcp_delete_dialog_final.png")
    
    # 步骤6: 详细分析对话框
    print("\n=== 步骤6: 分析删除确认对话框 ===", file=sys.stderr)
    dialog = page.locator("role=dialog")
    
    if not dialog.is_visible():
        print("❌ 对话框不可见!", file=sys.stderr)
        return
    
    # 对话框完整文本
    dialog_text = dialog.inner_text()
    print(f"\n📝 对话框文本:\n{dialog_text}\n", file=sys.stderr)
    
    # 对话框HTML (只打印前2000字符)
    dialog_html = dialog.evaluate("el => el.outerHTML")
    print(f"\n📄 对话框HTML (前2000字符):\n{dialog_html[:2000]}\n", file=sys.stderr)
    
    # 查找复选框
    print("\n☑️  查找复选框/确认元素:", file=sys.stderr)
    checkbox_selectors = [
        "input[type='checkbox']",
        "[role='checkbox']",
        "label",
        "*[class*='checkbox']",
        "*[class*='check']"
    ]
    
    found_checkbox = False
    for selector in checkbox_selectors:
        count = dialog.locator(selector).count()
        if count > 0:
            print(f"  ✅ {selector}: {count} 个", file=sys.stderr)
            for i in range(min(count, 3)):  # 最多显示3个
                elem = dialog.locator(selector).nth(i)
                try:
                    visible = elem.is_visible()
                    text = elem.inner_text() if visible else "N/A"
                    print(f"      [{i+1}] visible={visible}, text='{text[:50]}'", file=sys.stderr)
                    if visible:
                        found_checkbox = True
                except:
                    pass
        else:
            print(f"  ❌ {selector}: 0 个", file=sys.stderr)
    
    # 查找按钮
    print("\n🔘 对话框按钮:", file=sys.stderr)
    buttons = dialog.locator("button").all()
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text()
            disabled = btn.is_disabled()
            visible = btn.is_visible()
            print(f"  按钮{i+1}: '{text}' (visible={visible}, disabled={disabled})", file=sys.stderr)
        except:
            pass
    
    if found_checkbox:
        print("\n✅ 找到复选框元素!", file=sys.stderr)
    else:
        print("\n❌ 未找到任何复选框元素", file=sys.stderr)
    
    print("\n=== 测试完成,请查看截图 ===", file=sys.stderr)
    page.wait_for_timeout(3000)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])
