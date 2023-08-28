import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# path = r'C:\Users\User\IdeaProjects\project1\Bsport\SEO日报\chromedriver.exe'
# chrome_options.binary_location = path
#
# url = 'http://localhost:9881/create/countall?end_date=20230815&max_results=9999&out_put_path=C%3A%5CUsers%5CUser%5CDesktop%5CSEO%5C_0815%5C&start_date=20230815'
url2 = 'http://localhost:9881/swagger-ui/index.html#/Mason%20Excel%20%E4%BA%A7%E7%94%9F/index2UsingPOST'
# driver = webdriver.Chrome()
# driver = webdriver.Edge()
# driver.get(url2)
# # browser = driver.get(url = url2)
# browser = webdriver.Chrome(options=chrome_options)
# browser.get(url2)
path = r'C:\Users\User\IdeaProjects\project1\Bsport\SEO日报\chromedriver.exe'
browser = webdriver.Chrome()
# button = browser.find_element(By.XPATH,'//div[@class="try-out"]/button')
# button.click()
browser.get(url2)
import time
time.sleep(5)
# button = browser.find_elements(By.XPATH,'//div[@class="try-out"]/button[0]')
#
# input = browser.find_elements(By.XPATH,'//div[@class="renderedMarkdown"]/input[0]')
# button = browser.find_element(By.XPATH,'//div[@class="try-out"]/button')
# button.click()
# input = browser.find_element(By.XPATH,'//div[@class="renderedMarkdown"]/input')
# input.send_keys('20230815')
# input = browser.find_element(By.XPATH,'//div[@class="renderedMarkdown"]/input[2]')
# input.send_keys('9999')


browser.quit()