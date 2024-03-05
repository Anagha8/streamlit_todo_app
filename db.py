import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')


def add_data(task,task_status,task_due_date):
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
	conn.commit()

def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data=c.fetchall()
	return data

def view_unique_task():
	c.execute('SELECT DISTINCT task FROM taskstable')
	data=c.fetchall()
	return data

def get_task(task):
    c.execute('SELECT * FROM taskstable WHERE task=?', (task,))
    data = c.fetchall()
    return data

def edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()