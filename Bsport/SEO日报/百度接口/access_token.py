import requests

# 替换为你的App Key和App Secret
app_key = "rCcSsGGfuu10lHFAPmBGsRunpp9wha09"
app_secret = "apNWQFX57OvLQvW7E5wyD8oWHdhyboqx"

# 构造请求URL
url = "https://openapi.baidu.com/oauth/2.0/token"
params = {
    "grant_type": "client_credentials",
    "client_id": app_key,
    "client_secret": app_secret
}

# 发送请求并获取access-token
response = requests.get(url, params=params)
data = response.json()
access_token = data["access_token"]

print(access_token)