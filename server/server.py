from flask import Flask, render_template, request, jsonify, redirect
from liteup.schemes.all_schemes import all_schemes
app = Flask(__name__)
app.secret_key = 'This is really unique and secret'
app.config['DEBUG'] = True
app.current_scheme = None


def preview_url(SchemeCls):
    return "%s.png" % (SchemeCls.__name__.lower())


@app.route('/')
def LiteupBase():
    scheme_names = [
        (cls.__name__, preview_url(cls)) for cls in all_schemes
        if cls.ui_select
    ]
    return render_template('mainpage.html',
                           scheme_names=sorted(scheme_names),
                           current_scheme=app.current_scheme)


@app.route('/config', methods=["POST"])
def ConfigChange():
    print(request.args)
    scheme_name = request.form.get('scheme_name', None)
    if scheme_name:
        app.current_scheme = scheme_name

    return redirect("/")


@app.route('/config', methods=["GET"])
def ConfigAPI():
    return jsonify({"current_scheme": app.current_scheme})


if __name__ == "__main__":
    app.run(debug=True)
