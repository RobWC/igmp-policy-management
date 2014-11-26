from flask import Flask
app = Flask(__name__)

@app.route("/",methods=['HEAD'])
def hello():
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
