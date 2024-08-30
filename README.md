# WeChat Bot Project

## 项目介绍
这是一个基于 ItChat 的微信机器人项目，实现了相册管理、图片上传等功能。

## 结构
- `main.py`：启动和管理微信机器人。
- `commands.py`：处理用户的指令。
- `pictools.py`：执行具体的功能（如创建相册、上传图片）。
- `upload_state.py`：保存上传状态。
- `templates/index.html`：前端模板。

## 安装
1. 克隆仓库：`git clone https://github.com/liyihao1110/wechat_robot.git`
2. 安装依赖：`pip install -r requirements.txt`

## 使用
1. 运行 `app.py` 启动微信机器人。
2. 发送指令如 `/create 相册名` 来创建相册。
