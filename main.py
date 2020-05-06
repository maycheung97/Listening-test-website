import copy
import time

from flask import *
import random
import os
import pandas as pd
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def home():
    session["count"] = 0
    session["result"] = []
    session["comment"] = []

    session['id'] = str(time.time())

    session['data'] = []

    df = pd.read_csv("listening_test_triplets.csv")
    for index, row in df.iterrows():
        if index >= 53:
            break
        temp = [row[0].strip().strip('\'').split('.')[0], row[2].strip().strip(
            '\'').split('.')[0], row[1].strip().strip('\'').split('.')[0]]
        session['data'].append(temp)

    data_1 = copy.deepcopy(session['data'][3:])
    session['data'].extend(data_1)

    for i in range(0, 53):
        session['data'][i][0] = "recs_slow/" + session['data'][i][0] + "_slow.wav"
        session['data'][i][1] = "recs_slow/" + session['data'][i][1] + "_slow.wav"
        session['data'][i][2] = "recs_slow/" + session['data'][i][2] + "_slow.wav"
    for i in range(53, 103):
        session['data'][i][0] = "recs/" + session['data'][i][0] + ".wav"
        session['data'][i][1] = "recs/" + session['data'][i][1] + ".wav"
        session['data'][i][2] = "recs/" + session['data'][i][2] + ".wav"

    random.shuffle(session['data'])

    with open('out_%s.csv' % session['id'], 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["a", "prop", "b", 'result', 'comment'])

    return render_template("main.html", audio_a=session['data'][session["count"]][0],
                           audio_b=session['data'][session["count"]][1],
                           audio_c=session['data'][session["count"]][2], msg="Pre Test", first=True)


@app.route('/submit')
def submit():
    if "count" not in session:
        return redirect("/")

    session["result"].append(request.args.get("result"))
    session["comment"].append(request.args.get("comment"))
    print(request.args.get("result"))
    print(request.args.get("comment"))
    print(session["count"])

    if session["count"] >= 3:
        with open('out_%s.csv' % session['id'], 'a+', encoding='utf-8') as f:
            csv_writer = csv.writer(f)

            csv_writer.writerow(
                [session['data'][session["count"]][0].split('/')[1], session['data'][session["count"]][1].split('/')[1],
                 session['data'][session["count"]][2].split('/')[1], session["result"][session["count"]],
                 session["comment"][session["count"]]])

    if session["count"] == 102:
        session["count"] = 0
        return render_template("finish.html")

    msg = ""

    session["count"] += 1

    if session["count"] <= 2:
        msg = "Pre Test"
    elif session["count"] <= 52:
        msg = "Count(" + str(int(session["count"]) - 2) + ")"
        msg = str(int(session["count"]) - 2) + "/100"
    else:
        msg = "Count(" + str(int(session["count"]) - 52) + ")"
        msg = str(int(session["count"]) - 2) + "/100"

    return render_template("main.html", audio_a=session['data'][session["count"]][0],
                           audio_b=session['data'][session["count"]][1],
                           audio_c=session['data'][session["count"]][2], msg=msg)


@app.route('/survey')
def survey():
    gender = request.args.get("gender")
    age = request.args.get("age")
    hearing = request.args.get("hearing")

    with open('out_%s.csv' % session['id'], 'a+', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["gender", gender])
        csv_writer.writerow(["age", age])
        csv_writer.writerow(["hearing", hearing])
    return "test finish"


@app.route('/static/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, 'static', path))


if __name__ == '__main__':
    app.run(debug=True)
