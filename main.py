# /index.py
from flask import Flask, request, jsonify, render_template, session
import os
import pickle
import datetime
import time
import pandas as pd
import numpy as np
import random
import logging


# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__)
app.secret_key = 'MY_SECRET_KEY'


def label_Message(message):
    logging.warning('In label_Message')
    # load the model from disk
    model_filename = 'model/model.pkl'
    tfidf_filename = 'model/tfidf.pkl'
       
    model = pickle.load(open(model_filename, 'rb'))
    tfidf = pickle.load(open(tfidf_filename, 'rb'))
     
    pred = model.predict(tfidf.transform([message]))
    message_label = pred[0]
    
    
    logging.warning('Out label_Message')
    return message_label



def label_to_persian(label):
    res = ''
    if label == 'HAPPY':
        res = 'خوشحال'
    elif label == 'SAD':  
        res = 'ناراحت'

    return res       

def Create_message(message):
    logging.warning('In create message')
    global result

    
    ### State : on
    label = session['label']
    state = session['state']
    result = session['result']
    result['response'] = ''
    result['status'] = 'on'
    
    if state == 'start':
        label = label_Message(message)
        session['label'] = label
        result['message'] = message
        result['response'] = 'ممنونم، نظر شما دریافت شد. شما به نظر '
        
        if label == 'HAPPY':
            result['response'] +=  'خوشحال هستید'
            result['label'] = label_to_persian(label[0])
        elif label == 'SAD':
            result['response'] += 'ناراحت هستید'
            result['label'] = label_to_persian(label[0])

        session['state'] = 'done'
    
    
    
    
   
    elif state == 'done':
        result['response'] = 'گزارش شما ثبت شده است، گزارش جدیدی ثبت شود؟ (بله، خیر)'
        result['status'] = 'on'
        
        if message == 'بله':
            result = {}
            result['response'] = 'لطفا نظر خود را وارد کنید'
            result['status'] = 'on'
            session['state'] = 'start'
            session['label'] = ''

            
        elif message == 'خیر':
            result['response'] = 'ممنونم'
            session['state'] = 'done'
        
        else:
            session['state'] = 'done'
            
   
    session['result']  = result
    
    return result


      
@app.route('/')
def index():
    session['state'] = 'start'
    session['label'] = ''
    session['result'] = {}
    return render_template('index2.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response_text = Create_message(message)

    
    #print('\nRESPONSE TEXT ', response_text)
    return jsonify(response_text)




