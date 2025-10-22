import time, random, requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By


def handle_scraping(
    url:str,
    link:str,
) -> Dict[str, Any]:
    options = webdriver.ChromeOptions()

    # Prepare chrome to look more human
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.set_capability("browserName", "chrome")
    options.add_argument("--window-size=1200,800")

    try:
        main_driver = webdriver.Remote(command_executor=url, options=options)
        main_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # Hide driver from detection

        main_driver.get(link)

        time.sleep(random.randint(5, 8))

        page_body = main_driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")

        return {
            'success': True,
            'data': page_body,
            'error': None,
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f'{e}',
        }


def check_health(
    link:str,
) -> Dict[str, Any]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(link, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        if not soup.body:
            raise ValueError("No <body> tag found in HTML, content may not have rendered correctly.")

        return {
            "success": True,
            "data": link,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "data": link,
            "error": str(e),
        }
