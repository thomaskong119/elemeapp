import sendmsg

dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'

# sendmsg.sendmsg('18676559554','测试测试')

sendmsg.sendding(dingurl,'18676559554','测试测试')