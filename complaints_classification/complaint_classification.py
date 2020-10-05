# -*- coding: utf-8 -*-
'''
Project: ABC finance consumer complaints management
Created by: Krishna Prakash
Date created : 11-Sep-2020
Purpose:
This is a sample web based online consume complaint classification module
Features:
1. Online submission of consumer complaints
2. Storing the complaints data in SQLite database
3. Classify the complaints to appropriate department using a machine learning model
'''


#importing important libraries
import pickle
import warnings
warnings.filterwarnings('ignore')
import pickle

from flask import Flask, render_template, request


# load the complaints classification model
complaints_class = pickle.load(open("./model/complaint_classification_model.pkl", 'rb'))

# INITIALIZE REST API service
app = Flask(__name__)

# Home page
@app.route('/',methods=['POST', 'GET'])
def home():
    home_page = '<html><h1>ABC FINANCE HOME PAGE</h1><body><a href="/application.html">Click here to submit new complaint</a></html>'
    return home_page

# Build API for calling classification model through the web application
@app.route('/application.html',methods=['POST', 'GET'])
def complaints_submission():
    deparment_name = ""
    message = ""
    if request.method == 'POST':
        try:
            customer_name = request.form['customer_name']
            customer_complaint = request.form['complaint_narrative']
            # customer_complaint = "my money is still pending"
            print(customer_complaint)
            department_name = complaints_class.predict([customer_complaint])
            print(department_name)
            message = 'Your complaint is assigned to : '+str(department_name)
         
        except:
            message = 'Error!'   
    return render_template('application.html',complaint_status = message)

# RUN THE API SERVICE
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
