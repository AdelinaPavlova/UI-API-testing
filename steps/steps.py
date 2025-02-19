from playwright.sync_api import Page
from module_7_playwright.page_object.CartPage import CartPage
from module_7_playwright.page_object.ProductPage import ProductPage
import allure

class Steps:
    def __init__(self, page: Page):
        self.page = page
        self.product_page = ProductPage(page)
        self.cart_page = CartPage(page)
    @allure.step("Открыта страница с товарами")
    def open_product_page(self):
        self.product_page.open_page()

    @allure.step("Выбран бренд {brand_name}")
    def brand_choice(self, brand_name):
        self.product_page.brands(brand_name)

    @allure.step("Товары добавлены в корзину")
    def add_to_cart(self):
        self.product_page.add_products()

    @allure.step("Открыта страница корзины")
    def go_to_cart(self):
        self.cart_page.go_to_user_cart()

    @allure.step("Выполнено размещение заказа")
    def place_order(self):
        self.cart_page.order()

    @allure.step("Заполнена информация для платежей")
    def input_payment_info(self):
        self.cart_page.add_info()

    @allure.step("Скачан файл с информацией о заказе")
    def download_invoice(self):
        return self.cart_page.invoice()

    @allure.step("Проверен файл с информацией о заказе")
    def check_invoice(self, user_info):
        invoice_content = self.download_invoice()
        self.cart_page.assertion(invoice_content, user_info)
