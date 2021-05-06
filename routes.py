from app import app
from Lms import *
from google_classroom import *
import dateparser, datetime, hashlib
from flask import render_template

subjects = {}

@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    global subjects
    #Reqd: [[Subject_Name_1, [[Res-Title, URL], [Res-Titel, URL]], [[S-Title, URL], [S-Title, URL]]], [Subject_Name_2, [[Res-Title, URL], [Res-Titel, URL]], [[S-Title, URL], [S-Title, URL]]], .....................]
    #google: [[URL, Name, Date posted, Due Date, Max possible marks, Marks received, Submitted/Assigned/Graded],...]
    #google_s: [[URL, Name],..]
    l, g = [], []
    #print(google_s, google)
    #Latest assignments based on due date
    for i in range(len(google_s)):
        base = hashlib.md5(google_s[i][1].encode()).hexdigest()
        subjects[base] = [google_s[i][1], google[i]]
        temp = [[google_s[i][1], base], [[], []]]
        for j in range(min(2, len(google[i][1]))):
            temp[-1][j] = [google[i][1][j][1], google[i][1][j][0]]
        temp.append([[], []])
        ct = 0;
        for j in google[i][0]:
            if j[3][0] == "N":
                temp[-1][ct] = [j[1],j[0]]
                ct += 1
            else:
                if ',' in j[3]:
                    #print(j[3])
                    t = dateparser.parse(" ".join(j[3].split(" ")[1:]), date_formats=["%b %m %I %p"], languages=["en"])
                    c = datetime.datetime.now()
                    if t >= c:
                        temp[-1][ct] = [j[1], j[0]]
                        ct += 1
                else:
                    t = dateparser.parse(j[3], date_formats=["%b %m %I %p"], languages=["en"]).date()
                    c = datetime.datetime.now().date()
                    if t >= c:
                        temp[-1][ct] = [j[1], j[0]]
                        ct += 1
            if ct == 2:
                break
        l.append(temp)
    for i in range(len(lms_s)):
        base = hashlib.md5(lms_s[i][1].encode()).hexdigest()
        subjects[base] = [lms_s[i][1], lms[i]]
        temp = [[lms_s[i][1], base], [[], []], [[], []]]
        ct, ct1 = 0, 0
        for j, k in lms[i].items():
            for z in k[-1:0:-1]:
                details = list(z.items())[0][1]
                if details.get("is_resource") == 1 and ct != 2:
                    temp[1][ct] = [list(z.items())[0][0], details.get('url')]
                    ct += 1
                elif details.get("is_resource") == 0 and ct1 != 2:
                    temp[2][ct1] = [list(z.items())[0][0], details.get("url")]
                    ct1 += 1
        l.append(temp)
        # l = [['Applied ML with TF Batch 1', [[], []], [['IA2', 'https://classroom.google.com/u/0/c/MjY0MTE2NzQ3MjI0/a/MjY0MTE2NzQ3MjUx/details'], ['IA1', 'https://classroom.google.com/u/0/c/MjY0MTE2NzQ3MjI0/a/MjY0MTE2NzQ3MjM4/details']]], ['Cryptography and System Security_A_20_21', [['TY CSS IA-2 Approved -Not Approved LISt', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=21123'], ['IA-1 Topic Approval List', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=19234']], [[], []]],
    # ['Cryptography and System Security_A_20_21', [['TY CSS IA-2 Approved -Not Approved LISt', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=21123'], ['IA-1 Topic Approval List', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=19234']], [[], []]],
    # ['Cryptography and System Security_A_20_21', [['TY CSS IA-2 Approved -Not Approved LISt', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=21123'], ['IA-1 Topic Approval List', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=19234']], [[], []]],
    # ['Cryptography and System Security_A_20_21', [['TY CSS IA-2 Approved -Not Approved LISt', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=21123'], ['IA-1 Topic Approval List', 'https://lms-kjsce.somaiya.edu/mod/resource/view.php?id=19234']], [[], []]]]
    # print(l)
    print(subjects)
    return render_template("home.html", course = l)

@app.route("/subject/<string:id>")
def subject(id):
    value = subjects.get(id)
    r, s = [], []
    if type(value[1]) is list:
        for j in value[1][0]:
            s.append([j[1], j[0], j[2], j[3], j[-1], j[-2], j[-3]])
        for j in value[1][1]:
            r.append([j[1], j[0], j[2]])
    else:
        for j, k in value[1].items():
            for z in k[-1:0:-1]:
                details = list(z.items())[0][1]
                if details.get("is_resource") == 1:
                    r.append([list(z.items())[0][0], details.get('url'), details.get("upload_time")])
                elif details.get("is_resource") == 0:
                    s.append([list(z.items())[0][0], details.get("url"), details.get("upload_time"), details.get("due_date"), details.get("submission"), details.get("marks_received"), details.get("max_marks")])
    return render_template("subject.html", resources = r, assignments = s, subject = value[0])