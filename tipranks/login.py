from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from .errors import (
	TipRanksLoginError
)

from selenium import webdriver
from selenium_stealth import stealth


class TipRanksLogin:
	def __init__(self, email, password):
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
		options.add_experimental_option("useAutomationExtension", False)
		self.driver = webdriver.Chrome(options=options)

		stealth(
			self.driver,
			languages=["en-US", "en"],
			vendor="Google Inc.",
			platform="Win32",
			webgl_vendor="Intel Inc.",
			renderer="Intel Iris OpenGL Engine",
			fix_hairline=True,
		)

		self.email = email
		self.password = password

	def login(self):
		self.driver.get("https://www.tipranks.com/sign-in?redirectTo=%2F")

		try:
			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
			).send_keys(self.email)

			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
			).send_keys(self.password)

			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, "client-templates-loginPage-styles__submitButton"))
			).click()

		except TimeoutException:
			raise TipRanksLoginError("Failed To Find Login Elements")

		try:
			WebDriverWait(self.driver, 3).until(
				EC.presence_of_element_located((By.XPATH, "//label[@for='popupUserBox']"))
			)

		except TimeoutException:
			self.driver.quit()
			raise TipRanksLoginError("Failed To Login, Check Credentials")

		self.driver.refresh()
		login = self.find_cookies()

		if not login:
			self.driver.quit()
			raise TipRanksLoginError("Failed To Login, Check Credentials")

		return self.format_cookies()

	def format_cookies(self):
		browser_cookies = self.driver.get_cookies()
		cookies = ""

		for cookie in browser_cookies:
			cookies += f"{cookie['name']}={cookie['value']}; "

		self.driver.quit()

		return cookies

	def find_cookies(self):
		cookies = self.driver.get_cookies()

		return [True for cookie in cookies if cookie["name"] == "token"][0]