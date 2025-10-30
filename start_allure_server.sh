#!/bin/bash
# 启动 Allure 报告服务器（避免跨域问题）

echo "🚀 启动 Allure 报告服务器..."
echo "=================================="
echo ""

cd "$(dirname "$0")"

# 检查端口是否被占用
if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 8888 已被占用"
    echo "🔄 停止旧服务..."
    pkill -f "allure.*serve.*8888"
    sleep 2
fi

# 检查报告数据是否存在
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
    echo "❌ 测试结果不存在"
    echo "💡 请先运行测试："
    echo "   python3 -m pytest tests/aevatar/test_daily_regression_project.py -m project --alluredir=allure-results"
    exit 1
fi

echo "✨ 正在启动服务..."
echo "📊 报告地址: http://localhost:8888"
echo ""
echo "💡 提示:"
echo "   - 浏览器会自动打开"
echo "   - 按 Ctrl+C 停止服务器"
echo "   - 如果浏览器未自动打开，请手动访问: http://localhost:8888"
echo ""

# 启动服务（会自动打开浏览器）
allure serve allure-results -p 8888


