import sys

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', **globals())


@app.route('/obj/<obj_class>')
def obj(obj_class):
    cls = getattr(sys.modules[__name__], obj_class)
    return cls().data()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)