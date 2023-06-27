import logging as log
import os

import mariadb
import redis
from flask import Flask, render_template_string

page_template = '''
        <div style="margin: auto; text-align: center;">
        <h1>{{ welcome_text }}</h1><br>
        You're the #{{ visitors }} visitor to view Andy Hu's Top 5 NBA GOAT players:<br>
        <ul>
            {%- for team in teams %}
            <li>{{ team }}</li>
            {%- endfor %}
        </ul>
        </div>
        '''

app = Flask(__name__)
# cache = redis.StrictRedis(host='cache-service', port=6379)
cache = redis.StrictRedis(host='cache-service.andy-rollout-demo.svc.cluster.local', port=6379)

@app.route('/')
def root():
    visitors = cache_get_visitor_count()
    team = db_get_teams()

    return render_template_string(page_template, visitors=visitors, teams=team, welcome_text=os.getenv("WELCOME", "Hey NBA Fanatic!"))



def db_get_teams():
    conn = mariadb.connect(
        host=os.environ['MARIA_HOST'],
        database="andy-argo-db1",
        user=os.environ['MARIA_USER'],
        password=os.environ['MARIA_PASS'],
    )

    cur = conn.cursor()
    # cur.execute("SELECT teams FROM semifinalists;")
    cur.execute("SELECT player FROM goatplayers;")

    return [x[0] for x in cur.fetchall()] 


def cache_get_visitor_count():
    return cache.incr('visitors')