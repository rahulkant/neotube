import MySQLdb

db = MySQLdb.connect('localhost', 'root','vegeta','neoyoutube')
cursor  = db.cursor()
sql = ""
print cursor.execute(sql)
db.close()
