# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 19:29:23 2022

@author: viswateja
"""

import pickle


def load_model():
    loaded_model = pickle.load(open(r"D:\MLOPs\finalized_model.sav", 'rb'))
    print("loading model-----------------------------")
    return loaded_model

def predict(loaded_model,data):
    result = loaded_model.predict(data,)
    return result

def input_req(data):
    model = load_model()
    response = predict(model,data)
    return str(response[0])


