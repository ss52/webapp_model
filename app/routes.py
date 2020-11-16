from app import app
import json
from flask import render_template, flash, request, redirect, url_for
import app.model as model
import plotly
from app.forms import Change_json


ALLOWED_EXTENSIONS = {"json"}


def make_calc(data):

    time, w = model.batch_calc(data)

    tdata = zip(time, w)
    graph = [dict(x=time, y=w, type="scatter")]
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, tdata


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'calc' in request.form:
            # check if the post request has the file part
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            file = request.files["file"]

            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                data = json.load(file)
                graphJSON, tdata = make_calc(data)

                return render_template("pic.html",
                                       graphJSON=graphJSON,
                                       tdata=tdata,
                                       data=data)
        elif 'change' in request.form:
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            file = request.files["file"]

            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                data = json.load(file)
                return redirect(url_for('change', data=data))

    return render_template("model.html")


@app.route("/change", methods=["GET", "POST"])
def change():

    MyForm = Change_json()
    data = request.args['data']

    if request.method == "GET":
        MyForm.input_field.data = data.replace(", ", ",\n")
        # MyForm.input_field.data = f'test \ntest \n'

    if MyForm.validate_on_submit():
        new_data = json.loads(MyForm.input_field.data.replace("'", '"'))

        graphJSON, tdata = make_calc(new_data)

        return render_template("pic.html",
                               graphJSON=graphJSON,
                               tdata=tdata,
                               data=new_data)

    return render_template("change.html", form=MyForm)
