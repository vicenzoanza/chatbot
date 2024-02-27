from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.189 Safari/537.36")



driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = opts
)

driver.get('https://www.promptior.ai/about')

sleep(3)

elemento = driver.find_element(By.XPATH, '//div[@class="text-section"]')

texto = elemento.text

with open("informacion/informacion.txt", "w", encoding="utf-8") as f:
    f.write(texto)