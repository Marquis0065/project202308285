import requests
# submit :http://fundmng.bsportsadmin.com/api/manage/user/admin/login/submit
## Cookie:admin-uid=690; admin-token=94d926a0f52c4325b22b2ccef72b5051

# list : http://fundmng.bsportsadmin.com/api/manage/system/auth/init/system/list    4e4380eda18f46e3af36cf2452947a00
def get_request_headers(url, username, password,code):
    # 创建一个Session对象
    session = requests.Session()
    # 构造登录请求的数据
    data = {
        'username': username,
        'password': password,
        'code':code
    }

    # 发送POST请求并保存登录后的Cookie
    session.post(url, data=data)

    # 获取保存的Cookie信息
    headers = session.cookies.get_dict()

    return headers

# 示例用法
url = 'https://example.com/login'
username = 'your_username'
password = 'your_password'

headers = get_request_headers(url, username, password)
print(headers)