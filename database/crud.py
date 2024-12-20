import sqlite3
import os

db_name = os.getenv('SQLITE')

# получение из бд случайного вопроса заданной сложности
def get_question(level):
    cn = sqlite3.connect(db_name)
    # print('сложность=',[level])
    sql = 'SELECT * FROM Questions WHERE Level = ? ORDER BY random() LIMIT 1'
    cur = cn.cursor()
    cur.execute(sql, [level])
    q = cur.fetchone()
    cn.commit()
    cur.close()
    cn.close()
    # print(q)
    return q


# добавление нового вопроса - не реализовано
def add_question(level):
    cn = sqlite3.connect(db_name)
    # print('сложность=',[level])
    sql = 'SELECT * FROM Questions WHERE Level = ? ORDER BY random() LIMIT 1'
    cur = cn.cursor()
    cur.execute(sql, [level])
    q = cur.fetchone()
    cn.commit()
    cur.close()
    cn.close()
    print(q)
    return q
