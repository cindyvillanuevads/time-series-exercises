# for presentation purposes
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# visualize 
import matplotlib.pyplot as plt

import seaborn as sns


# working with dates
from datetime import datetime

# to evaluated performance using rmse
from sklearn.metrics import mean_squared_error
from math import sqrt 

# for tsa 
import statsmodels.api as sm

# holt's linear trend model. 
from statsmodels.tsa.api import Holt


def evaluate(validate, yhat_df , target_var):
    '''
    This function will take the actual values of the target_var from validate, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse




def plot_and_eval(train, validate, yhat_df, target_var):
    '''
    This function takes in the target var name (string), and returns a plot
    of the values of train for that variable, validate, and the predicted values from yhat_df. 
    it will als lable the rmse. 
    '''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(validate[target_var], label='Validate', linewidth=1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(validate,yhat_df, target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()

# function to store the rmse so that we can compare
def append_eval_df(validate, yhat_df, eval_df, model_type, target_var):
    '''
    this function takes in as arguments the type of model run, and the name of the target variable. 
    It returns the eval_df with the rmse appended to it for that model and target_var. 
    '''
    rmse = evaluate(validate,yhat_df,target_var)
    d = {'model_type': [model_type], 'target_var': [target_var],
        'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)




def make_predictions(yhat_df, validate,  temp, temp_unc):
    yhat_df = pd.DataFrame({'AverageTemperature': [temp],
                           'AverageTemperatureUncertainty': [temp_unc]},
                          index=validate.index)
    return yhat_df



def modeling (temp, temp_unc, yhat_df, train, validate, model_name, eval_df):
    #prediction
    yhat_df = make_predictions(yhat_df, validate,  temp, temp_unc)
    #plot actual vs predicted values
    for col in train.columns:
        plot_and_eval(train, validate , yhat_df, col)
    #evaluate
    for col in train.columns:
        eval_df = append_eval_df(validate, yhat_df, eval_df, model_type = model_name, 
                                 target_var = col)
    return eval_df