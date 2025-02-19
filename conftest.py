import json
import logging.config
import os
from os import path

import allure
from playwright.sync_api import sync_playwright
from module_7_playwright.api import AutomationApi
from module_7_playwright.settings import config
from module_7_playwright.utils.fake import Fake
import pytest


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(log_file_path)
USER_DATA_FILE = os.path.join('C:/Users/tanai/PycharmProjects/autotesty_python_advanced/module_7_playwright',
                              "user_data.json")

pytest_plugins = [
    "module_7_playwright.src.fixtures",
    "module_7_playwright.src.actions.base",
]


@pytest.fixture(scope="session")
def web():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        yield page
        browser.close()


@pytest.fixture(scope="module")
def api():
    return AutomationApi(base_url=config()['source']['api_url'])


def pytest_runtest_makereport(item, call) -> None:
    if call.when == "call":
        if call.excinfo is not None and "page" in item.funcargs:
            page = item.funcargs["page"]
            allure.attach(page.screenshot(type="png"),
                          name=f'{item.nodeid}.png',
                          attachment_type=allure.attachment_type.PNG,)

@pytest.fixture(scope="module")
def user_info():
    fake = Fake()

    data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=6),
        "title": fake.title(),
        "birth_date": fake.birth_date(),
        "birth_month": fake.birth_month(),
        "birth_year": fake.birth_year(),
        "firstname": fake.name(),
        "lastname": fake.name(),
        "company": fake.name(),
        "address1": fake.address(),
        "address2": fake.address(),
        "country": fake.country(),
        "zipcode": fake.zipcode(),
        "state": fake.city(),
        "city": fake.city(),
        "mobile_number": fake.mobile_number(),
    }

    print(f"Создание пользователя с данными: {data}")
    return data


@pytest.fixture(scope="module")
def create_user(api, user_info):
    response = api.create_user(user_data=user_info)
    assert response.status_code in [200, 201], f"Ошибка при создании пользователя: {response.text}"
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_info, f, indent=4)
    return user_info


@pytest.fixture(scope="module")
def web_auth(api):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        with open(USER_DATA_FILE, "r") as f:
            user_info = json.load(f)
        page.goto(("https://www.automationexercise.com/login"), timeout=60000)
        page.fill('input[data-qa="login-email"]', user_info["email"])
        page.fill('input[data-qa="login-password"]', user_info["password"])
        page.click("button[data-qa='login-button']")

        cookies = context.cookies()
        yield page, cookies, user_info

        browser.close()
