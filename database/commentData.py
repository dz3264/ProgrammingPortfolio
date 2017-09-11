import sqlite3
import datetime
import time
from time import gmtime, strftime

conn = sqlite3.connect('CommentTable.db')
comment = conn.cursor()

def create_table():
    comment.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(id INTEGER, user TEXT, context TEXT, date TEXT, parent INTEGER, reply INTEGER, replyName TEXT, file TEXT)')


def dynamic_data_entry(dataId, userName, commentContext, parentId, replytTo,fileName):
    replyName = read_name(replytTo)
    #print(replytTo)
    #print(replyName)
    user = userName
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%M-%D %H: %M: %S'))
    context = commentContext
    parent = parentId
    reply = replytTo
    file = fileName
    comment.execute("INSERT INTO stuffToPlot(id, user, context, date, parent, reply,replyName, file) VALUES (?,?,?,?,?,?,?,?)",
                    (dataId, user, context, date, parent, reply,replyName, file))
    conn.commit()

def read_from_db(fileName):
    comment.execute("SELECT * FROM stuffToPlot WHERE file = (?)",(fileName,))
    data = comment.fetchall()

    return data

def read_parent(fileName):
    comment.execute("SELECT * FROM stuffToPlot WHERE file = (?)  AND parent is NULL",(fileName,))
    data = comment.fetchall()

    return data

def read_child(fileName, parent):
    comment.execute("SELECT * FROM stuffToPlot WHERE file = (?)  AND parent = (?)",(fileName,parent,))
    data = comment.fetchall()
    #print(data)
    return data

def data_size():
    comment.execute("SELECT * FROM stuffToPlot")
    data = comment.fetchall()
    size = len(data)
    return size

def read_name(id):
    comment.execute("SELECT * FROM stuffToPlot WHERE id = (?) ", (id,))
    data = comment.fetchall()
    if (len(data) <= 0):
        return None
    else:
        return data[0][1]

def read_test():
    comment.execute("SELECT * FROM stuffToPlot WHERE id = (?) ", (data_size()-1,))
    data = comment.fetchall()
    return data[0]
#create_table()
#data_entry()


#dynamic_data_entry(0,'dz3264','TEST2',None, None,'Position.java')
#time.sleep(1)
#dynamic_data_entry(1,'feitianjitui','666',0, None, 'Position.java')
#time.sleep(1)
#dynamic_data_entry(2,'btyao2','hehe',None, 1, 'Position.java')
#time.sleep(3)
#dynamic_data_entry(3,'btyao2','hehe',None, None, 'Main.java')

#dynamic_data_entry(4,'schen154','TEST2333',None, None,'Position.java')

#print(read_from_db('Position.java'))
#print(read_parent('Position.java'))
#print(read_child('Position.java',0))
#read_name(0)
#read_name(1)
#print(data_size())
#comment.close()
#conn.close()
#print(read_test())



# Source: https://www.youtube.com/watch?v=qfGu0fBfNBs