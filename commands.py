from command.pictools import create, delete_1, delete_2, upload, show_1, show_2, show_3
# 处理用户的指令
# 处理用户的指令
def process_command(message_content, toUserName):
    try:
        parts = message_content.split()
        command = parts[0]

        if command == "/create" and len(parts) == 2:
            album_name = parts[1]
            return create(album_name), None

        elif command == "/删除" and len(parts) == 3:
            if "相册" in parts[1]:
                album_name = parts[2]
                return delete_1(album_name), None
            elif "图片" in parts[1]:
                photo_name = parts[2] + ".png"
                return delete_2(photo_name), None

        elif command == "/help":
            return (
                "指令格式如下：\n/create {相册名称} 创建一个相册\n/删除 相册 {相册名称} 删除一个相册\n/删除 图片 {照片名称} 删除一张照片\n/上传 {图片名称} {相册名称} 上传一张图片到指定相册\n/show 展示所有相册\n/show 相册 {相册名称} 展示指定相册内的所有照片\n/show 图片 {照片名称} 获取指定照片",
                None,
            )

        elif command == "/上传" and len(parts) == 3:
            photo_name = parts[1]
            album_name = parts[2]
            upload_msg= upload(photo_name, album_name)
            return upload_msg, None

        elif command == "/show" and len(parts) == 1:
            return show_1(), None

        elif command == "/show" and len(parts) == 3:
            if "相册" in parts[1]:
                album_name = parts[2]
                return show_2(album_name), None
            elif "图片" in parts[1]:
                photo_name = parts[2] + ".png"
                return None, show_3(photo_name)

    except Exception as e:
        # 捕获异常并将其转换为字符串返回
        return f"An error occurred: {str(e)}", None

    return None, None


# 处理图片消息
def handle_picture(msg):
    from upload_state import upload_state

    if upload_state['waiting']:
        photo_name = upload_state['photo_name']
        album_name = upload_state['album_name']
        save_path = f"./datas/相册/{album_name}/{photo_name}.png"

        msg.download(save_path)
        upload_state['received'] = True
        return f"图片 '{photo_name}' 接收成功，保存到相册 '{album_name}' 中。"
    return None
