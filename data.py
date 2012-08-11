import webapp2
from simplehandler import SimpleHandler
from model import MilitaryUnit, MUDamage
from google.appengine.ext import db
import json
from datetime import date, timedelta
from google.appengine.api import memcache

def count_10_days_mu_data():
    result = {}
    groups = db.GqlQuery("SELECT * FROM MilitaryUnit")
    mu_map = {}
    for mu in groups:
        mu_map[mu.mu_id] = [mu.mu_name, mu.mu_location, mu.mu_members_count]
    result["mu"] = mu_map
    mu_damage_result = db.GqlQuery("SELECT * FROM MUDamage WHERE date > :1 ORDER BY date", date.today() - timedelta(days = 12))
    damage_map = {}
    for mu_damage in mu_damage_result:
        if mu_damage.mu_id not in damage_map:
            damage_map[mu_damage.mu_id] = []
        damage_map[mu_damage.mu_id].append([mu_damage.date.strftime("%Y-%m-%d"), mu_damage.damage])
    result["damage"] = damage_map
    memcache.set("10_days_mu_data", result)

class Get10DaysMUDataJSON(SimpleHandler):
    def get(self):
        data = memcache.get("10_days_mu_data")
        if data is None:
            count_10_days_mu_data()
            data = memcache.get("10_days_mu_data")
        json_result = json.dumps(data)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json_result)

app = webapp2.WSGIApplication([
    ('/data/get_json_10', Get10DaysMUDataJSON),
], debug=False)