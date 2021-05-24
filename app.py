from flask import Flask, render_template
import requests
import json
from types import SimpleNamespace
import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    data = requests.get('https://nanoticker.info/json/stats.json').text
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    bps = x.BPSMedian
    cps = x.CPSMedian
    backlog = x.blockCountMedian - x.cementedMedian

    seconds_remaining = (backlog / (cps-bps))
    timedelta_obj = datetime.timedelta(seconds=seconds_remaining)

    days = timedelta_obj.days
    total_seconds = timedelta_obj.total_seconds()
    hours = (total_seconds - (days * 24 * 60 * 60)) // 3600
    minutes = ((total_seconds - (days * 24 * 60 * 60)) % 3600) // 60
    seconds = total_seconds % 60
    
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True) 