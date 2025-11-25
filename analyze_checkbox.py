"""
详细分析第二层弹窗中的所有可点击元素
"""
from playwright.sync_api import sync_playwright
import json

def analyze_checkbox():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # 登录
            print("登录中...")
            page.goto("http://localhost:5173")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)
            
            if page.locator("input[type='email']").count() > 0:
                page.fill("input[type='email']", "haylee@test.com")
                page.fill("input[type='password']", "Wh520520!")
                page.click("button:has-text('Login')")
                page.wait_for_timeout(3000)
            
            # 进入Workflows
            page.goto("http://localhost:5173/dashboard/workflows")
            page.wait_for_timeout(2000)
            page.wait_for_selector("role=table", timeout=10000)
            
            # 打开第一层弹窗
            print("\n打开删除对话框...")
            first_row = page.locator("table tbody tr", has_text="untitled_workflow").first
            menu_btn = first_row.locator("td:last-child button").first
            menu_btn.click()
            page.wait_for_timeout(1000)
            
            page.locator("text=Delete").first.click()
            page.wait_for_timeout(1500)
            
            # 点击第一层Yes
            print("点击第一层Yes...")
            dialog1 = page.locator("role=dialog")
            dialog1.locator("button:has-text('Yes')").first.click()
            page.wait_for_timeout(2000)
            
            # 分析第二层弹窗
            print("\n" + "="*80)
            print("分析第二层弹窗")
            print("="*80)
            
            dialog2 = page.locator("role=dialog")
            if not dialog2.is_visible():
                print("第二层弹窗未出现!")
                return
            
            # 1. 获取所有元素及其属性
            print("\n1. 弹窗中的所有元素:")
            all_elements = dialog2.locator("*").all()
            print(f"   总元素数: {len(all_elements)}")
            
            # 2. 查找所有可点击的元素
            print("\n2. 可点击的元素 (button, [onclick], [role='button']):")
            clickable_selectors = [
                "button",
                "[onclick]",
                "[role='button']",
                "[role='checkbox']",
                "input",
                "label"
            ]
            
            for selector in clickable_selectors:
                elements = dialog2.locator(selector).all()
                print(f"\n   {selector}: {len(elements)} 个")
                for i, elem in enumerate(elements):
                    try:
                        tag = elem.evaluate("el => el.tagName")
                        visible = elem.is_visible()
                        clickable = elem.is_enabled() if visible else False
                        
                        # 获取所有属性
                        attrs = elem.evaluate("""el => {
                            let attrs = {};
                            for (let attr of el.attributes) {
                                attrs[attr.name] = attr.value;
                            }
                            return attrs;
                        }""")
                        
                        text = elem.inner_text()[:30] if visible else ""
                        
                        print(f"      [{i+1}] <{tag}> visible={visible}, text='{text}'")
                        if attrs:
                            print(f"           属性: {json.dumps(attrs, indent=10)[:200]}")
                    except Exception as e:
                        print(f"      [{i+1}] 无法分析: {e}")
            
            # 3. 特别查找包含"I understand"的元素
            print("\n3. 包含'I understand'的元素及其父元素:")
            understand_elem = dialog2.locator("text=/I understand/i").first
            if understand_elem.count() > 0:
                # 获取元素信息
                elem_info = understand_elem.evaluate("""el => {
                    return {
                        tag: el.tagName,
                        text: el.textContent,
                        classes: el.className,
                        id: el.id,
                        onclick: el.onclick ? 'YES' : 'NO',
                        parentTag: el.parentElement?.tagName,
                        parentClasses: el.parentElement?.className,
                        parentOnclick: el.parentElement?.onclick ? 'YES' : 'NO'
                    };
                }""")
                print(f"   元素信息: {json.dumps(elem_info, indent=4)}")
                
                # 尝试获取前面的兄弟元素(复选框可能在这里)
                sibling = understand_elem.evaluate("""el => {
                    let prev = el.previousElementSibling;
                    if (prev) {
                        return {
                            tag: prev.tagName,
                            text: prev.textContent?.substring(0, 20),
                            classes: prev.className,
                            id: prev.id,
                            type: prev.type,
                            role: prev.getAttribute('role')
                        };
                    }
                    return null;
                }""")
                if sibling:
                    print(f"   前一个兄弟元素: {json.dumps(sibling, indent=4)}")
            
            print("\n" + "="*80)
            print("请在浏览器中手动勾选复选框,观察DevTools中的变化")
            print("按Enter继续...")
            print("="*80)
            
            input()
            
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    analyze_checkbox()
