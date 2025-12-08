import markdown
import os
from pathlib import Path

def convert_md_to_html():
    # 定义震动源和目标
    base_dir = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data"
    md_file = base_dir / "知识.md"
    html_file = base_dir / "知识_preview.html"

    if not md_file.exists():
        print(f"源文件不存在: {md_file}")
        return

    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 转换为 HTML
    html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])

    # 添加 CSS 样式 (GitHub/Notion 风格)
    styled_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>知识库重构</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background-color: #ffffff;
        }}
        h1, h2, h3 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{ font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        table th, table td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }}
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        ul, ol {{
            padding-left: 2em;
        }}
        code {{
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
        }}
        hr {{
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }}
    </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(styled_html)

    print(f"HTML 预览已生成: {html_file}")

if __name__ == "__main__":
    convert_md_to_html()

