from flask import Flask,request,render_template
import replicate
import os
import time
import google.generativeai as palm

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=api)
model = {"model":"models/chat-bison-001"}


app = Flask(__name__)

r = ""
first_time = 1

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global r,first_time
    if first_time==1:
        r = request.form.get("r")
        first_time=0
    return(render_template("main.html",r=r))

@app.route("/text_gpt", methods=["GET", "POST"])
def text_gpt():
    return render_template("text_gpt.html")

@app.route("/text_result", methods=["GET", "POST"])
def text_result():
    q = request.form.get("q")
    response = palm.chat(messages=[q], model="models/chat-bison-001")
    time.sleep(5)
    return render_template("text_result.html", r=response.result)

@app.route("/image_gpt",methods=["GET","POST"])
def image_gpt():
    return(render_template("image_gpt.html"))

@app.route("/image_result",methods=["GET","POST"])
def image_result():
    q = request.form.get("q")
    r = replicate.run(
    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    input={
        "prompt": q,
        }
    )
    global image_prompt
    image_prompt = q
    time.sleep(10)
    return(render_template("image_result.html",r=r[0]))

@app.route("/recreate",methods=["GET","POST"])
def recreate():
    r = replicate.run(
    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    input={
        "prompt": image_prompt,
        }
    )
    time.sleep(10)
    return(render_template("recreate.html",r=r[0]))

@app.route("/NTU",methods=["GET","POST"])
def NTU():
    return(render_template("NTU.html"))
    
@app.route("/more_NTU",methods=["GET","POST"])
def more_NTU():
    return(render_template("more_NTU.html"))

@app.route("/end",methods=["GET","POST"])
def end():
    global first_time,r
    first_time = 1
    return(render_template("end.html",r=r))

if __name__ == "__main__":
    app.run()
