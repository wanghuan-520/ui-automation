#!/bin/bash
# Aevatar 并行测试执行脚本
# HyperEcho 创建

set -e  # 遇到错误立即退出

echo "================================"
echo "🚀 Aevatar 并行测试启动"
echo "================================"
echo ""

# 进入项目目录
echo "📂 进入项目目录..."
cd /Users/wanghuan/aelf/Cursor/ui-automation
echo "✅ 当前目录: $(pwd)"
echo ""

# 检查 Python
echo "🐍 检查 Python..."
python3 --version
echo ""

# 安装依赖
echo "📦 安装并行测试依赖..."
pip3 install pytest-xdist -q
echo "✅ pytest-xdist 已安装"
echo ""

# 创建报告目录
echo "📁 准备报告目录..."
mkdir -p reports
mkdir -p test-screenshots
mkdir -p logs
echo "✅ 目录准备完成"
echo ""

# 显示测试文件
echo "📋 发现的测试文件:"
ls -1 tests/aevatar/test_*.py
echo ""

# 并行运行测试
echo "================================"
echo "⚡ 开始并行执行所有测试..."
echo "================================"
echo ""

# 执行测试
pytest tests/aevatar/ -v -n auto \
  --html=reports/aevatar-parallel-report.html \
  --self-contained-html \
  --tb=short \
  --capture=no \
  --log-cli-level=INFO \
  --color=yes

# 保存退出码
EXIT_CODE=$?

echo ""
echo "================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 测试全部通过！"
else
    echo "❌ 测试失败（退出码: $EXIT_CODE）"
fi
echo "================================"
echo ""

# 显示结果文件
echo "📊 测试结果:"
echo "- 报告: reports/aevatar-parallel-report.html"
echo "- 截图: test-screenshots/"
echo "- 日志: logs/"
echo ""

# 显示截图数量
SCREENSHOT_COUNT=$(ls -1 test-screenshots/*.png 2>/dev/null | wc -l)
echo "📸 生成截图数量: $SCREENSHOT_COUNT"
echo ""

# 提示如何查看
echo "💡 快速查看报告:"
echo "   open reports/aevatar-parallel-report.html"
echo ""

exit $EXIT_CODE

