import pytest
from playwright.sync_api import Page

def test_debug_delete_workflow(page: Page):
    """调试删除工作流功能"""
    
    # 1. 登录
    print("\n=== 步骤1: 登录 ===")
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # 检查是否需要登录
    if "login" in page.url.lower() or page.locator("input[type='email']").count() > 0:
        page.fill("input[type='email']", "haylee@test.com")
        page.fill("input[type='password']", "Wh520520!")
        page.click("button:has-text('Login')")
        page.wait_for_timeout(3000)
    print(f"✅ 当前URL: {page.url}")
    
    # 2. 进入Workflows页面
    print("\n=== 步骤2: 进入Workflows ===")
    page.goto("http://localhost:5173/dashboard/workflows")
    page.wait_for_timeout(2000)
    page.wait_for_selector("role=table", timeout=10000)
    
    # 3. 记录删除前数量
    print("\n=== 步骤3: 记录删除前数量 ===")
    workflows_before = page.locator("table tbody tr").count()
    print(f"删除前: {workflows_before} 个工作流")
    page.screenshot(path="reports/screenshots/debug_before_delete.png")
    
    # 4. 点击第一个untitled_workflow的菜单
    print("\n=== 步骤4: 打开操作菜单 ===")
    first_row = page.locator("table tbody tr", has_text="untitled_workflow").first
    menu_btn = first_row.locator("td:last-child button").first
    menu_btn.click()
    page.wait_for_timeout(1000)
    page.screenshot(path="reports/screenshots/debug_menu_opened.png")
    print("✅ 菜单已打开")
    
    # 5. 点击Delete
    print("\n=== 步骤5: 点击Delete ===")
    page.locator("text=Delete").first.click()
    page.wait_for_timeout(1000)
    page.screenshot(path="reports/screenshots/debug_delete_dialog.png")
    print("✅ 删除对话框已打开")
    
    # 6. 分析对话框
    print("\n=== 步骤6: 分析对话框 ===")
    dialog = page.locator("role=dialog")
    dialog_text = dialog.inner_text()
    print(f"对话框内容:\n{dialog_text}\n")
    
    buttons = dialog.locator("button").all()
    print(f"对话框按钮: {len(buttons)} 个")
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text()
            disabled = btn.is_disabled()
            print(f"  按钮{i+1}: '{text}' (禁用={disabled})")
        except:
            pass
    
    # 7. 点击Yes
    print("\n=== 步骤7: 点击Yes ===")
    yes_btn = dialog.locator("button:has-text('Yes')").first
    yes_btn.click(force=True)
    print("✅ Yes已点击")
    page.wait_for_timeout(3000)
    
    # 8. 等待对话框关闭
    print("\n=== 步骤8: 等待删除完成 ===")
    try:
        page.wait_for_selector("role=dialog", state="hidden", timeout=5000)
        print("✅ 对话框已关闭")
    except:
        print("⚠️ 对话框未关闭")
    
    page.screenshot(path="reports/screenshots/debug_after_click_yes.png")
    
    # 9. 刷新页面
    print("\n=== 步骤9: 刷新页面 ===")
    page.reload()
    page.wait_for_timeout(2000)
    page.wait_for_selector("role=table", timeout=10000)
    
    # 10. 再次计数
    workflows_after = page.locator("table tbody tr").count()
    print(f"刷新后: {workflows_after} 个工作流")
    page.screenshot(path="reports/screenshots/debug_after_refresh.png")
    
    # 11. 结果
    print("\n=== 删除结果 ===")
    print(f"删除前: {workflows_before}")
    print(f"删除后: {workflows_after}")
    print(f"差值: {workflows_before - workflows_after}")
    
    if workflows_after < workflows_before:
        print("✅ 删除成功!")
    else:
        print("❌ 删除失败! 数量未减少")
        
    page.wait_for_timeout(2000)
