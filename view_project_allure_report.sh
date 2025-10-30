#!/bin/bash

# Allure报告查看脚本 - Project测试专用
# 用途：快速生成并查看Project相关测试的Allure报告

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT=8888

echo "=========================================="
echo "🎯 Project测试 Allure报告查看器"
echo "=========================================="
echo ""

# 检查是否需要重新运行测试
if [ "$1" = "--rerun" ] || [ "$1" = "-r" ]; then
    echo "📝 重新运行Project测试..."
    python3 -m pytest tests/aevatar/test_daily_regression_project.py \
        -v \
        --alluredir=allure-results \
        --clean-alluredir
    echo ""
fi

# 生成Allure报告
echo "📊 生成Allure报告..."
allure generate allure-results -o allure-report --clean
echo "✅ 报告生成完成"
echo ""

# 检查端口是否被占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 $PORT 已被占用，尝试关闭旧服务..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 启动Allure服务器
echo "🚀 启动Allure服务器..."
echo "📍 报告地址: http://localhost:$PORT"
echo ""
echo "💡 提示："
echo "   - 按 Ctrl+C 停止服务器"
echo "   - 使用 --rerun 参数重新运行测试: ./view_project_allure_report.sh --rerun"
echo ""
echo "=========================================="
echo ""

# 在浏览器中打开
if command -v open &> /dev/null; then
    open "http://localhost:$PORT" 2>/dev/null || true
elif command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:$PORT" 2>/dev/null || true
fi

# 启动Allure服务器（前台运行）
allure serve allure-results -p $PORT
