from flask import Flask, request, render_template, jsonify, g
import replicate
import os
import time
import google.generativeai  # 假设这是Google Generative AI库的导入方式


# 配置环境变量
# 设置环境变量来安全地处理密钥
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
google_api_key = os.getenv("GOOGLE_API_KEY")

# 使用环境变量中的密钥初始化Google Generative AI模型
google.generativeai.configure(api_key=google_api_key)
app = Flask(__name__)

text_model = {"model": "models/chat-bison-001"}

app = Flask(__name__)

r = ""
first_time = 1

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    global r, first_time
    if first_time == 1:
        r = request.form.get("r")
        first_time = 0
    return render_template("main.html", r=r)

@app.route("/text_gpt", methods=["GET", "POST"])
def text_gpt():
    return render_template("text_gpt.html")

@app.route("/text_result", methods=["GET", "POST"])
def text_result():
    q = request.form.get("q")
    response = google_ai.chat(**text_model, messages=[{"role": "user", "content": q}])
    return render_template("text_result.html", r=response.choices[0].message.content)

@app.route("/image_gpt", methods=["GET", "POST"])
def image_gpt():
    return render_template("image_gpt.html")

@app.route("/image_result", methods=["GET", "POST"])
def image_result():
    q = request.form.get("q")
    response = google_ai.generate_image(**image_model, prompt=q)
    time.sleep(10)  # 假定有一定的处理延时
    return render_template("image_result.html", r=response.url)  # 假设响应中包含图像的URL

@app.route("/recreate", methods=["GET", "POST"])
def recreate():
    response = google_ai.generate_image(**image_model, prompt=r)
    time.sleep(10)
    return render_template("recreate.html", r=response.url)

@app.route("/NTU", methods=["GET", "POST"])
def NTU():
    return render_template("NTU.html")

@app.route("/more_NTU", methods=["GET", "POST"])
def more_NTU():
    return render_template("more_NTU.html")

@app.route("/end", methods=["GET", "POST"])
def end():
    global first_time, r
    first_time = 1
    return render_template("end.html", r=r)

if __name__ == "__main__":
    app.run()

