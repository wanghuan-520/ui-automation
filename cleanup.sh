#!/bin/bash
# 清理脚本 - 删除所有生成的测试文件和报告

cd "$(dirname "$0")"

echo "🧹 开始清理项目..."

# 清理测试截图
if [ -d "test-screenshots" ]; then
    echo "📸 清理测试截图..."
    rm -rf test-screenshots/*
fi

# 清理Allure报告
echo "📊 清理Allure报告..."
rm -rf allure-results allure-results-smoke
rm -rf allure-report allure-report-smoke

# 清理Pytest缓存
echo "🗑️  清理Pytest缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# 清理测试报告
echo "📄 清理测试报告..."
rm -rf reports/*.html 2>/dev/null
rm -rf logs/*.log 2>/dev/null

# 清理日志文件
rm -f diagnose_output.log diagnosis_output.log test_output.log 2>/dev/null

# 清理临时文件
echo "🗂️  清理临时文件..."
find . -type f -name "*.tmp" -delete 2>/dev/null
find . -type f -name "*.bak" -delete 2>/dev/null

echo "✅ 清理完成！"
echo ""
echo "保留的目录："
echo "  - tests/ (测试代码)"
echo "  - test-cases/ (测试用例文档)"
echo "  - test-data/ (测试数据)"
echo ""
echo "已清理："
echo "  ✅ 测试截图"
echo "  ✅ Allure报告"
echo "  ✅ Pytest缓存"
echo "  ✅ 测试报告"
echo "  ✅ 日志文件"

