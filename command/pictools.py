import os,time
from upload_state import upload_state
import shutil  # 需要引入shutil库

ALBUMS_PATH = "datas/相册/"  # 请根据实际路径调整

def create(album_name):
    path = os.path.join(ALBUMS_PATH, album_name)
    if not os.path.exists(path):
        os.makedirs(path)
        return f"相册 '{album_name}' 创建成功！"
    else:
        return f"相册 '{album_name}' 已存在！"

def delete_1(album_name):
    path = os.path.join(ALBUMS_PATH, album_name)
    if os.path.exists(path):
        try:
            # 递归删除文件夹及其中的所有内容
            shutil.rmtree(path)
            return f"相册 '{album_name}' 删除成功！"
        except Exception as e:
            # 捕获删除过程中可能的异常
            return f"删除相册 '{album_name}' 失败：{str(e)}"
    else:
        return f"相册 '{album_name}' 不存在！"

def delete_2(photo_name):
    for root, dirs, files in os.walk(ALBUMS_PATH):
        if photo_name in files:
            os.remove(os.path.join(root, photo_name))
            return f"图片 '{photo_name}' 删除成功！"
    return f"未找到图片 '{photo_name}'。"

def upload(photo_name, album_name):
    if not os.path.exists(os.path.join(ALBUMS_PATH, album_name)):
        return f"相册 '{album_name}' 不存在！", None
    
    upload_state['waiting'] = True
    upload_state['photo_name'] = photo_name
    upload_state['album_name'] = album_name
    upload_state['received'] = False

    
    time.sleep(20)

    if upload_state['received']:
        result = None
    else:
        result = "未接收到图片，请重试。"

    upload_state['waiting'] = False
    upload_state['photo_name'] = ''
    upload_state['album_name'] = ''
    upload_state['received'] = False

    return result

def show_1():
    albums = os.listdir(ALBUMS_PATH)
    return "相册列表：" + ", ".join(albums)

def show_2(album_name):
    path = os.path.join(ALBUMS_PATH, album_name)
    if os.path.exists(path):
        photos = os.listdir(path)
        return f"相册 '{album_name}' 的图片：" + ", ".join(photos)
    else:
        return f"相册 '{album_name}' 不存在！"

def show_3(photo_name):
    """
    展示图片函数，接到/show {图片名称}指令后
    返回图片路径给主模块发送
    """
    for root, dirs, files in os.walk(ALBUMS_PATH):
        if photo_name in files:
            return os.path.join(root, photo_name)
    return "失败,不是没有图片，就是因为报错了，重试或者去找开发者"
