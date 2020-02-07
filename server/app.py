from flask import Flask, request

from image_factory import create_image

app = Flask(__name__)


@app.route('/set')
def set_image():
    width = request.form['width']
    height = request.form['height']
    return ''


if __name__ == '__main__':
    app.run()
