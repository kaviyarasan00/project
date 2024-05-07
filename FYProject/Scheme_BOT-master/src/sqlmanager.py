# import sqlite3
# conn = sqlite3.connect('data.db',check_same_thread=False)
# cur = conn.cursor();

import mysql.connector;

conn = mysql.connector.connect(
    user='root',
    password='Askavi499@',
    host='localhost',
    port='3306',
    database='fyproject'
)

cur = conn.cursor();

# create table questionset(question_id varchar(50),category varchar(50),question varchar(50),suggestions varchar(100),pair_key varchar(50),pair_value varchar(50),consider_as_a_category boolean,placeholder varchar(50));

# try:
#     cur.execute("create table userdata(userid varchar,username varchar,useremail varchar,userassword varchar)")
# except :
#     print("Table already created...")

def insertUserData(data):
    cur.execute(f"insert into userdata values('{data[0]}','{data[1]}','{data[2]}','{data[3]}')");
    conn.commit();

def isEmailPresent(email):
    cur.execute(f"select * from userdata where useremail='{email.lower()}'")
    return (len(cur.fetchall()) != 0)

def getDetail(email):
    cur.execute(f"select * from userdata where useremail='{email.lower()}'")
    return cur.fetchall()[0]

def displayUserData():
    cur.execute("select * from userdata")
    ls = cur.fetchall()
    for i in ls:
        print(i)
    return ls;

def getQuestioinSet():
    cur.execute("select distinct category from questionset;")
    ls = cur.fetchall();
    d = {}
    for i in ls:
        cur.execute(f"select * from questionset where category='{i[0]}'")
        js = cur.fetchall();
        ls = []
        for j in js:
            temp = {}
            temp["question_id"] = j[0]
            temp["category"] = j[1]
            temp["question"] = j[2]
            temp["suggestion"] = [] if (len(j[3]) == 0) else j[3].strip().split(",")
            temp["pair_key"]= j[4]
            temp["pair_value"]= j[5]           
            temp["consider_as_a_category"] = bool(j[6])
            temp["placeholder"] = j[7]
            ls.append(temp)
        d[i[0]] = ls;
    return d;

def getCategory():
    cur.execute("select distinct category from questionset;")
    ls = cur.fetchall()
    return [i[0] for i in ls];

def storeSchemeData(name,description):
    cur.execute(f"insert into scheme_data values('{name}','{description}')");
    conn.commit();

def getSchemeData():
    cur.execute("select * from scheme_data");
    return (cur.fetchall());

getSchemeData();

# d = {
#             "general": [
#                 {
#                     "question_id": "qno1",
#                     "question": "What is your Name ?",
#                     "suggestion": [],
#                     "key": "name",
#                     "value": "",
#                     "consider_as_a_category": False,
#                     "placeholder": "Enter your name ..."
#                 },
#                 {
#                     "question_id": "qno2",
#                     "question": "What is your Age ?",
#                     "suggestion": [],
#                     "key": "age",
#                     "value": "",
#                     "consider_as_a_category": False,
#                     "placeholder": "Enter your Age ..."
#                 },
#                 {
#                     "question_id": "qno3",
#                     "question": "What is your Occupation ?",
#                     "suggestion": ["Student", "Electriction", "Engineer", "Doctor", "Former"],
#                     "key": "occupation",
#                     "value": "",
#                     "consider_as_a_category": True,
#                     "placeholder": "Enter your Occupation ..."
#                 }
#             ],
#             "student": [
#                 {
#                     "question_id": "qno1",
#                     "question": "What is your Qualification ?",
#                     "suggestion": ["10th", "12th", "BE", "BTech", "MTech", "ME", "BSC"],
#                     "key": "qualification",
#                     "value": "",
#                     "consider_as_a_category": True,
#                     "placeholder": "Enter your Age ..."
#                 }
#             ],
#             "be": [
#                 {
#                     "question_id": "qno1",
#                     "question": "What is your Major ?",
#                     "suggestion": ["ECE", "MECT", "CSE", "EEE"],
#                     "key": "major",
#                     "value": "",
#                     "consider_as_a_category": False,
#                     "placeholder": "Enter your Major ..."
#                 }
#             ],
#             "former": [
#                 {
#                     "question_id": "qno1",
#                     "question": "Either you are Siru Former or Kuru Former",
#                     "suggestion": ["Siru", "Kuru"],
#                     "key": "Types of Former",
#                     "value": "",
#                     "consider_as_a_category": False,
#                     "placeholder": "Enter your Category ..."
#                 }
#             ]
#         }


# ls = ['general','student','be','former']
# count = 1;
# for i in ls:
#     for j in d[i]:
#         sug = ','.join(j['suggestion'])
#         print(sug)
#         cur.execute(f"""insert into questionset values('{"qid"+str(count)}','{i}','{j["question"]}','{sug}','{j["key"]}','{j["value"]}',{j["consider_as_a_category"]},'{j["placeholder"]}')""");
#         count+=1;
# conn.commit();
# displayUserData()

# insertUserData(('uid3', 'Kavi', 'kavi@gmail.com', '1234'))