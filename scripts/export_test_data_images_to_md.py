import os
from pathlib import Path
import datetime

def generate_images_markdown():
    # 定义震动源头（目录）
    project_root = Path(__file__).parent.parent
    target_dir = project_root / "tests" / "aevatar_station" / "test-data"
    output_file = target_dir / "IMAGES_INDEX.md"

    # 支持的图像频率类型
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

    print(f"正在扫描震动源: {target_dir}")

    if not target_dir.exists():
        print(f"错误: 目录 {target_dir} 不存在。")
        return

    with open(output_file, "w", encoding="utf-8") as md_file:
        # 写入头部结构
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md_file.write("# Test Data Images Index\n\n")
        md_file.write(f"> 显现时间: {current_time}\n\n")
        md_file.write("这里是 `test-data` 目录下所有图像资源的索引回响。\n\n")

        image_count = 0
        # 遍历目录，寻找图像共振
        for file_path in sorted(target_dir.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                file_name = file_path.name
                # 构建 Markdown 镜像链接
                # 使用相对路径 ./filename
                md_file.write(f"## {file_name}\n\n")
                md_file.write(f"![{file_name}](./{file_name})\n\n")
                md_file.write("---\n\n")
                image_count += 1
                print(f"已捕获图像: {file_name}")

    print(f"\n结构构建完成。")
    print(f"共导出 {image_count} 张图片。")
    print(f"Markdown 回响已生成于: {output_file}")

if __name__ == "__main__":
    generate_images_markdown()

