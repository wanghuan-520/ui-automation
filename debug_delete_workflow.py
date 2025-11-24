"""
调试脚本：测试删除工作流功能
"""
from playwright.sync_api import sync_playwright
import time

def test_delete_workflow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. 登录
            print("=== 步骤1: 登录 ===")
            page.goto("http://localhost:5173")
            page.wait_for_load_state("networkidle")
            page.fill("input[type='email']", "haylee@test.com")
            page.fill("input[type='password']", "Wh520520!")
            page.click("button:has-text('Login')")
            page.wait_for_timeout(3000)
            print(f"✅ 登录后URL: {page.url}")
            
            # 2. 进入Workflows页面
            print("\n=== 步骤2: 进入Workflows页面 ===")
            page.goto("http://localhost:5173/dashboard/workflows")
            page.wait_for_timeout(2000)
            page.wait_for_selector("role=table", timeout=10000)
            
            # 3. 记录删除前的数量
            print("\n=== 步骤3: 记录删除前数量 ===")
            workflows_before = page.locator("table tbody tr").count()
            print(f"删除前工作流总数: {workflows_before}")
            page.screenshot(path="reports/screenshots/mcp_before_delete.png")
            
            # 4. 找到第一个untitled_workflow并点击操作菜单
            print("\n=== 步骤4: 点击第一个untitled_workflow的操作菜单 ===")
            first_untitled_row = page.locator("table tbody tr", has_text="untitled_workflow").first
            action_button = first_untitled_row.locator("td:last-child button").first
            action_button.click()
            page.wait_for_timeout(1000)
            print("✅ 操作菜单已打开")
            page.screenshot(path="reports/screenshots/mcp_menu_opened.png")
            
            # 5. 点击Delete
            print("\n=== 步骤5: 点击Delete ===")
            delete_option = page.locator("text=Delete").first
            delete_option.click()
            page.wait_for_timeout(1000)
            print("✅ Delete选项已点击")
            page.screenshot(path="reports/screenshots/mcp_delete_dialog.png")
            
            # 6. 查看对话框内容
            print("\n=== 步骤6: 分析删除确认对话框 ===")
            dialog = page.locator("role=dialog")
            if dialog.is_visible():
                dialog_text = dialog.inner_text()
                print(f"对话框文本:\n{dialog_text}")
                
                # 查找所有按钮
                buttons = dialog.locator("button").all()
                print(f"\n对话框中的按钮数量: {len(buttons)}")
                for i, btn in enumerate(buttons):
                    try:
                        btn_text = btn.inner_text()
                        is_disabled = btn.is_disabled()
                        print(f"  按钮{i+1}: '{btn_text}' (禁用: {is_disabled})")
                    except:
                        print(f"  按钮{i+1}: 无法读取")
            
            # 7. 直接点击Yes
            print("\n=== 步骤7: 点击Yes确认删除 ===")
            yes_button = dialog.locator("button:has-text('Yes')").first
            yes_button.click(force=True)
            print("✅ Yes按钮已点击")
            page.wait_for_timeout(3000)
            
            # 8. 检查删除结果
            print("\n=== 步骤8: 检查删除提示 ===")
            try:
                page.wait_for_selector("role=dialog", state="hidden", timeout=5000)
                print("✅ 对话框已关闭")
            except:
                print("⚠️ 对话框可能未关闭")
            
            page.screenshot(path="reports/screenshots/mcp_after_delete.png")
            
            # 9. 刷新页面验证
            print("\n=== 步骤9: 刷新页面验证 ===")
            page.reload()
            page.wait_for_timeout(3000)
            page.wait_for_selector("role=table", timeout=10000)
            
            workflows_after = page.locator("table tbody tr").count()
            print(f"刷新后工作流总数: {workflows_after}")
            page.screenshot(path="reports/screenshots/mcp_after_refresh.png")
            
            # 10. 结果对比
            print("\n=== 删除结果 ===")
            print(f"删除前: {workflows_before}")
            print(f"删除后: {workflows_after}")
            if workflows_after < workflows_before:
                print("✅ 删除成功!")
            else:
                print("❌ 删除失败! 数量未减少")
            
            input("\n按Enter键关闭浏览器...")
            
        except Exception as e:
            print(f"❌ 出错: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path="reports/screenshots/mcp_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    test_delete_workflow()
