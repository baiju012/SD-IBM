# Import the Flask framework for creating a web application
from flask import Flask, render_template, request, session

# Import IBM Db2 database library for database connectivity
import ibm_db

# Import IBM Cloud Object Storage and Boto3 library for cloud file storage
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Import the 'os' module to handle various OS-related functions
import os

# Import 're' module for regular expressions, used for email validation
import re

# Import the 'random' and 'string' modules for generating random passwords
import random
import string

# Import 'datetime' module for working with date and time
import datetime

# Import 'requests' library for sending HTTP requests (used for sending emails)
import requests



app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT=32286; UID=ryf63762;PASSWORD=83jNg2jpp4x60BeD; SECURITY=SSL;SSLServerCertificate = DigiCertGlobalRootCA.crt", "", "")
url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"


@app.route("/")

@app.route("/register", methods=['GET'])
def show_registration_form():
    return render_template("registration.html")


@app.route("/register", methods=['POST', 'GET'])
def signup():
    msg = ''  # Initialize an empty message

    if request.method == 'POST':
        # Get user registration details from the registration form
        name = request.form["sname"]
        email = request.form["semail"]
        username = request.form["susername"]
        role = int(request.form['role'])

        # Generate a random password
        password = ''.join(random.choice(string.ascii_letters) for i in range(0, 8))

        # Default registration link
        link = 'https://gkv.ac.in'

        print(password)

        # Check if the provided email is already registered
        sql = "SELECT * FROM register WHERE email= ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            msg = "Already Registered"  # If the email is already in use, display a message

            return render_template('registration.html', error=True, msg=msg)

        # Check if the email is valid using a basic regex pattern
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address!"

        else:
            # Insert the registration details into the database
            insert_sql = "INSERT INTO register VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)

            # Bind the parameters to the SQL statement
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, username)
            ibm_db.bind_param(prep_stmt, 5, role)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)

            # Prepare an email message to send to the registered user
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": email}],
                        "subject": "Student Account Details"
                    }
                ],
                "from": {"email": "216301031@gkv,ac.com"},
                "content": [
                    {
                        "type": "text/plain",
                        "value": "Dear {} ,  \n Welcome to Grukul kangri University, Here are the details to log in to your student portal:\n"
                                 "Your Username: {} \n  Password: {}  \n"
                                 "Thank you \n Sincerely\n Office of Admissions\n Grukul kangri University \n"
                                 "E-Mail: admission@gkv.ac.in ; Website: www.gkv.ac.in"
                                 .format(name, username, password)
                    }
                ]
            }
            
            
            
            
            

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
