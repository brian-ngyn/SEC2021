from flask import Flask, redirect, url_for, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

cred = credentials.Certificate("redacted")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'redacted'
})

bucket = storage.bucket()
model = None
df3 = None
file_train = ""
file_test = ""

@app.route('/', methods=["POST", "GET"])
def index():
    global file_train
    if request.method == "POST":
        file_train = request.form["myFile_train"]
        return redirect("train-model")
    else:
        return render_template("index.html")

@app.route('/train-model', methods=["POST", "GET"])
def train_model():
    global model
    global file_train
    global file_test
    df = pd.read_csv(file_train)

    subdf = df[['Glucose', 'BloodPressure', 'Insulin', 'BMI', 'DiabetesPedigreeFunction']]
    X = subdf
    Y = df.Outcome

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, train_size=0.8, shuffle=False)

    model = LogisticRegression(max_iter=750)
    model.fit(X_train, Y_train)

    if request.method == "POST":
        file_test = request.form["myFile_test"]
        return redirect("run-regression")
    else:
        return render_template("train-model.html", accuracy=round((model.score(X_test, Y_test) * 100),2))

@app.route('/run-regression', methods=["POST", "GET"])
def run_regression():
    global model
    global file_test
    global df3
    blob = bucket.blob(file_test)

    df2 = pd.read_csv(file_test)
    df3 = df2.drop(columns = ['Outcome'])
    df2 = df3.drop(columns = ['Patient', 'SkinThickness', 'Age'])

    results = model.predict(df2)
    df3['Outcome'] = results
    df3.to_csv("prediction_" + file_test, index=False)
    blob = bucket.blob("prediction_" + file_test)
    blob.upload_from_filename("prediction_" + file_test)

    if request.method == "POST":
        return redirect("load-csv")
    else:
        return render_template("run-regression.html")

@app.route('/load-csv', methods=["POST", "GET"])
def load_csv():
    global df3

    if request.method == "GET":
        return render_template("load-csv.html", csv=df3.to_html(index=False, classes="center"))
    else:
        return redirect("/")