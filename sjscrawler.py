import shenjian

user_key = "751bf29858-YzNjZmZjMT"
user_secret = "Q3NTFiZjI5ODU4Zj-f172b4a46cc3cff"

service = shenjian.Service(user_key,user_secret)
result = service.get_money_info()
print(result)
result = service.get_node_info()
print(result)
result = service.get_app_list(page=1, page_size=30)
print(result['data']['list'])
