## Import the required libraries ##
from flask_cors import CORS 
import pymongo 
import os
from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import json
import pandas as pd

# connect to the mongoDB cloud

# connection_url='mongodb+srv://abin:abin@cluster0.vklmj.mongodb.net/TableDB?retryWrites=true&w=majority'

connection_url = os.environ.get('MONGODB_URL')

app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Access the Database 
Database = client.get_database('TableDB') 

# Access the Table 
SampleTable = Database.SalaryExperience

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getdelay', methods=['POST'])
def get_delay():
    # get the input from the html page
    result=request.form
    
    YearsOfExperience=result['YearsOfExperience']

    future_val=float(YearsOfExperience)

    # load the saved model
    reg_model = joblib.load('SLR_model.pkl')
 
    prediction=reg_model.predict(future_val)
    
    # To write back to the database
    pred=str(prediction[0])
 
    mydict = { "YearsOfExperience": future_val, "Salary":pred}
    mydict1=mydict.copy()
    SampleTable.insert_one(mydict)
    
    # To produce the prediction in the html page 

    return render_template('result.html',mydict1=mydict1)
      

if __name__ == '__main__':
    app.run(debug=True)
