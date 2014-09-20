#!/usr/bin/env python
import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch
import json

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    result = ""
    url1 = "http://hack2014.justdial.com/search/json/completedefault/%s/13043647/77620617/100km/10"
    cat_list = []

    for x in xrange(ord('a'), ord('z')+1):
      for y in xrange(ord('a'), ord('z')+1):
        url = url1 % (chr(x)+chr(y))
        try:
            rdata = urlfetch.fetch( url = url, 
                                    follow_redirects = False, 
                                    deadline = 30)
        except Exception as e:
            log = "HTTP error"
            logging.warning(log)
            log = traceback.format_exc()
            logging.warning(log)
            # code HTTP error
            code = {"code" : 1, "desc":"HTTP error - " + str(e)}
            final_json = json.dumps(code)
            self.response.out.write(final_json)
            return


        if rdata.status_code == 200:
            data = json.loads(rdata.content)
            for cat in data["data"]:
                if cat["mcat"] is not None:
                    if cat["mcat"] not in cat_list:
                        cat_list.append(cat["mcat"])

    self.response.headers['Content-Type'] = 'text/plain'
    
    for tmp in cat_list:
        result += tmp + "\n"
    self.response.out.write(result)



app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
