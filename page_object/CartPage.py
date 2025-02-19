from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page
        self.info = {
            "name_on_card": "123`123`13`",
            "card_number": "`123`3`323`133",
            "ex.": "111",
            "MM": "11",
            "YYYY": "1111"
        }

    def get_payment_info(self):
        return self.info

    def go_to_user_cart(self):
        self.page.get_by_role("link", name=" Cart").click()

    def order(self):
        self.page.get_by_text("Proceed To Checkout").click()
        self.page.get_by_role("link", name="Place Order").click()

    def add_info(self):
        payment_info = self.get_payment_info()
        self.page.locator("input[name=\"name_on_card\"]").click()
        self.page.locator("input[name=\"name_on_card\"]").fill(payment_info["name_on_card"])
        self.page.locator("input[name=\"card_number\"]").click()
        self.page.locator("input[name=\"card_number\"]").fill(payment_info["card_number"])
        self.page.get_by_placeholder("ex.").click()
        self.page.get_by_placeholder("ex.").fill(payment_info["ex."])
        self.page.get_by_placeholder("MM").dblclick()
        self.page.get_by_placeholder("MM").fill(payment_info["MM"])
        self.page.get_by_placeholder("YYYY").click()
        self.page.get_by_placeholder("YYYY").fill(payment_info["YYYY"])
        self.page.get_by_role("button", name="Pay and Confirm Order").click()

    def invoice(self):
        with self.page.expect_download() as download_info:
            self.page.get_by_role("link", name="Download Invoice").click()
        download = download_info.value
        download.save_as('file.txt')
        downloaded_file_path = download.path()
        with open(downloaded_file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            return text_content

    def assertion(self, invoice_content, user_info):
        assert invoice_content.startswith(
            f'Hi {user_info["firstname"]} {user_info["lastname"]}') and 'Your total purchase' in invoice_content
