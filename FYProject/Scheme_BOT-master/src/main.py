from flask import Flask,render_template,request,jsonify,redirect
from flask_cors import CORS
from sqlmanager import *;

app = Flask(__name__, template_folder='./templates')

CORS(app) 

class PyObject_SQL:
    def __init__(self):
        self.userdata = { }
        
    def userIdGenerator(self):
        ls = displayUserData()
        if ls:
          last_user_id = ls[-1][0].replace("uid", "")
          new_user_id = int(last_user_id) + 1
          return 'uid' + str(new_user_id)
        else:
        # Handle the case where ls is empty
         return 'uid1'  # or some default user ID


class PyObject_BOT:
    def __init__(self):
        self.question_set = getQuestioinSet()
        self.list_category = ["general"]
        self.list_index = 0;
        self.questions = [];
        self.question_number = 0;
    
    def question_order_generator(self):
        while self.list_index < len(self.list_category):
            for i in list(self.question_set[str(self.list_category[self.list_index])]):
                self.questions.append(i);
            self.list_index+=1;

class tempData:
    def __init__(self):
        self.userid = "";
                
po = PyObject_BOT();
pos = PyObject_SQL();
td = tempData();

@app.route('/')
@app.route('/signup')
def signup():
    return render_template("up.html")

@app.route('/signin')
def signin():
    return render_template("in.html")

@app.route('/home/<id>')
def home(id):
    return render_template('index.html',ls = getSchemeData());

@app.route('/in_up/<string>',methods=["POST","GET"])
def sign_in_up(string):
    if(request.method == "POST"):    
        useremail = request.form.get('useremail').lower().strip()
        userpassword = request.form.get('password1').strip()
        if(string == "signup"):
            userid = pos.userIdGenerator()
            username = request.form.get('username').strip().capitalize();
            if(isEmailPresent(useremail)):
                return render_template("up.html",msg = "Email id is already used")
            else:
                temp = []
                temp.append(userid)
                temp.append(username)
                temp.append(useremail)
                temp.append(userpassword)
                insertUserData(temp)
                return redirect('/signin')
        elif(string == "signin"):
            if(not isEmailPresent(useremail)):
                return render_template("in.html",msg = "Your Email Id is not Registered.")
            else:
                ls = getDetail(useremail)
                if(ls[2].lower() == useremail.lower() and ls[3] == userpassword):
                    return redirect('/home/'+ls[0]);
                else:
                    return render_template("in.html",msg = "Password is not matched.")
                        
    return "Not worked"

