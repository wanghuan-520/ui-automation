"""
重构测试文件：删除冗余测试用例
"""
import re

# 读取原文件
with open('tests/aevatar_station/test_profile_personal_settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 要删除的测试方法名
tests_to_delete = [
    'test_p2_profile_input_validation',
    'test_p1_profile_field_length_boundary',
    'test_p1_profile_required_fields',
    'test_p2_profile_email_edit_validation',
    'test_p2_phone_field_invalid_input',
    'test_p2_all_fields_max_length',
    'test_p2_all_fields_min_length_and_char_type',
]

# 找到每个测试方法的起止行号
test_ranges = []
current_test = None
test_start = None
indent_level = None

for i, line in enumerate(lines):
    # 检测测试方法开始
    match = re.match(r'(\s*)def (test_\w+)\(', line)
    if match:
        # 保存上一个测试的结束位置
        if current_test and current_test in tests_to_delete:
            test_ranges.append((test_start, i - 1, current_test))
        
        # 开始新的测试
        indent_level = len(match.group(1))
        current_test = match.group(2)
        test_start = i
        
        # 回退到找到前面的@pytest.mark装饰器
        j = i - 1
        while j >= 0:
            if lines[j].strip().startswith('@pytest.mark'):
                test_start = j
                j -= 1
            elif lines[j].strip() == '' or lines[j].strip().startswith('#'):
                j -= 1
            else:
                break

# 处理最后一个测试
if current_test and current_test in tests_to_delete:
    test_ranges.append((test_start, len(lines) - 1, current_test))

print(f"找到 {len(test_ranges)} 个要删除的测试:")
for start, end, name in test_ranges:
    print(f"  - {name}: 行 {start+1} - {end+1} ({end-start+1} 行)")

# 生成新文件内容（删除指定的测试方法）
new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    # 检查是否在删除范围内
    in_delete_range = False
    for start, end, name in test_ranges:
        if start <= i <= end:
            in_delete_range = True
            skip_until = end
            break
    
    if not in_delete_range:
        new_lines.append(line)

# 写入新文件
with open('tests/aevatar_station/test_profile_personal_settings_refactored.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n原文件行数: {len(lines)}")
print(f"新文件行数: {len(new_lines)}")
print(f"删除行数: {len(lines) - len(new_lines)}")
print(f"\n✅ 新文件已生成: tests/aevatar_station/test_profile_personal_settings_refactored.py")

