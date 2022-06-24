#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://dlg2178:postgres123@35.196.192.139/proj1part2"
print(DATABASEURI)
#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)




@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM artists")
  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/designs/<designid>')
def getdesign(designid=None):
  print(request.args)
  sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.available = true;"
  if(designid):
    sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.available = true AND designs.design_id ={};".format(designid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  designs = {}
  for result in cursor:
    design = {
    'id': result[0],
    'name': result[1],
    'desc': result[2],
    'city': result[3],
    'state': result[4],
    'cost': result[5],
    'available': result[6],
    'artistid': result[7],
    }
    designs[result[0]] = design
  cursor.close()
  print(designs)
  context = dict(data = designs)
  return render_template("designs.html", **context)

@app.route('/designs')
def designs(designid=None):
  print(request.args)
  sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.available = true;"
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  designs = {}
  for result in cursor:
    design = {
    'id': result[0],
    'name': result[1],
    'desc': result[2],
    'city': result[3],
    'state': result[4],
    'cost': result[5],
    'available': result[6],
    'artistid': result[7],
    }
    designs[result[0]] = design
  cursor.close()
  context = dict(data = designs)
  return render_template("designs.html", **context)

@app.route('/artists')
def artists():
  print(request.args)

  sqlquery = "SELECT artist_id, name, city, state, biography FROM artists;"
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  artists = {}
  for result in cursor:
    artist = {
    'id': result[0],
    'name': result[1],
    'city': result[2],
    'state': result[3],
    'bio': result[4]
    }
    artists[result[0]] = artist
  cursor.close()
  context = dict(data = artists)
  return render_template("artists.html", **context)

@app.route('/studios')
def studios():
  print(request.args)

  sqlquery = "SELECT * FROM studio;"
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  studios = {}
  for result in cursor:
    studio = {
    'id': result[0],
    'address': result[1],
    'city': result[2],
    'state': result[3],
    'zip': result[4]
    }
    studios[result[0]] = studio
  cursor.close()
  context = dict(data = studios)
  return render_template("studios.html", **context)

