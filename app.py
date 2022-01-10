from flask import Flask, render_template,request,redirect

import pandas as pd
import numpy as np
import os
import time

from bokeh.io import curdoc
from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components,file_html
from os.path import dirname, join  
import requests

app = Flask(__name__)


###Load data from Quandl

def datetime(x):
    return np.array(x, dtype=np.datetime64)

def get_data(name):
###Load data from AlphaVantage
    base_url = 'https://www.alphavantage.co/query?'
    params = {'function': 'TIME_SERIES_INTRADAY', 'symbol':name, 'interval':'5min',
          'outputsize':'full', 'apikey': '385B2D7KI45KELKJ'}
    response = requests.get(base_url, params=params)

# Here define your dataframe

    raw = response.json()
    interval = '5min'
    mykey = 'Time Series (' + interval + ')'
    df = pd.DataFrame.from_dict(raw[mykey])
    x = pd.to_datetime(df.columns, format = '%Y-%m-%d')
 

    return df, x


def create_figure(df, x):


    p = figure(x_axis_type="datetime", plot_width=800, plot_height=350)
    p.line(x, df.loc['2. high'], color='firebrick', legend_label='high' , line_width=1)
    p.line(x, df.loc['3. low'], color='navy', legend_label='low', line_width=1)

    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "green"
    p.ygrid.band_fill_alpha = 0.1

    p.legend.location = "top_left"
    return p


@app.route("/index", methods=['GET','POST'])    

def index():
    
    if request.method == 'GET':
        return render_template('Search.html')
        
    else:
        #request was a POST
        symbol = request.form['ticker']
        mydata, myx = get_data(symbol)
        
        plot = create_figure(mydata, myx)

        script, div = components(plot)       
        return render_template('Plot.html', script=script, div=div)
       
@app.route('/', methods=['GET','POST'])
def main():
    return redirect('/index')

if __name__== "__main__":

    app.run(port=33508, debug = True)
