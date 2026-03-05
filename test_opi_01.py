import pytest
import requests
import yaml
import allure  # 引入 allure 库


def read_test_data():
    with open("test_data.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [(item['user_id'], item['expected_name']) for item in data]


# Allure 报告层级：Epic (史诗/大项目) -> Feature (功能模块) -> Story (用户故事/子功能)
@allure.epic("JSONPlaceholder 开放接口测试项目")
@allure.feature("用户管理模块")
@allure.story("获取单个用户信息接口")
@pytest.mark.parametrize("user_id, expected_name", read_test_data())
def test_get_user_info(user_id, expected_name):
    # 动态在报告里生成每次测试的具体标题
    allure.dynamic.title(f"验证获取用户ID为 {user_id} 的信息")

    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    # 记录执行步骤，这些文字都会出现在最终的网页报告里
    with allure.step(f"第一步: 发送 GET 请求到 {url}"):
        response = requests.get(url)
        status_code = response.status_code
        re_data = response.json()

    with allure.step("第二步: 验证响应状态码"):
        assert status_code == 200, f"实际状态码是: {status_code}"

    with allure.step("第三步: 验证响应数据结构"):
        assert "name" in re_data, "name不在返回数据中"

    with allure.step(f"第四步: 验证用户姓名是否等于 {expected_name}"):
        user_name = re_data['name']
        assert user_name == expected_name, f"名字不匹配！预期: {expected_name}, 实际: {user_name}"