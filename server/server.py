from flask import Flask, render_template, request
from liteup import options
app = Flask(__name__)
app.secret_key = 'This is really unique and secret'
app.config['DEBUG'] = True


@app.route('/')
def LiteupConfig():
    import pudb
    pudb.set_trace()  # breakpoint 6647d072 //

    return render_template('mainpage.html')


if __name__ == "__main__":
    app.run(debug=True)
