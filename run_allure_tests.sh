#!/bin/bash
# Aevatar 日常回归测试 - Allure报告快速启动脚本

echo "🌌 Aevatar 日常回归测试 - Allure报告"
echo "=================================="
echo ""

# 默认运行稳定版本测试
python3 run_daily_regression_allure.py --stable

echo ""
echo "✨ 完成！"

