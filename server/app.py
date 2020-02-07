from flask import Flask, request

from image_factory import create_image

app = Flask(__name__)


@app.route('/set')
def set_image():
    pass


if __name__ == '__main__':
    app.run()
