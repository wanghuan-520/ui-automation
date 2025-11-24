import re

# 从最新的日志中提取对话框HTML
log_file = "pytest_log.txt"

# 运行测试并保存日志
import subprocess
result = subprocess.run(
    ["pytest", "tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflowsE2E::test_workflow_full_lifecycle_e2e", "-v", "-s"],
    capture_output=True,
    text=True,
    timeout=120
)

# 查找对话框HTML
html_match = re.search(r'📄 对话框HTML结构:\s*(<div role="dialog".*?</div>)\s*📝', result.stdout + result.stderr, re.DOTALL)

if html_match:
    dialog_html = html_match.group(1)
    
    # 格式化HTML
    from html import unescape
    dialog_html = unescape(dialog_html)
    
    # 保存到文件
    with open("reports/delete_dialog_structure.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Delete Dialog Structure</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .info { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        pre { background: #f5f5f5; padding: 15px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Delete Workflow Dialog - Current Structure</h1>
    <div class="info">
        <p><strong>Environment:</strong> localhost:5173</p>
        <p><strong>Date:</strong> 2025-11-24</p>
        <p><strong>Finding:</strong> No checkbox or "I understand" text found</p>
    </div>
    <h2>Complete HTML Structure:</h2>
    <pre>""" + dialog_html.replace("<", "&lt;").replace(">", "&gt;") + """</pre>
    <h2>Rendered View:</h2>
    <div style="border: 2px solid #ccc; padding: 20px; background: white;">
""" + dialog_html + """
    </div>
</body>
</html>""")
    print("✅ HTML结构已保存到: reports/delete_dialog_structure.html")
else:
    print("❌ 未找到对话框HTML")
