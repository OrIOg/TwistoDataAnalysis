import twitter
import sqlite3
import utilities
import os.path

credentials = utilities.get_credentials()
db = sqlite3.connect('twisto_tweets.db')

api = twitter.Api(consumer_key=credentials[0], consumer_secret=credentials[1],
                  application_only_auth=True, tweet_mode='extended')

last_id = None

start_count = db.execute("SELECT count(*) FROM tweets;").fetchone()[0]

try:
	for status_id in db.execute("SELECT id FROM tweets ORDER BY time DESC LIMIT 1;"):
		last_id = int(status_id[0]) - 1
except:
	pass


def writemany(db: sqlite3.Connection, objs: twitter.models.Status):
    parameters = [(obj.id_str, obj.created_at_in_seconds, obj.full_text,
                   obj.in_reply_to_status_id, obj.in_reply_to_user_id, str(obj)) for obj in objs]
    db.executemany(
    	f'''insert OR ignore into tweets (id, time, text, reply_status_id, reply_user_id, raw_json) values (?, ?, ?, ?, ?, ?);''', parameters)
    db.commit()


print(f"Last Tweet ID: {last_id}")
results = api.GetUserTimeline(
    screen_name="TwistoCaen", count=100, trim_user=True, include_rts=False, since_id=last_id)
while results and results[-1].id > last_id:
	lasst = results[-1]
	writemany(db, results)
	results = api.GetUserTimeline(screen_name="TwistoCaen", count=100,
	                              trim_user=True, include_rts=False, max_id=lasst.id - 1)

end_count = db.execute("SELECT count(*) FROM tweets;").fetchone()[0]

print(f"{end_count-start_count} new Tweets.")
db.close()
exit(0)
