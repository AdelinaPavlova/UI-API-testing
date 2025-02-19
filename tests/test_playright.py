import pytest
from module_7_playwright.steps.steps import Steps
import allure


@allure.title("e2e тест создания заказа")
@allure.suite("Базовые тесты")
@pytest.mark.parametrize("brand_name", ["(6) Polo", "(5) H&M"])
def test_e2e_shopping(api, user_info, create_user, web_auth, brand_name):
    page, cookies, user_info = web_auth
    steps = Steps(page)
    steps.open_product_page()
    steps.brand_choice(brand_name)
    steps.add_to_cart()
    steps.go_to_cart()
    steps.place_order()
    steps.input_payment_info()
    steps.download_invoice()
    steps.check_invoice(user_info)
