#!/bin/bash
# 快速查看Allure报告

echo "🌐 正在启动Allure服务器..."
echo ""
echo "💡 提示："
echo "  • Allure服务器会自动打开浏览器"
echo "  • 报告将正确显示（无CORS问题）"
echo "  • 按 Ctrl+C 可停止服务器"
echo ""

# 检查是否有测试结果
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
    echo "❌ 未找到测试结果"
    echo "💡 请先运行测试："
    echo "   python3 run_daily_regression_allure.py --stable"
    exit 1
fi

# 使用allure serve查看报告（推荐）
# 这会重新生成报告并启动服务器
allure serve allure-results

