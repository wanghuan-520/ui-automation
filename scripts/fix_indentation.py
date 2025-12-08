lines = []
with open('tests/aevatar_station/test_profile_change_password.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 test_p1_password_length_boundary 的装饰器开始位置
start_index = -1
for i, line in enumerate(lines):
    if '@pytest.mark.boundary' in line and 'def test_p1_password_length_boundary' in lines[i+2]:
        start_index = i
        break
    # 兼容另一种可能（取决于P1在哪里）
    if '@pytest.mark.P1' in line and '@pytest.mark.boundary' in lines[i+1]:
        start_index = i
        break

if start_index != -1:
    # 从 start_index 开始，直到下一个方法的定义（test_p2...）
    # 或者简单点，我们知道直到文件末尾或者某个特定标记
    # 我们只需修正缩进。所有顶格或缩进错误的行，都加 4 个空格。
    
    # 实际上，之前插入的代码缩进是 4 空格，但在类 TestChangePassword 下应该是 4 空格。
    # 等等，类本身顶格，方法应该缩进 4 空格。
    # 之前的脚本插入的代码本身带有 4 空格缩进。
    
    # 让我们看看 761 行：
    # 761:         @pytest.mark.P1  (8 spaces? no, class methods usually 4 spaces)
    # class TestChangePassword:
    #     def method(): ...
    
    # 让我们读取类定义的缩进。
    # 看来我在脚本里插入时，new_method 的第一行有缩进，但后续行没有对齐？
    
    # 直接暴力修复：
    # 读取 761 行到下一个方法定义之间的所有行，确保它们都相对于类有正确的缩进（4空格）。
    
    # 重新读取并重写
    pass

# 更简单的：用正则替换修正
import re
content = "".join(lines)

# 修正缩进错误
# 查找那段代码
pattern = r'(    @pytest\.mark\.boundary\n    @pytest\.mark\.parametrize)'
# 应该是
#     @pytest.mark.P1
#     @pytest.mark.boundary
# ...

# 让我们再看一次文件内容截图
# 761:         @pytest.mark.P1
# 762:     @pytest.mark.boundary

# 761 有 8 个空格（因为上一段代码是 TC-PWD-005执行成功，在方法内，所以可能有误解？）
# 不，上一个方法结束了。
# 类的方法应该有 4 个空格缩进。

# 修正逻辑：将该方法的所有行都统一缩进为 4 空格。
new_lines = []
in_target_method = False
for line in lines:
    if '@pytest.mark.P1' in line and 'def test_p1_password_length_boundary' in "".join(lines[lines.index(line):lines.index(line)+5]):
        in_target_method = True
        # 这一行本身可能缩进不对，强制设为 4 空格
        new_lines.append("    @pytest.mark.P1\n")
        continue
        
    if in_target_method:
        if 'def test_p2_password_complexity_requirements' in line:
            in_target_method = False
            new_lines.append(line)
            continue
        
        # 处理目标方法内的行
        stripped = line.lstrip()
        if stripped:
            new_lines.append("    " + stripped)
        else:
            new_lines.append("\n")
    else:
        new_lines.append(line)

with open('tests/aevatar_station/test_profile_change_password.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

