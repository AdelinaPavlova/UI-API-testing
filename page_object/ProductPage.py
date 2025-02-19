from playwright.sync_api import Page


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_1 = page.locator(
            "body > section > div > div.row > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.product-overlay > div > a")
        self.product_2 = page.locator(
            "body > section > div > div.row > div.col-sm-9.padding-right > div > div:nth-child(4) > div > div.single-products > div.product-overlay > div > a")
        self.product_1_hover = page.locator("//div[@class='productinfo text-center']/a[@data-product-id = '1']")
        self.product_2_hover = page.locator("//div[@class='productinfo text-center']/a[@data-product-id = '8']")

    def _close_window(self):
        self.page.get_by_role("button", name="Continue Shopping").click()

    def open_page(self):
        self.page.get_by_role("link", name=" Products").click()

    def brands(self, brand_name):
        self.page.get_by_role("link", name=brand_name).click()

    def add_products(self):
        self.page.locator("(//div[@class='productinfo text-center'])[1]").hover()
        self.page.locator(
            "body > section > div > div.row > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.product-overlay > div > a").click()
        self._close_window()
        self.page.locator("(//div[@class='productinfo text-center'])[2]").hover()
        self.page.locator(
            "body > section > div > div.row > div.col-sm-9.padding-right > div > div:nth-child(4) > div > div.single-products > div.product-overlay > div > a").click()
        self._close_window()
