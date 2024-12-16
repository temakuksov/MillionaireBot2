import sqlite3

db_name = 'demo.db'

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
    print(q)
    return q


# добавление нового вопроса -
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
