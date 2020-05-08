from app import app
import json
from flask import render_template, flash, request, redirect
import model
import plotly

ALLOWED_EXTENSIONS = {"json"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # file.save(os.path.join(uploads_dir, file.filename))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            data = json.load(file)
            time, w = model.batch_calc(data)

            tdata = zip(time, w)
            graph = [dict(x=time, y=w, type="scatter")]
            graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template("pic.html", graphJSON=graphJSON, tdata=tdata)

    return render_template("model.html")
