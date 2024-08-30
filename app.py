from flask import Flask, render_template, Response, request
import subprocess
import threading
import time
import webbrowser  # Import webbrowser module

app = Flask(__name__)

# 用于标记命令行输出
output_stream = []

def run_main(output_callback):
    """
    运行 main.py 并实时输出命令行日志。
    """
    try:
        process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # 行缓冲，实时输出
        )

        # 实时读取输出并发送到回调函数
        for line in iter(process.stdout.readline, ''):
            output_callback(line.rstrip())  # 确保每行日志正确显示
            time.sleep(0.1)

        process.stdout.close()
        process.wait()

    except Exception as e:
        output_callback(f"Error running bot: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bot():
    # 启动 main.py 文件
    threading.Thread(target=run_main, args=(stream_output,)).start()
    return "Bot started!", 200

def stream_output(line):
    """
    通过 SSE 将输出发送到客户端。
    """
    with app.app_context():
        output_stream.append(line)  # 将输出添加到全局输出流列表

@app.route('/logs')
def logs():
    """
    将命令行日志实时发送到网页。
    """
    def generate():
        previous_output = len(output_stream)
        while True:
            current_output = len(output_stream)
            if current_output > previous_output:
                data = output_stream[previous_output:current_output]
                yield 'data: ' + '\n'.join(data) + '\n\n'  # 发送每行日志并换行
                previous_output = current_output
            time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}/'

    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    time.sleep(1)
    webbrowser.open(url)