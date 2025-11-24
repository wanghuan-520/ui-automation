"""
使用Playwright Inspector定位删除对话框元素
运行后会暂停,可以手动inspect元素
"""
from playwright.sync_api import sync_playwright
import time

def inspect_delete_dialog():
    with sync_playwright() as p:
        # 使用inspector模式
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 登录
            print("正在登录...")
            page.goto("http://localhost:5173")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)
            
            if page.locator("input[type='email']").count() > 0:
                page.fill("input[type='email']", "haylee@test.com")
                page.fill("input[type='password']", "Wh520520!")
                page.click("button:has-text('Login')")
                page.wait_for_timeout(3000)
            
            # 进入Workflows
            print("进入Workflows页面...")
            page.goto("http://localhost:5173/dashboard/workflows")
            page.wait_for_timeout(2000)
            page.wait_for_selector("role=table", timeout=10000)
            
            # 打开删除对话框
            print("打开删除对话框...")
            first_row = page.locator("table tbody tr", has_text="untitled_workflow").first
            menu_btn = first_row.locator("td:last-child button").first
            menu_btn.click()
            page.wait_for_timeout(1000)
            
            page.locator("text=Delete").first.click()
            page.wait_for_timeout(1500)
            
            print("\n" + "="*60)
            print("删除对话框已打开!")
            print("="*60)
            
            # 获取对话框
            dialog = page.locator("role=dialog")
            
            # 输出对话框所有文本内容
            print("\n📝 对话框完整文本:")
            print(dialog.inner_text())
            
            # 查找所有可交互元素
            print("\n" + "="*60)
            print("🔍 对话框中的所有可交互元素:")
            print("="*60)
            
            # 1. 所有input元素
            inputs = dialog.locator("input").all()
            print(f"\n1. Input元素: {len(inputs)} 个")
            for i, inp in enumerate(inputs):
                inp_type = inp.get_attribute("type")
                inp_name = inp.get_attribute("name") or ""
                inp_id = inp.get_attribute("id") or ""
                visible = inp.is_visible()
                print(f"   [{i+1}] type={inp_type}, name={inp_name}, id={inp_id}, visible={visible}")
            
            # 2. 所有label元素
            labels = dialog.locator("label").all()
            print(f"\n2. Label元素: {len(labels)} 个")
            for i, lbl in enumerate(labels):
                try:
                    text = lbl.inner_text()
                    visible = lbl.is_visible()
                    lbl_for = lbl.get_attribute("for") or ""
                    print(f"   [{i+1}] text='{text[:60]}', for={lbl_for}, visible={visible}")
                except:
                    pass
            
            # 3. 所有div元素(可能是自定义复选框)
            divs_with_role = dialog.locator("div[role]").all()
            print(f"\n3. 带role的Div元素: {len(divs_with_role)} 个")
            for i, div in enumerate(divs_with_role[:10]):  # 只显示前10个
                role = div.get_attribute("role")
                try:
                    text = div.inner_text()[:40]
                except:
                    text = ""
                print(f"   [{i+1}] role={role}, text='{text}'")
            
            # 4. 包含"understand"或"checkbox"文本的所有元素
            print(f"\n4. 包含'understand'文本的元素:")
            understand_elems = dialog.locator("text=/understand/i").all()
            print(f"   找到 {len(understand_elems)} 个")
            for i, elem in enumerate(understand_elems):
                try:
                    text = elem.inner_text()
                    tag = elem.evaluate("el => el.tagName")
                    visible = elem.is_visible()
                    print(f"   [{i+1}] <{tag}> visible={visible}")
                    print(f"        text: {text}")
                except:
                    pass
            
            # 5. 所有button元素
            buttons = dialog.locator("button").all()
            print(f"\n5. Button元素: {len(buttons)} 个")
            for i, btn in enumerate(buttons):
                try:
                    text = btn.inner_text()
                    disabled = btn.is_disabled()
                    visible = btn.is_visible()
                    print(f"   [{i+1}] text='{text}', disabled={disabled}, visible={visible}")
                except:
                    pass
            
            # 6. 获取完整HTML结构
            print(f"\n6. 对话框完整HTML (前3000字符):")
            html = dialog.evaluate("el => el.outerHTML")
            print(html[:3000])
            
            print("\n" + "="*60)
            print("✅ 元素分析完成")
            print("="*60)
            print("\n按Ctrl+C退出...")
            
            # 保持页面打开
            input()
            
        except KeyboardInterrupt:
            print("\n用户中断")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    inspect_delete_dialog()
