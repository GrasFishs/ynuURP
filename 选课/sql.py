import pymysql

db = pymysql.connect('localhost','root','gotoAnd@123','urp',use_unicode=True, charset="utf8")

cursor = db.cursor()

sql = "SELECT * FROM GRADE WHERE course_grade > '%d'" % 90

try:
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row,end=" ")

except Exception as e:
    print(e)
    db.rollback()

db.close()