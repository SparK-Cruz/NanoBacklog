from flask import Flask
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

    seconds_remaining = (backlog / cps)
    timedelta_obj = datetime.timedelta(seconds=seconds_remaining)

    days = timedelta_obj.days
    total_seconds = timedelta_obj.total_seconds()
    hours = (total_seconds - (days * 24 * 60 * 60)) // 3600
    minutes = ((total_seconds - (days * 24 * 60 * 60)) % 3600) // 60
    seconds = total_seconds % 60
    
    body = """
    <html>
        <head>
            <title>Nano Backlog</title>
        </head>
        <body>
            <div class="demo-layout-waterfall mdl-layout mdl-js-layout">
                <main class="mdl-layout__content">
                    <div class = "page-content">
                        Current Bps (Median): {bps:.2f}<br>
                        Current Cps (Median): {cps:.2f}<br>
                        Current Backlog (Median): {backlog}<br>

                        With the current rates, the backlog will be cleared in: <br>
                        <h1>{days} days, {hours:.0f} hours, {min:.0f} min, {sec:.0f} sec</h1>
                    </div>
                </main>
            </div>
        </body>
    </html>
    """.format(
        bps=bps, 
        cps=cps, 
        backlog=backlog, 
        days=days, 
        hours=hours, 
        min=minutes, 
        sec=seconds)

    return body