from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {
 'browser': 'IE',
 'browser_version': '11.0',
 'os': 'Windows',
 'os_version': '10',
 'resolution': '1024x768',
 'name': 'Bstack-[Python] Sample Test'
}

driver = webdriver.Remote(
    command_executor='http://mathieuferrandea1:xnFQ16hcVF8PJP5ttDTh@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

driver.get("https://projet13.mathieuferrandeau.fr/")
if not "GERER-MON-BUDGET.FR" in driver.title:
    raise Exception("Unable to load https://projet13.mathieuferrandeau.fr/")
print(driver.title)
driver.quit()
