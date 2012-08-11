import webapp2
from simplehandler import SimpleHandler
from google.appengine.api import urlfetch
import urllib
import cgi
from bs4 import BeautifulSoup
from model import MilitaryUnit, Citizen
from google.appengine.ext import db
import json
from datetime import datetime

def delete_mu(mu_id):
	citizens = db.GqlQuery("SELECT * FROM Citizen WHERE citizen_mu_id = :1", mu_id)
	for citizen in citizens:
		citizen.delete()
	groups = db.GqlQuery("SELECT * FROM MilitaryUnit WHERE mu_id = :1", mu_id)
	for group in groups:
		group.delete()
	
class LoadMUPage(SimpleHandler):

	members_counter = 0

	def get(self):
		self.render("admin_mu_form.html", {"url":"load_mu", "load_mu_active":True, "title":"Load MU"})

	def post(self):
		mu_id = int(cgi.escape(self.request.get('mu')))
		delete_mu(mu_id)
		result = urlfetch.fetch("http://www.erepublik.com/en/main/group-list/members/" + str(mu_id))
		if result.status_code == 200:
			regiment_urls, mu_name, mu_location = self.process_group(result.content)
			mu_location = mu_location.replace("\n", "")
			mu_location = mu_location.strip()
			for regiment_url in regiment_urls:
				self.process_regiment(regiment_url, mu_id)
			group = MilitaryUnit(mu_name = mu_name, mu_id = mu_id, mu_location = mu_location, mu_members_count = self.members_counter)
			group.put()			
			self.render("admin.html", {"text" : "Group added : name=" + group.mu_name + " location=" + group.mu_location + " id=" + str(group.mu_id) + " members=" + 
				str(group.mu_members_count)})

	def process_group(self, content):
		soup = BeautifulSoup(content)
		regiment_urls = []
		for regiment_option in soup.find_all("div", 'regiment_drop_down')[0].find_all("option"):
			regiment_urls.append(regiment_option["url"])
		group_header = soup.find("div", "header_content")
		mu_name = group_header.h2.span.text
		mu_location = group_header.find("div", "details").a.text
		return regiment_urls, mu_name, mu_location

	def process_regiment(self, regiment_url, mu_id):
		result = urlfetch.fetch("http://www.erepublik.com" + regiment_url)
		if result.status_code == 200:
			soup = BeautifulSoup(result.content)
			result_data = []
			for td in soup.find_all("td", "avatar"):				
				citizen_url = td.a["href"]
				citizen_id = int(citizen_url[citizen_url.find("profile") + 8:])
				citizen_name = td.a.text
				citizen = Citizen(citizen_name = citizen_name, citizen_id = citizen_id, citizen_mu_id = mu_id)
				citizen.put()
				self.members_counter += 1
				result_data.append([citizen_name, citizen_id, mu_id])					

class DeleteMUPage(SimpleHandler):
	def get(self):
		self.render("admin_mu_form.html", {"url":"delete_mu", "delete_mu_active":True, "title":"Remove MU"})

	def post(self):
		mu_id = int(cgi.escape(self.request.get('mu')))
		delete_mu(mu_id)		
		self.render("admin.html", {"text" : "MilitayUnit " + str(mu_id) + " deleted"})

class CurrentTimePage(SimpleHandler):
	def get(self):
		self.render("admin.html", {"text" : "current time : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "current_time_active":True})

app = webapp2.WSGIApplication([
    ('/admin/load_mu', LoadMUPage),
	('/admin/delete_mu', DeleteMUPage),
	('/admin/current_time', CurrentTimePage),
], debug=True)