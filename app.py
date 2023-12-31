from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random
import smtplib
import json

app = Flask(__name__)
file = open('config.json')
Login_creds = json.load(file)

MongoDB_ID = Login_creds['db_login']
MongoDB_Pass = Login_creds['db_pass']
ComUnity_ID = Login_creds['mail_id']
ComUnity_Pass = Login_creds['mail_pass']

uri = f'mongodb+srv://{MongoDB_ID}:{MongoDB_Pass}@cluster0.pyebiiy.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)

db = client['Alumni_Data']

y_l = db.list_collection_names()
y_l_int = sorted(map(int, y_l))
years_loaded = list(map(str, y_l_int))

OTP_dict = {}

name_modif = {}

try:
    client.admin.command('ping')
except Exception as e:
    print(e)

@app.route('/')
def Landing_Page():
   return render_template('index.html', slct_yr = years_loaded, update_confirmed = "False")

@app.route('/SignIn')
def SignIn_page():
   return render_template('login.html', slct_yr = years_loaded)

@app.route('/SearchAlumni', methods = ['GET','POST'])
def Seacrh_alumni():
   allrec = {}
   results = []
   if request.method == 'POST':
      name = ""
      i_name = request.form.get('Alname')
      i_name = i_name.lower()
      name_array = i_name.split(" ")
      for nms in name_array:
         name = name + nms.capitalize() + " "
      name = name.rstrip()
      course = request.form.get('course')
      year = request.form.get('year')
      if name == "":
         collection = db[str(year)]
         allrec = collection.find({"COURSE" : str(course)}) 
         for x in allrec:
            document_dict = dict(x)
            results.append(document_dict)
      else:
         collection = db[str(year)]
         allrec = collection.find({"NAME" : str(name), "COURSE" : str(course)}) 
         for x in allrec:
            document_dict = dict(x)
            results.append(document_dict)
         

   return render_template('index.html', rec = results, slct_yr = years_loaded, update_confirmed = "False")

@app.route('/LoginAlumni', methods = ['GET', 'POST'])
def InitLogin():
   au_mail = []
   if request.method == 'POST':
      t_name = ""
      i_name = request.form.get('InpName')
      i_name = i_name.lower()
      name_array = i_name.split(" ")
      for nms in name_array:
         t_name = t_name + nms.capitalize() + " "
      t_name = t_name.rstrip()
      t_email = request.form.get('InpEmail')
      t_year  = request.form.get('year')
      collection = db[str(t_year)]
      allrec = collection.find({"NAME" : str(t_name)})
      for rec in allrec:
         au_mail = rec['EMAIL']
      if au_mail == str(t_email):
         otp = str(random.randint(100000,999999))
         OTP_dict[str(t_name)] = otp
         name_modif[str(t_name)] = t_year
         with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(ComUnity_ID,ComUnity_Pass)
            message = f'Subject: OTP for Alumni Authentication \n\n OTP for login is {otp}'
            smtp.sendmail('cic.community2023@gmail.com', [str(t_email), 'nikunjsaini37@gmail.com']  ,message)
            return redirect(url_for('RedirectLogin'))
      else:
         return render_template('Error.html', error_code = "1")
      
   return render_template('Error.html', error_code = "2")

@app.route('/Redirect_OTP')
def RedirectLogin():
   return render_template('OTPauth.html')

@app.route('/Validate_OTP', methods = ['GET', 'POST'])
def ValidateOTP():
   if request.method == 'POST':
      v_name = ""
      otp_auth_name = request.form.get('InpName')
      otp_auth_name = otp_auth_name.lower()
      name_array = otp_auth_name.split(" ")
      for nms in name_array:
         v_name = v_name + nms.capitalize() + " "
      v_name = v_name.rstrip()
      v_OTP = request.form.get('OTP')

      if v_name in OTP_dict and OTP_dict[v_name] == v_OTP:
         del OTP_dict[v_name]
         return redirect(url_for('Open_modifier', auth_name = v_name))
      else:
         del OTP_dict[v_name]
         return render_template('Error.html', error_code = "3")
   
   return render_template('Error.html', error_code = "2")

# @app.route('/Modif', methods = ['GET', 'POST'])
# def ModifyData():
#    name = "Ishan Bansal"
#    year = "2020"
#    collection  = db[year]
#    rec = collection.find_one({"NAME" : name})
#    return render_template('ModifyData.html',prev_data = rec, b_year = year)

@app.route('/Open_Modif/<auth_name>')
def Open_modifier(auth_name):
   name = auth_name
   year = name_modif[name]
   del name_modif[name]
   collection  = db[year]
   rec = collection.find_one({"NAME" : name})
   return render_template('ModifyData.html', prev_data = rec, b_year = year)

@app.route('/UpdateData', methods = ['GET', 'POST'])
def Update():
   if request.method == 'POST':
      name = request.form.get('hidden_name')
      year = request.form.get('hidden_year')
      job = request.form.get('job_title')
      location = request.form.get('location')
      linkedin = request.form.get('linkedin')
      website = request.form.get('website')
      email = request.form.get('m_email')
      collection = db[str(year)]
      s_query = {"NAME" : name }
      c_query = { "$set" : {"WEBSITE": website ,"JOB": job, "LOCATION": location, "LINKEDIN": linkedin, "EMAIL": email}}
      confirmed = collection.find_one_and_update(filter = s_query, update = c_query)
      if confirmed:
         return redirect('/MainPage')
      else:
         render_template('Error.html', error_code = "4")
   else:
      return render_template('Error.html', error_code = "2")
   
@app.route('/MainPage')
def MainPage():
   return render_template('index.html', update_confirmed = "True", slct_yr = years_loaded)

if __name__== "__main__":
   app.debug = True
   app.run()
