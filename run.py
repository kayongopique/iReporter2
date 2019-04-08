from api import Create_app
from flask import render_template
app = Create_app('default')


if __name__ == '__main__':
    app.run()