@app.route('/studios/<studioid>')
def getstudio(studioid=None):
  print(request.args)

  sqlquery = "SELECT * FROM studio WHERE studio_id = {};".format(studioid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  studios = {}
  for result in cursor:
    studio = {
    'id': result[0],
    'address': result[1],
    'city': result[2],
    'state': result[3],
    'zip': result[4]
    }
    studios[result[0]] = studio
  cursor.close()
  context = dict(data = studios)
  return render_template("studios.html", **context)



@app.route('/appointments')
def appointments():
  print(request.args)

  sqlquery = "SELECT appointments.appointment_id, customers.name, artists.name, designs.description, appointments.start_time, appointments.end_time, appointments.projected_cost, studio.address, payments.amount, artists.artist_id, customers.customer_id, designs.design_id, studio.studio_id, payments.payment_id FROM appointments JOIN customers ON appointments.customer_id = customers.customer_id JOIN artists ON appointments.artist_id = artists.artist_id JOIN designs ON appointments.design_id = designs.design_id JOIN studio ON appointments.studio_id = studio.studio_id JOIN payments ON appointments.payment_id = payments.payment_id;"
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  appts = {}
  for result in cursor:
    appt = {
    'id': result[0],
    'customer': result[1],
    'artist': result[2],
    'design': result[3],
    'start': result[4],
    'end': result[5],
    'cost': result[6],
    'address': result[7],
    'paid': result[8],
    'artistid': result[9],
    'customerid': result[10],
    'designid': result[11],
    'studioid': result[12],
    'paymentid': result[13]}
    appts[result[0]] = appt
  cursor.close()
  context = dict(data = appts)
  return render_template("appointments.html", **context)

@app.route('/appointment/<apptid>')
def getappointment(apptid=None):
  print(request.args)

  sqlquery = "SELECT appointments.appointment_id, customers.name, artists.name, designs.description, appointments.start_time, appointments.end_time, appointments.projected_cost, studio.address, payments.amount, artists.artist_id, customers.customer_id, designs.design_id, studio.studio_id, payments.payment_id FROM appointments JOIN customers ON appointments.customer_id = customers.customer_id JOIN artists ON appointments.artist_id = artists.artist_id JOIN designs ON appointments.design_id = designs.design_id JOIN studio ON appointments.studio_id = studio.studio_id JOIN payments ON appointments.payment_id = payments.payment_id WHERE appointments.appointment_id = {};".format(apptid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  appts = {}
  for result in cursor:
    appt = {
    'id': result[0],
    'customer': result[1],
    'artist': result[2],
    'design': result[3],
    'start': result[4],
    'end': result[5],
    'cost': result[6],
    'address': result[7],
    'paid': result[8],
    'artistid': result[9],
    'customerid': result[10],
    'designid': result[11],
    'studioid': result[12],
    'paymentid': result[13]}
    appts[result[0]] = appt
  cursor.close()
  context = dict(data = appts)
  return render_template("appointments.html", **context)

@app.route('/billing')
def billing():
  print(request.args)

  sqlquery = "SELECT bill.payment_id, bill.appointment_id, payments.payment_date, payments.method, payments.amount FROM bill JOIN payments ON bill.payment_id = payments.payment_id;"

  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  payments = {}
  for result in cursor:
    payment = {
    'pay_id': result[0],
    'appt_id': result[1],
    'date': result[2],
    'method': result[3],
    'amount': result[4],
    }
    payments[result[0]] = payment
  cursor.close()
  context = dict(data = payments)
  return render_template("billing.html", **context)

@app.route('/payment/<paymentid>')
def payment(paymentid=None):
  print(request.args)

  sqlquery = "SELECT bill.payment_id, bill.appointment_id, payments.payment_date, payments.method, payments.amount FROM bill JOIN payments ON bill.payment_id = payments.payment_id WHERE bill.payment_id = {};".format(paymentid)

  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  payments = {}
  for result in cursor:
    payment = {
    'pay_id': result[0],
    'appt_id': result[1],
    'date': result[2],
    'method': result[3],
    'amount': result[4],
    }
    payments[result[0]] = payment
  cursor.close()
  context = dict(data = payments)
  return render_template("billing.html", **context)

@app.route('/profile/<profileid>')
def profile(profileid=None):
  print(request.args)

  sqlquery = "SELECT * FROM customers WHERE customer_id = {};".format(profileid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  
  for result in cursor:
    customer = {
    'id': result[0],
    'name': result[1],
    'bio': result[2],
    'city': result[3],
    'state': result[4],
    'registered': result[5],
    'gender': result[6]
    }
  context = dict(data = customer)
  return render_template("profile.html", **context)

@app.route('/artist/<profileid>')
def artistprofile(profileid=None):
  print(request.args)

  sqlquery = "SELECT artist_id, name, city, state, biography, registration_date FROM artists WHERE artists.artist_id = {};".format(profileid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  profile = {}
  for result in cursor:
    profile = {
    'id': result[0],
    'name': result[1],
    'city': result[2],
    'state': result[3],
    'bio': result[4],
    'registered': result[5]
    }
  cursor.close()

  query2 = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE artists.artist_id = {};".format(profileid)
  #
  # example of a database query
  #
  cursor = g.conn.execute(query2)
  designs = []
  for result in cursor:
    design = {
    'id': result[0],
    'name': result[1],
    'desc': result[2],
    'city': result[3],
    'state': result[4],
    'cost': result[5],
    'available': result[6],
    }
    designs.append(design)
  cursor.close()
  profile['designs'] = designs
  context = dict(data = profile)
  return render_template("artistprofile.html", **context)


@app.route('/another')
def another():
  return render_template("another.html")

# Search for designs
@app.route('/searchdesigns', methods=['POST'])
def searchdesigns():
  searchterm = request.form['term']
  intterm = 0
  if searchterm.isnumeric():
    intterm = int(searchterm)
  sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.design_id = '{}' OR artists.name LIKE '%%{}%%' OR designs.description LIKE '%%{}%%' OR artists.city LIKE '%%{}%%';".format(intterm, searchterm, searchterm, searchterm)
  cursor = g.conn.execute(sqlquery)
  designs = {}
  for result in cursor:
    design = {
    'id': result[0],
    'artist': result[1],
    'desc': result[2],
    'city': result[3],
    'state': result[4],
    'cost': result[5],
    'available': result[6],
    'artistid': result[7],
    }
    designs[result[0]] = design
  cursor.close()
  print(designs)
  context = dict(data = designs)
  return render_template("designs.html", **context)


@app.route('/searchartists', methods=['POST'])
def searchdartists():
  searchterm = request.form['term']
  intterm = 0
  if searchterm.isnumeric():
    intterm = int(searchterm)
  sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.design_id = '{}' OR artists.name LIKE '%%{}%%' OR designs.description LIKE '%%{}%%' OR artists.city LIKE '%%{}%%';".format(intterm, searchterm, searchterm, searchterm)
  sqlquery = "SELECT artist_id, name, city, state, biography FROM artists WHERE artist_id = '{}' OR name LIKE '%%{}%%' OR city LIKE '%%{}%%' OR state LIKE '%%{}%%';".format(intterm, searchterm, searchterm, searchterm)
  #
  # example of a database query
  #
  cursor = g.conn.execute(sqlquery)
  artists = {}
  for result in cursor:
    artist = {
    'id': result[0],
    'name': result[1],
    'city': result[2],
    'state': result[3],
    'bio': result[4]
    }
    artists[result[0]] = artist
  cursor.close()
  context = dict(data = artists)
  return render_template("artists.html", **context)

@app.route('/book/<designid>', methods=['POST'])
def bookappt(designid=None):
  sqlquery = "SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.design_id = {};".format(designid)
  cursor = g.conn.execute(sqlquery)
  design = {}
  appt_options = {}
  for result in cursor:
    design = {
    'id': result[0],
    'artist': result[1],
    'desc': result[2],
    'city': result[3],
    'state': result[4],
    'cost': result[5],
    'available': result[6],
    'artistid': result[7],
    }
  cursor.close()
  appt_options['design'] = design

  query2 = "SELECT address, city, state, zip_code, studio_id FROM studio WHERE city = '{}'".format(design['city'])
  cursor = g.conn.execute(query2)
  studios = []
  for result in cursor:
    studios.append(result)
  appt_options['studios'] = studios
  cursor.close()

  query3 = "SELECT start_time, end_time FROM appointments WHERE artist_id = {}".format(design['artistid'])
  cursor = g.conn.execute(query3)
  bookings = []
  for result in cursor:
    bookings.append(result)
  cursor.close()
  appt_options['bookings'] = bookings
  print(appt_options)
  context = dict(data = appt_options)
  return render_template("book.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
