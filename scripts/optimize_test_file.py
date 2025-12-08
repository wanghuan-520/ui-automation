import re

file_path = 'tests/aevatar_station/test_profile_change_password.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 插入 BOUNDARY_TEST_CASES
cases_code = """    # 边界值测试数据（用于参数化测试）
    BOUNDARY_TEST_CASES = [
        {
            "value": "Ab1!",
            "length": 4,
            "description": "小于边界值-2（4字符）",
            "meets_complexity": True,
            "should_pass": False,
            "expected_error": "密码过短"
        },
        {
            "value": "Ab1!5",
            "length": 5,
            "description": "小于边界值-1（5字符）",
            "meets_complexity": True,
            "should_pass": False,
            "expected_error": "密码过短"
        },
        {
            "value": "Ab1!56",
            "length": 6,
            "description": "等于边界值（6字符，满足复杂度）",
            "meets_complexity": True,
            "should_pass": True,
            "expected_error": None
        },
        {
            "value": "Ab1!567",
            "length": 7,
            "description": "大于边界值+1（7字符）",
            "meets_complexity": True,
            "should_pass": True,
            "expected_error": None
        },
        {
            "value": "Ab1!567890123456789012345678901234567890123456789",
            "length": 50,
            "description": "远大于边界值（50字符）",
            "meets_complexity": True,
            "should_pass": True,
            "expected_error": None
        },
        {
            "value": "aaaaaa",
            "length": 6,
            "description": "等于边界值但不满足复杂度（仅小写）",
            "meets_complexity": False,
            "should_pass": False,
            "expected_error": "复杂度不足"
        },
        {
            "value": "AAAAAA",
            "length": 6,
            "description": "等于边界值但不满足复杂度（仅大写）",
            "meets_complexity": False,
            "should_pass": False,
            "expected_error": "复杂度不足"
        },
        {
            "value": "123456",
            "length": 6,
            "description": "等于边界值但不满足复杂度（仅数字）",
            "meets_complexity": False,
            "should_pass": False,
            "expected_error": "复杂度不足"
        },
    ]
    
    @pytest.mark.P0"""

content = content.replace('@pytest.mark.P0', cases_code, 1)

# 2. 替换 test_p1_password_length_boundary 方法
new_method = """    @pytest.mark.P1
    @pytest.mark.boundary
    @pytest.mark.parametrize("test_case", BOUNDARY_TEST_CASES, ids=lambda x: x["description"])
    def test_p1_password_length_boundary(self, logged_in_change_password_page, request, test_case):
        \"\"\"TC-PWD-006: 密码长度边界值测试（参数化）\"\"\"
        logger.info(f"执行边界值测试: {test_case['description']}")
        
        password_page = logged_in_change_password_page
        # 从账号池获取当前密码
        current_password = request.node._account_info[2] if hasattr(request.node, '_account_info') else "TestPass123!"
        
        # 填写表单并提交
        password_page.change_password(
            current_password=current_password,
            new_password=test_case["value"],
            confirm_password=test_case["value"]
        )
        
        # 智能等待结果
        success_found = False
        error_found = False
        
        # 定义选择器
        success_selectors = ["text=successfully", "text=Success", "text=success", ".text-success", ".alert-success"]
        error_selectors = ["text=Failed", "text=Error", ".text-danger", ".alert-danger", "text=/failed/i", "text=/error/i"]
        
        # 轮询等待（最多3秒）
        import time
        start_time = time.time()
        while time.time() - start_time < 3:
            # 检查成功
            for sel in success_selectors:
                if password_page.page.is_visible(sel):
                    success_found = True
                    break
            # 检查失败
            for sel in error_selectors:
                if password_page.page.is_visible(sel):
                    error_found = True
                    break
            if success_found or error_found:
                break
            password_page.page.wait_for_timeout(200)
            
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_boundary_{test_case['length']}_{timestamp}.png"
        password_page.take_screenshot(screenshot_path, reveal_passwords=True)
        
        # 判定
        actual_passed = False
        if success_found and not error_found:
            actual_passed = True
        elif error_found:
            actual_passed = False
        
        # Allure 记录
        result_status = "成功" if actual_passed else "失败"
        expected_status = "成功" if test_case['should_pass'] else "失败"
        
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name=f"{test_case['description']}（预期:{expected_status}, 实际:{result_status}）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 断言
        assert actual_passed == test_case['should_pass'], \\
            f"结果不符: 预期 {expected_status}, 实际 {result_status}"
            
        # 如果修改成功，fixture teardown 会自动恢复密码，无需手动操作
"""

# 使用正则找到旧方法的起始和结束位置进行替换
# 旧方法签名：def test_p1_password_length_boundary(self, logged_in_change_password_page, request):
# 下一个方法签名：def test_p2_password_complexity_requirements
pattern = r'@pytest\.mark\.P1\s+@pytest\.mark\.boundary\s+def test_p1_password_length_boundary[\s\S]+?(?=@pytest\.mark\.P2)'
match = re.search(pattern, content)

if match:
    content = content[:match.start()] + new_method + "\n    " + content[match.end():]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Optimization applied successfully.")
else:
    print("Could not find the target method to replace.")

