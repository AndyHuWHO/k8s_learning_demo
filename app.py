import logging as log
import os

import mariadb
import redis
from flask import Flask, render_template_string

page_template = '''
        <div style="margin: auto; text-align: center;">
        <h1>{{ welcome_text }}</h1><br>
        You're visitor #{{ visitors }} to learn about the FIFA 2022 World Cup Semifinalists:<br>
        <ul>
            {%- for team in teams %}
            <li>{{ team }}</li>
            {%- endfor %}
        </ul>
        </div>
        '''

app = Flask(__name__)
cache = redis.StrictRedis(host='cache', port=6379)

@app.route('/')
def root():
    visitors = cache_get_visitor_count()
    team = db_get_teams()

    return render_template_string(page_template, visitors=visitors, teams=team, welcome_text=os.getenv("WELCOME", "Hey Football Fanatic!"))



def db_get_teams():
    conn = mariadb.connect(
        host="db",
        database="acorn",
        user=os.environ['MARIA_USER'],
        password=os.environ['MARIA_PASS'],
    )

    cur = conn.cursor()
    cur.execute("SELECT teams FROM semifinalists;")

    return [x[0] for x in cur.fetchall()] 


def cache_get_visitor_count():
    return cache.incr('visitors')