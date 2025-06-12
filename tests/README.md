# GodGPT自动化测试说明

## 环境要求

- Python 3.7+
- Appium Server
- Android SDK
- 已安装的GodGPT应用

## 安装依赖

```bash
pip install -r test-requirements/requirements.txt
```

## 运行测试前的准备

1. 确保Appium服务器已启动：
```bash
appium
```

2. 确保Android设备已连接并启用USB调试模式：
```bash
adb devices
```

3. 确保GodGPT应用已安装在设备上

## 运行测试

在项目根目录下执行：
```bash
python -m pytest tests/test_godgpt_wisdom.py -v
```

## 测试内容

当前测试用例包含：
- Today's Wisdom Drop功能的完整流程测试
  - 验证卡片点击
  - 验证页面跳转
  - 验证关键元素显示
  - 验证交互组件存在

## 注意事项

1. 测试前请确保设备ID在`test_godgpt_wisdom.py`中正确配置
2. 测试使用`noReset`模式，保持应用数据不被清除
3. 如果测试失败，会自动保存截图到`error_screenshot.png`

## 调试提示

如果遇到元素定位问题，可以使用Appium Inspector工具来获取正确的元素定位信息。 