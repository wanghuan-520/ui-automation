with open('tests/aevatar_station/test_profile_change_password.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 错误的片段（761-764行）
wrong_snippet = """        @pytest.mark.P1
    @pytest.mark.boundary
    @pytest.mark.parametrize("test_case", BOUNDARY_TEST_CASES, ids=lambda x: x["description"])
    def test_p1_password_length_boundary(self, logged_in_change_password_page, request, test_case):"""

# 正确的片段（统一4空格）
correct_snippet = """    @pytest.mark.P1
    @pytest.mark.boundary
    @pytest.mark.parametrize("test_case", BOUNDARY_TEST_CASES, ids=lambda x: x["description"])
    def test_p1_password_length_boundary(self, logged_in_change_password_page, request, test_case):"""

if wrong_snippet in content:
    new_content = content.replace(wrong_snippet, correct_snippet)
    with open('tests/aevatar_station/test_profile_change_password.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed indentation.")
else:
    print("Snippet not found. Checking variations...")
    # 尝试模糊匹配或手动查找
    # 可能是 8 空格 P1, 4 空格 boundary
    # 无论如何，我们把整个文件里这段乱的缩进修好
    pass

