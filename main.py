#!/usr/bin/env python
import cgi
import datetime
import webapp2
import logging

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch
import json


class categories(ndb.Model):
  category = ndb.StringProperty()
  
class categoryDetails(ndb.Model):
    category = ndb.StringProperty()
    name = ndb.StringProperty()
    companyGeocodes = ndb.StringProperty()
    address = ndb.StringProperty()


class FetchCategories(webapp2.RequestHandler):
  def get(self):
    result = ""
    url1 = "http://hack2014.justdial.com/search/json/completedefault/%s/13043647/77620617/100km/10"
    cat_list = []

    #get categories from aa-zz and put them in cat_list
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

    #write data to db
    for categ in cat_list:
        c = categories()
        c.category = categ
        c.put()
        logging.info('%s added to DB' % categ)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Under construction')

class FetchCategoryDetails(webapp2.RequestHandler):
    def get(self):
        url = "http://hack2014.justdial.com/search/json/justdialapicat/%s/bangalore/bangalore/13043647/77620617/150km/100/%d"
        categories = ndb.gql('SELECT * FROM categories')
        for category in categories:
            docid_list = []
            for i in range(1,10):
                url = url % (category,i)
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
                    for res in data["results"]:
                        if res not in docid_list:
                            docid_list.append(res["docId"])
                            # TODO add to db
                            c = categoryDetails()
                            c.category = category
                            c.name = res["name"]
                            c.address = res["companyGeocodes"]
                            c.put()


                        
    self.response.headers['Content-Type'] = 'text/plain'    



app = webapp2.WSGIApplication([('/fetchCategories', FetchCategories),('/',MainPage),('/fetchCategoryDetails',MainPage)], debug=True)
