import cgi

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import os

DATA_FILE='rolls_data_digested.tsv'
APP_ID='yojana'

MAIN_PAGE_HTML = """\
<!doctype html>
<html>
<title> Yojana </title>
  <body bgcolor="#FFCC66">
    <center>
    <h1> Yojana </h1>
    <img src="http://i.telegraph.co.uk/multimedia/archive/01385/indian_voters_1385542c.jpg">
    <br>
    <hr>
    <br>
    <form action="/filter_data" method="get">
      <div> Constituency filter :  <select name="constituencyFilter"> %s  </select> </div>
      <br>
      <div> Anomaly filter :  <select name="anomalyFilter"> %s  </select> </div>
      <br>
      <div><input type="submit" value="Filter anomalous records by Constituency"></div>
    </form>
    <br>
    <hr>
    <br>
    <form action="/show_data" method="get">
      <div><input type="submit" value="Show all anomalous records"></div>
    </form>
    <br>
    <br>

    </center>
  </body>
</html>
"""

# <div> Attribute filter : %s</div>


class AnomalousRecord(ndb.Model):
    """Models an anomalous record."""
    voterId = ndb.StringProperty()
    name = ndb.StringProperty()
    gender = ndb.StringProperty(indexed=True)
    relation = ndb.StringProperty(indexed=True)
    relationName = ndb.StringProperty()
    houseId = ndb.StringProperty()
    anomalyType=ndb.StringProperty()
    constituency=ndb.StringProperty()
    voterAge = ndb.IntegerProperty(indexed=True)


    def toString(self):
      return '   \t   '.join([self.voterId,self.name,self.gender,self.relation,self.relationName,self.houseId, self.anomalyType, self.constituency, str(self.voterAge)])


class MainPage(webapp2.RequestHandler):

    def constituencies(self):
      C=set([])
      for r in AnomalousRecord.query(ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
        C.add(r.constituency)
      return list(C)

    def anomaly_types(self):
      A=set([])
      for r in AnomalousRecord.query(ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
        A.add(r.anomalyType)
      return list(A)

    def drop_down_options(self, values):
      htmlString=""
      for val in values:
        htmlString+= '<option value="'+val+'">'+val+'</option>'
      return htmlString


    def get(self):
        self.response.write(MAIN_PAGE_HTML % (self.drop_down_options(['all']+self.constituencies()),self.drop_down_options(['all']+self.anomaly_types())))
        pass


class Guestbook(webapp2.RequestHandler):

    def post(self):
        self.response.write('<!doctype html><html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write(cgi.escape(self.request.get('bday')))
        self.response.write('</pre></body></html>')


class ShowAllData(webapp2.RequestHandler):

  def get(self):
    for r in AnomalousRecord.query(ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
      self.response.write(r.toString()+'<br>')


class ReloadAllData(webapp2.RequestHandler):
  def get(self):
    #clear
    for r in AnomalousRecord.query(ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
      r.key.delete()
    #load
    for l in open(DATA_FILE):
      self.response.write('loading '+l+'<br>')
      ar=AnomalousRecord(parent=ndb.Key(AnomalousRecord,APP_ID))
      splits=l.rstrip('\n').split('\t')
      
      splits[2]=splits[2]  #gender
      splits[-1]=int(splits[-1])  #age
      
      ar.voterId,ar.name,ar.gender,ar.relation,ar.relationName,ar.houseId, ar.anomalyType, ar.constituency, ar.voterAge= tuple(splits)
      ar.put()



class FilterData(webapp2.RequestHandler):
  def get(self):
    constituencyToFilter = self.request.get('constituencyFilter')
    anomalyToFilter = self.request.get('anomalyFilter')
    if constituencyToFilter=="all":
      if anomalyToFilter=="all":
        for r in AnomalousRecord.query(ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
          self.response.write(r.toString()+'<br>')
    else:
      if anomalyToFilter=="all":
        for r in AnomalousRecord.query(AnomalousRecord.constituency==constituencyToFilter, ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
          self.response.write(r.toString()+'<br>')
      else:
        for r in AnomalousRecord.query(AnomalousRecord.constituency==constituencyToFilter,  AnomalousRecord.anomalyType==anomalyToFilter , ancestor=ndb.Key(AnomalousRecord,APP_ID)).fetch():
          self.response.write(r.toString()+'<br>')
    



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/show_data', ShowAllData),
    ('/reload_data', ReloadAllData),
    ('/filter_data', FilterData),
], debug=True)

