import itchat
from itchat.content import TEXT, PICTURE
from commands import process_command, handle_picture
import threading

# 定义一个函数来处理私聊文本消息
@itchat.msg_register(TEXT)
def reply(msg):
    sender_name = msg['User']['NickName']
    message_content = msg['Text']
    print(f"Received message from {sender_name}: {message_content}", flush=True)
    
    # 在独立线程中处理指令
    threading.Thread(target=process_text_message, args=(msg,)).start()

# 处理文本消息的函数
def process_text_message(msg):
    response, image_path = process_command(msg['Text'], toUserName=msg['FromUserName'])
    if response:
        itchat.send(response, toUserName=msg['FromUserName'])
        
    # 处理需要发送的图片
    if image_path:
        itchat.send_image(fileDir=image_path, toUserName=msg['FromUserName'])

# 定义一个函数来处理图片消息
@itchat.msg_register(PICTURE)
def picture_reply(msg):
    # 在独立线程中处理图片
    threading.Thread(target=process_picture_message, args=(msg,)).start()

# 处理图片消息的函数
def process_picture_message(msg):
    response = handle_picture(msg)
    if response:
        itchat.send(response, toUserName=msg['FromUserName'])

# 启动微信机器人
itchat.auto_login(hotReload=False)

# 启动微信机器人监听消息
itchat.run()