@app.route('/data',methods=["POST"])
def responseData():
    if(request.method == "POST"):
        obj = request.json
        if(len(obj) == 0):
            po.question_order_generator();
            jsontype = jsonify(po.questions[po.question_number])
            po.question_number += 1;
            return jsontype;
        else:
            if(obj['consider_as_a_category']):
                if(obj['value'].lower() in [i.lower() for i in obj['suggestion']]):
                    if(obj['value'].lower() not in po.list_category):
                        po.list_category.append(obj['value'].lower());
            print("cat",po.list_category)
            
            if(obj['value'] == '10th'):
                d = {
                    "question_id": "qno1",
                    "question": """Pradhan Mantri Kaushal Vikas Yojana (PMKVY): This scheme aims to provide skill development training to youth across India, including 10th pass students, to help them secure a better livelihood. <br>
                                National Apprenticeship Promotion Scheme (NAPS): NAPS offers apprenticeship training to 10th pass students, enabling them to gain practical skills and work experience.<br>
Mukhyamantri Yuva Swavalamban Yojana (MYSY): This scheme in Gujarat provides financial assistance for higher education to students who have passed the 10th standard.<br>
Mukhyamantri Yuva Nestham Scheme (MYNS): In Andhra Pradesh, this scheme provides financial assistance to unemployed youth, including 10th pass students, to reduce the burden of living expenses while they search for jobs.<br>
Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS): Some states offer health insurance schemes that cover 10th pass students and their families, providing them with access to quality healthcare services.<br>
Kishore Vaigyanik Protsahan Yojana (KVPY): This program by the Department of Science and Technology offers scholarships to students interested in pursuing a career in science, including those who have passed the 10th standard.<br>
National Scholarship Portal (NSP): The NSP provides various scholarships to students based on their academic performance, including those who have passed the 10th standard.""",
                    "suggestion": [],
                    "key": "name",
                    "value": "",
                    "consider_as_a_category": False,
                    "placeholder": "Enter your name ..."
                }
                jsontype = jsonify(d);
                return jsontype;
            elif(obj['value'] == '12th'):
                d = {
                    "question_id": "qno1",
                    "question": """Pradhan Mantri Kaushal Vikas Yojana (PMKVY): Offers skill development training to enhance employability for 12th pass students.<br>
National Apprenticeship Promotion Scheme (NAPS): Provides apprenticeship training to 12th pass students to gain practical skills and work experience.<br>
Pradhan Mantri Gramin Digital Saksharta Abhiyan (PMGDISHA): Aims to make 12th pass students digitally literate and offers training to use digital technologies.<br>
Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY): Focuses on rural youth, including 12th pass students, and provides skill development training for wage employment.<br>
Mukhyamantri Yuva Swavalamban Yojana (MYSY): Offers financial assistance for higher education to 12th pass students in Gujarat.""",
                    "suggestion": [],
                    "key": "name",
                    "value": "",
                    "consider_as_a_category": False,
                    "placeholder": "Enter your name ..."
                }
                jsontype = jsonify(d);
                return jsontype;
            elif(obj['value'] == 'ug'):
                d = {
                    "question_id": "qno1",
                    "question": """"Tamil Nadu Backward Classes Welfare Department Scholarships: This department provides scholarships to UG students belonging to backward classes to help them pursue higher education, including engineering courses.<br>
Tamil Nadu Minority Welfare Department Scholarships: UG students from minority communities can avail scholarships from this department to support their education, including engineering studies.<br>
Tamil Nadu State Government Merit Scholarship Scheme: This scheme provides financial assistance to meritorious UG students, including those studying engineering, based on their performance in the qualifying examination.""" ,
                    "suggestion": [],
                    "key": "name",
                    "value": "",
                    "consider_as_a_category": False,
                    "placeholder": "Enter your name ..."
                }
                jsontype = jsonify(d);
                return jsontype;
            elif(obj['value'] == 'ug' and 'engineering'):
                d = {
                    "question_id": "qno1",
                    "question": """Tamil Nadu Chief Minister's Merit Scholarship Scheme: This scheme provides financial assistance to meritorious students pursuing professional courses, including engineering, based on their performance in the qualifying examination.<br>
Tamil Nadu State Council for Science and Technology (TNSCST) Scholarships: TNSCST offers scholarships to students pursuing undergraduate and postgraduate courses in engineering, technology, and other fields related to science and technology.<br>
Tamil Nadu Educational Loan Scheme: The state government provides financial assistance to students pursuing higher education, including engineering, through educational loans at subsidized interest rates.<br>
Tamil Nadu Arasu Cable TV Corporation (TACTV) Free Coaching Scheme: This scheme provides free coaching to students belonging to economically weaker sections for various competitive examinations, including those related to engineering admissions and placements.""",
                    "suggestion": [],
                    "key": "name",
                    "value": "",
                    "consider_as_a_category": False,
                    "placeholder": "Enter your name ..."
                }
                jsontype = jsonify(d);
                return jsontype;
            elif(obj['value'] == 'Farmer' or 'farmer'):
                d = {
                    "question_id": "qno1",
                    "question": """Uzhavar Sandhai (Farmers' Market) Scheme: This scheme aims to eliminate middlemen and provide a direct market for farmers to sell their produce at fair prices. It helps in reducing post-harvest losses and ensuring better returns for farmers.<br>
Rythu Bima Group Life Insurance Scheme: Under this scheme, financial assistance is provided to the family of a farmer in case of death or permanent disability of the farmer. It aims to provide social security to farmers and their families.<br>
Farm Mechanization Scheme: This scheme provides subsidies and financial assistance to farmers for the purchase of agricultural machinery and equipment to improve productivity and efficiency in farming operations.<br>
Crop Insurance Scheme: The state government offers crop insurance schemes to protect farmers from crop losses due to natural calamities, pests, and diseases. It helps in reducing the financial risks associated with farming.<br>
Free Supply of Quality Seeds Scheme: Under this scheme, farmers are provided with quality seeds for various crops free of cost to improve crop yield and quality.<br>
Integrated Pest Management (IPM) Scheme: This scheme promotes the use of eco-friendly pest management practices among farmers to reduce the use of chemical pesticides and protect the environment.<br>
Dairy Development Scheme: This scheme aims to promote dairy farming in the state by providing subsidies and support for the establishment of dairy units, procurement of milch animals, and marketing of dairy products.""",
                    "suggestion": [],
                    "key": "name",
                    "value": "",
                    "consider_as_a_category": False,
                    "placeholder": "Enter your name ..."
                }
                jsontype = jsonify(d);
                return jsontype;
            else:
                if(len(po.questions)  > po.question_number):
                    jsontype = jsonify(po.questions[po.question_number])
                    po.question_number += 1;
                else:
                    po.question_order_generator();
                    if(len(po.questions) <= po.question_number):
                        jsontype = jsonify({'end_of_conversation' : True})
                    else:
                        jsontype = jsonify(po.questions[po.question_number])
                        po.question_number += 1;
                return jsontype;
@app.route('/admin',methods=["POST","GET"])
def admin_page():
    if(request.method == "POST"):
        name = request.form.get('scheme_name').strip()
        description = request.form.get('scheme_description').strip()
        storeSchemeData(name,description)
        return render_template("admin_page.html")
    else:
        return render_template("admin_page.html");
        
if __name__ == '__main__':
    app.run(debug=True)


    