from flask import Flask , request , render_template 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import __init__


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'Hello World!'

db = SQLAlchemy(app)
#dbModel
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    fname = db.Column(db.String(200), nullable = False) 
    lname = db.Column(db.String(200), nullable = False) 
    weight = db.Column(db.Integer, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Integer, nullable = False)
    bp_s =  db.Column(db.Integer, nullable = False)
    bp_d =  db.Column(db.Integer, nullable = False)
    chol =  db.Column(db.Integer, nullable = False)



@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")
 
 

@app.route('/submit', methods=["GET","POST"])
def submit():
    if request.method == "POST":
     fname = request.form.get('fname')
     lname = request.form.get('lname')
     age = request.form.get('age')
     weight = request.form.get('weight')
     height = request.form.get('height')
     bp_s = request.form.get('bp_s')
     bp_d = request.form.get('bp_d')
     chol = request.form.get('chol')
     
    try:
        age = int(age) if age else 0
        weight = float(weight) if weight else 0
        height = float(height)/100 if height else 0
        bp_s = float(bp_s) if bp_s else 0
        bp_d = float(bp_d) if bp_d else 0
        
        chol = int(chol) if chol else 0
    except ValueError:
        return "Error: Please enter a valid numbers"
    try:
     bmi = weight/(height ** 2)
     
     risk_score = 0
     
     if bmi < 18.5:
        bmi_status =("Underweight","danger")
        risk_score += 1
     elif  18.5 <= bmi <= 24.9 :
         bmi_status = ("Normal","success")    
     elif 25 <= bmi <= 29.9:
        bmi_status=("you are overweight", "warning")
        risk_score += 1
     else:
        bmi_status = ("Obese","danger")
        risk_score += 2 
    
    #Blood pressure check
     if bp_s <120 or bp_d < 80:        
        bp_status =("Normal","success")
     elif(120 <= bp_s <=129) and (60 <= bp_d < 80):
        bp_status =("Elevated","info")
        risk_score += 1
     elif(130 <= bp_s <= 139) or (81 <= bp_d <= 89):
         bp_status =("Hypertension Stage-1","warning")
         risk_score += 1
     elif(140 <= bp_s <= 180) or (90 <= bp_d <= 120):
         bp_status =("Hypertension Stage-2","danger")
         risk_score += 1
     else:
         bp_status =("High","danger")
         risk_score += 2
    
    #Cholestrol check
     if chol < 240:
         chol_status = ("Normal" , "success")
     elif chol <= 239:
         chol_status = ("Borderline","warning")
         risk_score += 1
     else:
         chol_status = ("High","danger")
         risk_score += 2
        
    
    #Risk category   
     if risk_score <= 1 or risk_score == 0:
        risk_status = ("Low Risk","success")
        guidance = "Your results look good overall. Keep maintaining a balanced diet, regular exercise, and routine check-ups."

     elif 2 <= risk_score <= 3:
        risk_status = ("Moderate Risk","warning")
        guidance = "Some of your values are above normal ranges. It is advisable to monitor your lifestyle, reduce salt/fat intake, and exercise regularly."
     else:
        risk_status = ("High Risk","danger")
        guidance = "Your results suggest a high health risk. Please consult a healthcare professional for further evaluation and guidance."
        
     new_user =Users(
         fname=fname, #type:ignore
         lname = lname,#type:ignore
         weight=weight,#type:ignore
         age=age,#type:ignore
         height=int(height *100),#type:ignore
         bp_s=bp_s,#type:ignore
         bp_d=bp_d,#type:ignore
         chol=chol#type:ignore
         
     )
     db.session.add(new_user)
     db.session.commit()
        
    except Exception as e:
            return f"Error in calculation: {str(e)}"
        
    
    
      
    return render_template("results.html", fname=fname, lname=lname, age=age, risk_status=risk_status, risk_score = risk_score, chol=chol, bp_s=bp_s , bp_d=bp_d, bmi_status=bmi_status,chol_status=chol_status, bp_status=bp_status, guidance=guidance, now=datetime.now(), bmi=round(bmi,2))

if __name__ == '__main__': 
  app.run(debug = True)
