import time
import redis
from flask import Flask, render_template
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv() 
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379,  password=os.getenv('REDIS_PASSWORD'))
app = Flask(__name__)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/titanic')
def titanic():
    df = pd.read_csv('titanic.csv')  # adjust path if needed
    table_html = df.head().to_html(classes='data', header="true")
    gender_survival = df[df['survived'] == 1]['sex'].value_counts().to_dict()
    return render_template('titanic.html', table=table_html,chart_data=gender_survival)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)