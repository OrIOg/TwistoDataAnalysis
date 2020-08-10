import twitter
import sqlite3
import utilities

DROP = False

credentials = utilities.get_credentials()
db = sqlite3.connect('twisto_tweets.db')

if DROP:
    db.execute('''DROP TABLE IF EXISTS tweets;''')
    db.execute('''CREATE TABLE IF NOT EXISTS tweets (
        id TEXT PRIMARY KEY,
        time TIMESTAMP NOT NULL,
        text TEXT NOT NULL,
        reply_status_id TEXT,
        reply_user_id TEXT,
        raw_json TEXT NOT NULL
    );''')

api = twitter.Api(consumer_key=credentials[0], consumer_secret=credentials[1], application_only_auth=True, tweet_mode='extended')

def writemany(db: sqlite3.Connection, objs: twitter.models.Status):
    parameters = [(obj.id_str, obj.created_at_in_seconds, obj.full_text, obj.in_reply_to_status_id, obj.in_reply_to_user_id, str(obj)) for obj in objs]
    db.executemany(f'''insert into tweets (id, time, text, reply_status_id, reply_user_id, raw_json) values (?, ?, ?, ?, ?, ?);''', parameters)
    db.commit()

last_id = None

try:
    for status_id in db.execute("SELECT id FROM tweets ORDER BY time ASC LIMIT 1;"):
        last_id = int(status_id[0])-1
except:
    pass

while True:
    results = api.GetUserTimeline(screen_name="TwistoCaen", count=200, trim_user=True, include_rts=False, max_id=last_id if last_id else None)
    last_id = results[-1].id-1
    writemany(db, results)

db.close()
exit(0)