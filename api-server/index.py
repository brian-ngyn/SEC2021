from flask import Flask
from flask import request
app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

cred = credentials.Certificate("./sec2021-4362e-firebase-adminsdk-w43kk-eb144e1760.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sec2021-4362e.appspot.com'
})

bucket = storage.bucket()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/run-regression', methods=['GET'])
def run_regression():
    file_name = request.args.get('file_name')
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)

    df2 = pd.read_csv(file_name)
    df3 = df2.drop(columns = ['Outcome'])
    df2 = df3.drop(columns = ['Patient'])

    results = model.predict(df2)
    df3['Outcome'] = results
    df3.to_csv(file_name + "_prediction", index=False)
    blob = bucket.blob(filename + "_prediction")
    blob.upload_from_filename(filename + "_prediction")

    return '', 200

@app.route('/train-model', methods=['GET'])
def train_model():
    df = pd.read_csv("dataset_training.csv")

    subdf = df[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
    X = subdf
    Y = df.Outcome

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, train_size=0.8)

    model = LogisticRegression(max_iter=250)
    model.fit(X_train, Y_train)

    return '', 200
