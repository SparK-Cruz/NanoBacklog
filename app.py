from flask import Flask, render_template
import requests
import json
from types import SimpleNamespace
import datetime
import pandas as pd
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    bps, cps, backlog, days, hours, minutes, seconds = get_data()
    
    return render_template(
        'index.html',
        bps=format(bps, '.2f'), 
        cps=format(cps, '.2f'), 
        backlog=format(backlog, ','),
        days=format(days, '.0f'), 
        hours=format(hours, '.0f'), 
        min=format(minutes, '.0f'), 
        sec=format(seconds, '.0f')
    )

def get_data():
    API_data = requests.get('https://nanoticker.info/json/stats.json').text
    current_data = json.loads(API_data, object_hook=lambda d: SimpleNamespace(**d))

    current_bps = current_data.BPSMedian
    current_cps = current_data.CPSMedian
    backlog = current_data.blockCountMedian - current_data.cementedMedian

    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    current_data = {
        "hour": current_hour, 
        "minute": current_minute, 
        "bps": current_bps,
        "cps": current_cps
    }

    data_path = '/home/data.json'

    # create file if not exists
    if os.path.exists(data_path):
        df = pd.read_json(data_path)
    else:
        open(data_path, "a+")
        df = pd.DataFrame(current_data, index=[0])
        df.to_json(data_path, orient="records")
        print(df)

    # Clean entrys that are older than 1h
    df = df[(df['hour'] == current_hour) | (df['minute'] > current_minute)]

    # Only add if it is not yet in the df
    not_exists = df[(df['hour'] == current_hour) & (df['minute'] == current_minute)].empty
    if not_exists:
        df = df.append(current_data, ignore_index=True)
        df.to_json(data_path, orient="records")

    mean_bps = df['bps'].mean() 
    mean_cps = df['cps'].mean()

    seconds_remaining = (backlog / (mean_cps-mean_bps))
    timedelta = datetime.timedelta(seconds=seconds_remaining)

    days = timedelta.days
    total_seconds = timedelta.total_seconds()
    hours = (total_seconds - (days * 24 * 60 * 60)) // 3600
    minutes = ((total_seconds - (days * 24 * 60 * 60)) % 3600) // 60
    seconds = total_seconds % 60

    return mean_bps, mean_cps, backlog, days, hours, minutes, seconds

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True) 