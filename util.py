import pymysql
def get_mysql_result():
    db = pymysql.connect(host='120.77.253.60',user='shuowen',passwd='QuGSlFdQMRo9nWGWWN2o',database='shuowenuser')
    cursor = db.cursor()
    sql='select * from user'
    cursor.execute(sql)
    myresult = cursor.fetchall()
    return myresult