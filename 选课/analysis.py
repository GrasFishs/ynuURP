import numpy as np
import matplotlib.pyplot as plt
import pymysql

db = pymysql.connect('localhost','root','gotoAnd@123','urp',use_unicode=True, charset="utf8")
cursor = db.cursor()
sql = "SELECT course_name,course_grade FROM GRADE"
infos = []
map = {"60-":0,"60~70":0,"70~80":0,"80~90":0,"90+":0}
try:
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        infos.append(r[0])
        grade = r[1]
        if grade>=60 and grade<70:
            map["60~70"] += 1
        elif grade>=70 and grade<80:
            map["70~80"] += 1
        elif grade >= 80 and grade < 90:
            map["80~90"] += 1
        elif grade >= 90:
            map["90+"] += 1
        elif grade < 60:
            map["60-"] += 1
except Exception as e:
    print(e)
    db.rollback()

plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
# autopct ，show percet
plt.pie(x=list(map.values()), labels=map.keys(), autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.8)

plt.show()