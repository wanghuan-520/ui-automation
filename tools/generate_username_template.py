"""
重构Username字段验证用例 - 添加完整的场景覆盖
包括：格式验证、长度边界、必填验证、错误检查
"""

username_test_template = '''    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_username_field_validation(self, logged_in_profile_page):
        """
        TC-VALID-USERNAME-001: Username字段完整验证测试
        
        测试目标：验证Username字段的格式、长度、必填规则
        测试区域：Profile - Personal Settings - Username Validation
        
        ============================================================================
        后端校验规则（ABP Framework AbpUserConsts）:
        ============================================================================
        
        📋 字段属性
        ┌──────────────────────────────────────────────────────────────────┐
        │  字段名：UserName                                                 │
        │  必填状态：✅ 必填（后端强制验证）                               │
        │  可编辑性：✅ 可编辑                                             │
        │  长度限制：1-256字符                                             │
        └──────────────────────────────────────────────────────────────────┘
        
        🔤 字符类型规则
        ┌──────────────────────────────────────────────────────────────────┐
        │  正则表达式：^[a-zA-Z0-9_.@-]+$                                  │
        ├──────────────────────────────────────────────────────────────────┤
        │  ✅ 允许的字符：                                                  │
        │     • 英文字母（大小写）：a-z, A-Z                               │
        │     • 数字：0-9                                                  │
        │     • 下划线：_                                                  │
        │     • 点：.                                                      │
        │     • @符号：@                                                   │
        │     • 连字符：-                                                  │
        ├──────────────────────────────────────────────────────────────────┤
        │  ❌ 不允许的字符：                                                │
        │     • 空格（会导致验证失败）                                     │
        │     • 中文字符（标准ABP不支持）                                  │
        │     • 特殊字符：!#$%^&*()+=[]{}|\\\\:;"'<>,?/等                    │
        └──────────────────────────────────────────────────────────────────┘
        
        📊 测试场景覆盖（共15个场景）
        ┌─────────────────────────────────────────────────────────────────────┐
        │  1. 格式验证-有效（5个）                                             │
        │     ✅ 普通英文、带数字、带点@、带连字符、纯数字                     │
        │  2. 格式验证-无效（4个）                                             │
        │     ❌ 包含空格、特殊字符!@#$%、特殊字符*&^、中文                   │
        │  3. 长度验证（5个）                                                 │
        │     • 最小1字符、正常50字符、边界256字符、超长257字符、极长300字符   │
        │  4. 必填验证（1个）                                                 │
        │     • 空值应触发必填错误                                             │
        └─────────────────────────────────────────────────────────────────────┘
        
        预期结果：
        - 有效格式：成功保存，无错误提示
        - 无效格式：保存失败或被拒绝，应显示错误提示（前端bug检测）
        - 长度边界：超长应被截断或拒绝
        - 必填验证：空值应显示必填错误
        """
        logger.info("=" * 80)
        logger.info("TC-VALID-USERNAME-001: Username字段完整验证（格式+长度+必填）")
        logger.info("=" * 80)
        logger.info("后端规则：1-256字符，必填，^[a-zA-Z0-9_.@-]+$")
        logger.info("=" * 80)
        
        profile_page = logged_in_profile_page
        screenshot_idx = 1
        
        # 获取原始用户名
        original_username = profile_page.get_username_value()
        logger.info(f"原始Username: '{original_username}'")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"username_init_{timestamp}.png"
        profile_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name=f"{screenshot_idx}-Username字段初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        screenshot_idx += 1
        
        # 定义完整测试场景
        test_scenarios = [
            # ========== 1. 格式验证-有效（5个场景） ==========
            {
                "type": "format_valid",
                "name": "普通英文用户名",
                "value": f"TestUser{datetime.now().strftime('%H%M%S')}",
                "should_save": True,
                "should_error": False,
                "description": "纯英文字母（符合正则）",
                "expected": "成功保存",
            },
            {
                "type": "format_valid",
                "name": "带数字下划线",
                "value": f"user_123_{datetime.now().strftime('%H%M%S')}",
                "should_save": True,
                "should_error": False,
                "description": "英文+数字+下划线（符合正则）",
                "expected": "成功保存",
            },
            {
                "type": "format_valid",
                "name": "带点和@符号",
                "value": "user.name@test",
                "should_save": True,
                "should_error": False,
                "description": "包含点和@（符合正则）",
                "expected": "成功保存",
            },
            {
                "type": "format_valid",
                "name": "带连字符",
                "value": "user-name-123",
                "should_save": True,
                "should_error": False,
                "description": "包含连字符（符合正则）",
                "expected": "成功保存",
            },
            {
                "type": "format_valid",
                "name": "纯数字",
                "value": "123456789",
                "should_save": True,
                "should_error": False,
                "description": "纯数字（符合正则）",
                "expected": "成功保存",
            },
            
            # ========== 2. 格式验证-无效（4个场景） ==========
            {
                "type": "format_invalid",
                "name": "包含空格",
                "value": "user name 123",
                "should_save": False,
                "should_error": True,
                "description": "包含空格（不符合正则）",
                "expected": "保存失败，显示错误",
            },
            {
                "type": "format_invalid",
                "name": "特殊字符1",
                "value": "user!@#$%",
                "should_save": False,
                "should_error": True,
                "description": "包含!@#$%（不符合正则）",
                "expected": "保存失败，显示错误",
            },
            {
                "type": "format_invalid",
                "name": "特殊字符2",
                "value": "user*&^",
                "should_save": False,
                "should_error": True,
                "description": "包含*&^（不符合正则）",
                "expected": "保存失败，显示错误",
            },
            {
                "type": "format_invalid",
                "name": "中文字符",
                "value": "测试用户123",
                "should_save": False,
                "should_error": True,
                "description": "包含中文（不符合正则）",
                "expected": "保存失败，显示错误",
            },
            
            # ========== 3. 长度验证（5个场景） ==========
            {
                "type": "length_min",
                "name": "最小长度1字符",
                "value": "a",
                "should_save": True,
                "should_error": False,
                "description": "最小有效长度（边界值）",
                "expected": "成功保存",
            },
            {
                "type": "length_normal",
                "name": "正常长度50字符",
                "value": "u" * 50,
                "should_save": True,
                "should_error": False,
                "description": "正常长度",
                "expected": "成功保存",
            },
            {
                "type": "length_max",
                "name": "最大长度256字符",
                "value": "x" * 256,
                "should_save": True,
                "should_error": False,
                "description": "最大允许长度（边界值）",
                "expected": "成功保存",
            },
            {
                "type": "length_over",
                "name": "超长257字符",
                "value": "y" * 257,
                "should_save": False,
                "should_error": True,
                "description": "超过最大长度（边界值+1）",
                "expected": "被截断或显示错误",
            },
            {
                "type": "length_over",
                "name": "极长300字符",
                "value": "z" * 300,
                "should_save": False,
                "should_error": True,
                "description": "远超最大长度",
                "expected": "被截断或显示错误",
            },
            
            # ========== 4. 必填验证（1个场景） ==========
            {
                "type": "required_empty",
                "name": "空值验证",
                "value": "",
                "should_save": False,
                "should_error": True,
                "description": "空值（必填字段）",
                "expected": "显示必填错误",
            },
        ]
        
        validation_results = []
        
        # 执行测试场景
        for idx, scenario in enumerate(test_scenarios, 1):
            logger.info("")
            logger.info("=" * 70)
            logger.info(f"场景 {idx}/{len(test_scenarios)}: {scenario['name']}")
            logger.info("=" * 70)
            logger.info(f"  输入值: '{scenario['value'][:50]}{'...' if len(scenario['value']) > 50 else ''}'")
            logger.info(f"  长度: {len(scenario['value'])} 字符")
            logger.info(f"  描述: {scenario['description']}")
            logger.info(f"  预期: {scenario['expected']}")
            
            # 刷新页面确保干净状态
            profile_page.page.reload()
            profile_page.page.wait_for_load_state("domcontentloaded")
            profile_page.page.wait_for_timeout(2000)
            
            # 输入测试值
            profile_page.fill_input(profile_page.USERNAME_INPUT, scenario['value'])
            
            # 截图1：输入后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = scenario['name'].replace(' ', '_').replace('/', '_')
            screenshot_path = f"username_{safe_name}_input_{timestamp}.png"
            profile_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{screenshot_idx}-{scenario['name']}_输入后",
                attachment_type=allure.attachment_type.PNG
            )
            screenshot_idx += 1
            
            # 点击保存
            profile_page.click_element(profile_page.SAVE_BUTTON)
            profile_page.page.wait_for_load_state("networkidle")
            profile_page.page.wait_for_timeout(2000)
            
            # 检查是否有错误提示
            has_error = False
            error_message = ""
            try:
                # 检查HTML5验证错误
                validation_info = profile_page.page.evaluate(f"""
                    (() => {{
                        const el = document.querySelector("{profile_page.USERNAME_INPUT}");
                        return {{
                            valid: el ? el.validity.valid : null,
                            message: el ? el.validationMessage : '',
                            valueMissing: el ? el.validity.valueMissing : null,
                            patternMismatch: el ? el.validity.patternMismatch : null,
                            tooLong: el ? el.validity.tooLong : null,
                        }};
                    }})()
                """)
                
                if validation_info and not validation_info['valid']:
                    has_error = True
                    error_message = validation_info['message']
                    logger.info(f"  ✓ 检测到HTML5验证错误: {error_message}")
                
                # 检查页面错误提示
                error_selectors = [".invalid-feedback", ".text-danger", "[role='alert'].text-danger"]
                for selector in error_selectors:
                    if profile_page.is_visible(selector):
                        error_text = profile_page.get_text(selector)
                        if error_text:
                            has_error = True
                            error_message += f" | {error_text}"
                            logger.info(f"  ✓ 检测到页面错误提示: {error_text}")
            except Exception as e:
                logger.warning(f"  检查错误时出现异常: {e}")
            
            # 截图2：保存后（带错误检查）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"username_{safe_name}_saved_{timestamp}.png"
            profile_page.take_screenshot(screenshot_path)
            
            # 生成截图描述（统一格式）
            expected_str = "成功" if scenario['should_save'] else "失败"
            actual_str = "成功" if not has_error else "失败"
            error_expected_str = "无错误" if not scenario['should_error'] else "有错误"
            error_actual_str = "无错误" if not has_error else "有错误"
            
            screenshot_desc = f"{screenshot_idx}-{scenario['name']}_保存后（预期:{expected_str}/{error_expected_str}, 实际:{actual_str}/{error_actual_str}）"
            
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=screenshot_desc,
                attachment_type=allure.attachment_type.PNG
            )
            screenshot_idx += 1
            
            # 刷新验证
            profile_page.page.reload()
            profile_page.page.wait_for_load_state("domcontentloaded")
            profile_page.page.wait_for_timeout(2000)
            
            # 获取保存后的值
            saved_value = profile_page.get_username_value()
            is_saved = saved_value == scenario['value']
            
            # 判断结果
            save_match = is_saved == scenario['should_save']
            error_match = has_error == scenario['should_error']
            overall_match = save_match and error_match
            
            # 记录结果
            logger.info(f"")
            logger.info(f"  实际结果:")
            logger.info(f"    - 保存状态: {'成功保存' if is_saved else '未保存/被修改'}")
            logger.info(f"    - 保存值: '{saved_value[:50]}{'...' if len(saved_value) > 50 else ''}'")
            logger.info(f"    - 错误提示: {'有' if has_error else '无'} {f'({error_message})' if error_message else ''}")
            logger.info(f"")
            logger.info(f"  结果判断:")
            logger.info(f"    - 保存预期: {scenario['should_save']}，实际: {is_saved}，{'✅匹配' if save_match else '❌不匹配'}")
            logger.info(f"    - 错误预期: {scenario['should_error']}，实际: {has_error}，{'✅匹配' if error_match else '❌不匹配'}")
            logger.info(f"    - 综合结果: {'✅ 通过' if overall_match else '❌ 失败'}")
            
            # 如果是无效场景但没有错误提示，标记为前端bug
            if scenario['should_error'] and not has_error:
                logger.error(f"  ⚠️ 前端BUG：无效输入未显示错误提示！")
            
            validation_results.append({
                "scenario": scenario['name'],
                "type": scenario['type'],
                "input": scenario['value'],
                "input_length": len(scenario['value']),
                "saved": saved_value,
                "saved_length": len(saved_value) if saved_value else 0,
                "expected_save": scenario['should_save'],
                "actually_saved": is_saved,
                "expected_error": scenario['should_error'],
                "actually_error": has_error,
                "error_message": error_message,
                "match": overall_match
            })
        
        # 恢复原始用户名
        logger.info("")
        logger.info("=" * 70)
        logger.info(f"恢复原始Username: '{original_username}'")
        logger.info("=" * 70)
        profile_page.page.reload()
        profile_page.page.wait_for_load_state("domcontentloaded")
        profile_page.page.wait_for_timeout(2000)
        profile_page.fill_input(profile_page.USERNAME_INPUT, original_username)
        profile_page.click_element(profile_page.SAVE_BUTTON)
        profile_page.page.wait_for_load_state("networkidle")
        profile_page.page.wait_for_timeout(2000)
        
        # 输出测试结果汇总
        logger.info("")
        logger.info("=" * 80)
        logger.info("Username字段验证结果汇总")
        logger.info("=" * 80)
        logger.info("| 场景 | 类型 | 长度 | 保存预期 | 保存实际 | 错误预期 | 错误实际 | 结果 |")
        logger.info("|------|------|------|----------|----------|----------|----------|------|")
        for r in validation_results:
            scenario_short = r['scenario'][:15]
            type_short = r['type'].split('_')[0][:6]
            save_exp = "✓" if r['expected_save'] else "✗"
            save_act = "✓" if r['actually_saved'] else "✗"
            err_exp = "✓" if r['expected_error'] else "✗"
            err_act = "✓" if r['actually_error'] else "✗"
            result = "✅" if r['match'] else "❌"
            logger.info(f"| {scenario_short:15} | {type_short:6} | {r['input_length']:4} | {save_exp:8} | {save_act:8} | {err_exp:8} | {err_act:8} | {result:4} |")
        
        # 统计通过率
        passed = sum(1 for r in validation_results if r['match'])
        total = len(validation_results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        logger.info("")
        logger.info(f"总体通过率: {passed}/{total} ({pass_rate:.1f}%)")
        logger.info("=" * 80)
        
        logger.info("TC-VALID-USERNAME-001执行完成")
'''

# 保存模板
with open('tools/username_validation_template.txt', 'w', encoding='utf-8') as f:
    f.write(username_test_template)

print("✅ Username验证用例模板已生成: tools/username_validation_template.txt")
print(f"模板长度: {len(username_test_template.split(chr(10)))} 行")

