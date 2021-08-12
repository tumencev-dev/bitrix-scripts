from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    data = request.json
    result = data['client']['adress']
    return result

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
