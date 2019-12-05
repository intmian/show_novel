from flask import Flask

app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_book():
    pass


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
