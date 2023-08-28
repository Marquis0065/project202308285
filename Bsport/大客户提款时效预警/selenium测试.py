from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import hmac, base64, struct, hashlib

def get_google_code(secret):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", int(time.time()) // 30)
    google_code = hmac.new(key, msg, hashlib.sha1).digest()
    # 很多网上的代码不可用，就在于这儿，没有chr字符串
    o = ord(chr(google_code[19])) & 15
    # google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
    google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
    return '%06d' % google_code

# 生成验证码
google_code = get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')

submit_url = 'http://fundmng.bsportsadmin.com/api/manage/user/admin/login/submit'
browser = webdriver.Chrome()
browser.get('http://fundmng.bsportsadmin.com/login')
time.sleep(1)
user_input = browser.find_element(By.ID,'login_username')
user_input.send_keys('Marquis')
time.sleep(1)
pw_input = browser.find_element(By.ID,'login_password')
pw_input.send_keys('qwer123456')
time.sleep(1)
code_input = browser.find_element(By.ID,'login_code')
code_input.send_keys(google_code)
time.sleep(1)
button = browser.find_element(By.TAG_NAME,'button')
button.click()
# 等待页面加载完成
browser.implicitly_wait(10)
response = browser.page_source
print(response)
print(browser.get_cookies())
print(browser.get_log('browser'))

