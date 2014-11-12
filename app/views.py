from flask import render_template, jsonify
from app import app

@app.route('/')
@app.route('/index')
def index():
    settings = {"max_int": 500,
                "min_int": 0}
    return render_template("index.html",
                           settings=settings,
                           title="Spectrometer")

#@app.route('/spectra',)
#def spectra():
