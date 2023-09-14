from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

url = 'http://localhost:9881/swagger-ui/index.html#/Mason%20Excel%20%E4%BA%A7%E7%94%9F/index2UsingPOST'

# path = r'C:\Users\User\IdeaProjects\project1\Bsport\SEO日报\chromedriver.exe'
browser = webdriver.Chrome()
browser.get(url)
time.sleep(5)
button = browser.find_element(By.XPATH,'//div[@class="try-out"]/button')
button.click()
time.sleep(3)
input = browser.find_elements(By.XPATH,'//input')
input[0].send_keys('20230816')
time.sleep(3)
outpath = r'C:\Users\User\Desktop\SEO\_0816'+'\\'
input[2].send_keys(9999)
time.sleep(3)
input[4].send_keys(outpath)
time.sleep(3)
input[5].send_keys('20230816')
textarea = browser.find_element(By.TAG_NAME,'textarea')
textarea.clear()
text = '''[
{
    "accessToken": "eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhY2MiLCJhdWQiOiLnmb7luqbnu5_orqEiLCJ1aWQiOjMxNTYxMjMyLCJhcHBJZCI6IjEzYmQ1MDQ5YTY3NmQxMDczNzk1OTkzMjEwMmVjNTU3IiwiaXNzIjoi5ZWG5Lia5byA5Y-R6ICF5Lit5b-DIiwicGxhdGZvcm1JZCI6IjQ5NjAzNDU5NjU5NTg1NjE3OTQiLCJleHAiOjE2OTM3MzEyMzAsImp0aSI6Ijc3NzIwNjA3MDMwMjMyMTA0OTYifQ.yltXMOcGruPmi7u39JYYOGZv44Y6LzHgmdTA9XLv4ow6fjavMu9WoNlYPw9m2tPq",
    "userName": "connerseo"
},{
    "accessToken": "eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhY2MiLCJhdWQiOiLnmb7luqbnu5_orqEiLCJ1aWQiOjM4NTQ4NDk2LCJhcHBJZCI6IjEzYmQ1MDQ5YTY3NmQxMDczNzk1OTkzMjEwMmVjNTU3IiwiaXNzIjoi5ZWG5Lia5byA5Y-R6ICF5Lit5b-DIiwicGxhdGZvcm1JZCI6IjQ5NjAzNDU5NjU5NTg1NjE3OTQiLCJleHAiOjE2OTM3OTQ2NDIsImp0aSI6Ijc3NzIwOTU3ODQzMTYxMTY5OTQifQ.l0_u8ZDE83jcHno9D4XSCDyUhUDdzViuAk5vP4u4p9Yy6I_CMSNAGNBL-iPOlB50",
    "userName": "BSEOtongji"
},{
    "accessToken": "eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhY2MiLCJhdWQiOiLnmb7luqbnu5_orqEiLCJ1aWQiOjQwNzk5NTY5LCJhcHBJZCI6IjEzYmQ1MDQ5YTY3NmQxMDczNzk1OTkzMjEwMmVjNTU3IiwiaXNzIjoi5ZWG5Lia5byA5Y-R6ICF5Lit5b-DIiwicGxhdGZvcm1JZCI6IjQ5NjAzNDU5NjU5NTg1NjE3OTQiLCJleHAiOjE2OTM3OTQ3NjQsImp0aSI6Ijc3NzIwOTI2OTE5Mzk2NDc0OTcifQ.WGc7BT2qsUebCzcRV3RNVxC58mGxM2net2HW-LX-hDk7xQhNTi91P_IvRnScs2s7",
    "userName": "BTONGJi1"
}
]'''
textarea.send_keys(text)
time.sleep(5)
Execute = browser.find_element(By.XPATH,'//button[@class="btn execute opblock-control__btn"]')
Execute.click()
time.sleep(500)
browser.quit()