"""
  尝试调用mysql
"""
import pymysql
def test_connect():
    db = pymysql.connect('127.0.0.1', 'root', 'phpcj', 'post_emt_log')
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    #cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # sql = """CREATE TABLE EMPLOYEE (
    #          FIRST_NAME  CHAR(20) NOT NULL,
    #          LAST_NAME  CHAR(20),
    #          AGE INT,
    #          SEX CHAR(1),
    #          INCOME FLOAT )"""
    sql = """
create table post (
    id int unsigned primary key auto_increment,
    post_id int not null,
    model_name varchar(50) not null,
   created int(10) default 0
);
"""
    cursor.execute(sql)

    db.close()

test_connect()


create_table_sql = """
create table post (
    id int unsigned primary key auto_increment,
    post_id int not null,
    model_name varchar(50) not null,
   created int(10) default 0
);
"""