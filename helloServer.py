from flask import Flask, render_template, request, redirect, url_for

import sqlite3


DATABASE = "greetings_earthlings.db"

# __init__.py
# this 'app' variable is referenced in the wsgi.py file.
#  if you have done anything different you may need to adapt code through your
#   .py server script and the wsgi.py file
app = Flask(__name__)

# config.py
# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# can uncomment for Gunicorn deployment on Cardiff University OpenShift
#  but as demonstrated in this example, it works without
# (make sure gunicorn is in the requirements.txt folder)
# workers = int(os.environ.get('GUNICORN_PROCESSES', '3'))
# threads = int(os.environ.get('GUNICORN_THREADS', '1'))

# may need to uncomment the below two lines but works without,
#  Openshift sets https automatically, pages will be available at http, so will
#    need to navigate to a http<your url from openshift> manually first.
# forwarded_allow_ips = '*'
# secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

# if separate config file, this would be there as an Object
# SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-secret-key-for-me'
#
# add database link, if needed
#
#
# __init.py__
# and establish db var for reference later


@app.route("/")
def home():
    return "....server is running"


@app.route("/hello/")
@app.route("/hello/<firstname>/")
@app.route("/hello/<firstname>/<surname>")
def hello(**names):
    '''
      This page should have a form and then allow the user to input some data / answer
        a question and then receive some immediate feedback without the URL changing.
    '''

    try:
        firstname = names["firstname"]
    except (KeyError, AttributeError) as e:
        print(e)
        firstname = "world"

    try:
        surname = names["surname"]
    except (KeyError, AttributeError) as e:
        print(e)
        surname = ""

    return render_template('front_1.html',
                            title='home',
                            firstname=firstname,
                            surname=surname)


@app.route("/homeForm_1", methods=["POST"])
def home_form_1():
    if request.method == "POST":
        n = request.form['firstname']
        s = request.form['surname']
        print(f"hello, {n} {s}!")

        # write the firstname and surname into the .sqlite database here
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # table "names" features 3-columns, but ID auto-increments so we
            #  do not have to specify a value for this.
            cur.execute("INSERT INTO names ('first_name', 'surname') VALUES (?,?)",(n, s))
            conn.commit()
            db_msg = "name successfully added"
        except:
            conn.rollback()
            db_msg = "error in insert operation"
        finally:
            print(db_msg)  # output to terminal
            conn.close()

    return redirect(url_for("hello", firstname=n, surname=s))


@app.route("/list_greeted", methods=["GET", "POST"])
def database_interface():
    # call all items from database here
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM names")
        db_data = cur.fetchall()
        # print(db_data, type(db_data))
        # a list of tuples is returned, each tuple in the list has 3 items (0,1,2)
        #  tuple[0] is ID, tuple[1] first_name, tuple[2] surname.
        #   Remember this for refering to variables in html Jinja templating
        conn.commit()
        db_msg = "data successfully obtained"
    except:
        conn.rollback()
        db_msg = "error fetching table data"
    finally:
        print(db_msg)
        conn.close()

    return render_template("greeted.html", title="hellod to", db_data=db_data)
