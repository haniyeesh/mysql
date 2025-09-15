import mysql.connector as mysql
from jalase10 import *
from dl import *


def connect_to_database():
    try:                                                    #etesal be databse(mysql)

        con = mysql.connect(host='localhost', user='root', password='P@ssw0rd')
        return con
    except Exception as x:
        print(x)


def create_database():
    con = connect_to_database()
    cur = con.cursor()
    cur.execute('SHOW DATABASES')
    lst_dbs = cur.fetchall()
    print(lst_dbs)
    b = False                                         #sakhtan database amozeshgah
    for i in lst_dbs:
        if 'amozeshgah' in i[0]:
            b = True
    # print('database exists ....') if b else cur.execute('CREATE DATABASE amozeshgah')
    if b:
        print("database already exist")
    else:
        cur.execute('CREATE DATABASE amozeshgah')
        print('create database ...')


def connect_db_amozeshgah():
    con = mysql.connect(user='root', password='P@ssw0rd', database='amozeshgah')
    return con
# etesal be khode database amozeshgah


def create_table_teacher():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE teacher(
                    name_t nvarchar(20) not null ,
                    last_name_t nvarchar(20) not null,
                    code_t int not null  PRIMARY KEY ,
                    dtb_t date,
                    phone_number_t nvarchar(11) not null,
                    madrak_t nvarchar(20) not null,
                    class_t nvarchar(20) not null,
                    lesson_t nvarchar(20) not null,
                    bimeh_t nvarchar(10) not null     #boolean
                    
    )    
    ''')
        print('creating table teacher...')
        print(" teacher table created ")
    except Exception:
        print(" teacher table already exists")


# def delete_table_teacher():
#     con = connect_db_amozeshgah()                  #delete hame table
#     cur = con.cursor()
#     cur.execute('DROP TABLE IF EXISTS teacher')


def insert_record_table_teacher():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_t FROM teacher')
            lst = cur.fetchall()
            try:
                x = int(input('enter the teacher id  : '))
            except ValueError:
                print('error')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:
                na = input('enter the teacher name : ')
                if len(na) == 0:
                    na = '... '
                last_name = input("enter the teacher last name: ")
                if len(last_name) == 0:
                    last_name = '... '
                phone_number = input("enter the teacher phone number :")
                if len(phone_number) == 0:
                    phone_number = '... '
                madrak = input("enter the teacher sertificate: ")
                if len(madrak) == 0:
                    madrak = '... '
                classes = input("enter the teachers classes :")
                if len(classes) == 0:
                    classes = '... '
                lesson = input("enter the teacher lesson: ")
                if len(lesson) == 0:
                    lesson = '... '
                bimeh = input("dose teacher have  insurance (yes / no ): ")
                if len(bimeh) == 0:
                    bimeh = '... '
                y = int(input('birthday year : '))
                m = int(input('birthday mounth : '))
                d = int(input('birthday day : '))
                import datetime
                try:
                    d = datetime.date(y, m, d)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                print(d)
                sql = 'INSERT INTO teacher (code_t, name_t, last_name_t, phone_number_t, madrak_t, class_t, lesson_t, bimeh_t, dtb_t) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)'
                val = (x, na, last_name, phone_number, madrak, classes, lesson, bimeh, d)
                cur.execute(sql, val)
                con.commit()
                print(' add teacher ...')
                back_up_teacher()
                break
            else:
                print('code teacher exits ...')
        n = input(" do you want to enter code to add another teacher info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def query_code_teacher():
    while True:
        code = int(input('enter the teacher code witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM teacher  WHERE code_t ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have teacher with your entered code')
        else:
            print(lst)
        n = input(" do you want to enter code to search another teacher info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def list_column():
    con = connect_db_amozeshgah()        #hame joziat sakhtari table ro neshun mide na dadehaye tusho
    cur = con.cursor()
    cur.execute('describe teacher')
    lst = cur.fetchall()
    print(lst)


def change_teacher():
    while True:
        code = int(input('code for search: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_t FROM teacher WHERE code_t = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f'SELECT * FROM teacher WHERE code_t = {code}')
            print(cur.fetchone())
            print("warning!! you cant change the teacher id !!")
            print('\t 1 - change name ')
            print('\t 2 - change last name ')
            print('\t 3 - change date  ')
            print('\t 4 - change phone number  ')
            print('\t 5 - change madrak  ')
            print('\t 6 - change classes  ')
            print('\t 7 - change lessons  ')
            print('\t 8 - change bimeh  ')
            ans = input('enterd the number of your choice : ')
            if ans == '1':
                newname = input('new name : ')
                cur.execute(f"UPDATE teacher SET  name_t = '{newname}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()
            elif ans == '2':
                newlastname = input('new last name : ')
                cur.execute(f"UPDATE teacher SET  last_name_t = '{newlastname}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()

            elif ans == '3':
                newy = int(input('new birthday year : '))
                newm = int(input('new birthday mounth : '))
                newd = int(input('new birthday day : '))
                import datetime
                try:
                    d = datetime.date(newy, newm, newd)
                    con.commit()
                    print("changing was succesfully")
                    back_up_teacher()

                except ValueError:
                    d = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE teacher SET  dtb_t = '{d}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()


            elif ans == '4':

                phone_number = input("enter the teacher new phone number :")
                cur.execute(f"UPDATE teacher SET  phone_number_t = '{phone_number}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()
                if len(phone_number) == 0:
                    phone_number = '... '




            elif ans == '5':
                newmadrak = input('new madrak : ')
                cur.execute(f"UPDATE teacher SET  madrak_t = '{newmadrak}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()

            elif ans == '6':
                newclasses = input('zoj / fard  : ')
                cur.execute(f"UPDATE teacher SET  class_t = '{newclasses}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()

            elif ans == '7':
                newlessons = input('new lessons : ')
                cur.execute(f"UPDATE teacher SET  lesson_t= '{newlessons}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()

            elif ans == '8':
                newbimeh = input('new bimeh : ')
                cur.execute(f"UPDATE teacher SET  bimeh_t = '{newbimeh}' WHERE code_t = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_teacher()
        n = input(" do you want to enter another code to change another teacher info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def delete_teacher():              #etelaat code mored nazar kamellan pak mishavad
    while True:
        code = int(input('enter the teacher code witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_t FROM teacher WHERE code_t = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM teacher WHERE code_t ={code}")
            print("             deleting was succesfully    ")
            back_up_teacher()
            con.commit()
        n = input(" do you want to enter another code  ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_table_student():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
                    CREATE TABLE student(
                            name_s nvarchar(20) not null ,
                            last_name_s nvarchar(20) not null,
                            code_s int not null  PRIMARY KEY ,
                            dtb_s date,
                            phone_number_s nvarchar(11) not null,
                            teacher_s nvarchar(20) not null,
                            lesson_s nvarchar(20) not null
                           

            )    
            ''')
        print('creating student table...')
        print("student table created ")
    except Exception:
        print(" student table already exists")


def insert_record_table_student():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_s FROM student')
            lst = cur.fetchall()
            try:
                x = int(input('enter the student id  : '))
            except ValueError:
                print('error')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:
                na = input('enter the student name : ')
                if len(na) == 0:
                    na = '... '
                last_name = input("enter the student last name: ")
                if len(last_name) == 0:
                    last_name = '... '
                try:
                    phone_number = input("enter the student phone number :")
                    if len(phone_number) == 0:
                        phone_number = '... '
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    phone_number = "..."
                y = int(input('birthday year : '))
                m = int(input('birthday mounth : '))
                d = int(input('birthday day : '))
                import datetime
                try:
                    d = datetime.date(y, m, d)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                print(d)
                sql = 'INSERT INTO student (code_s, name_s, last_name_s, phone_number_s, dtb_s) VALUES ( %s, %s, %s, %s,%s)'
                val = (x, na, last_name, phone_number, d)
                cur.execute(sql, val)
                con.commit()
                print(' add student ...')
                back_up_student()
                break
            else:
                print('student code has existed ...')
        n = input(" do you want to enter code to add another student info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def query_code_student():
    while True:
        code = int(input('enter the student code witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM student WHERE code_s ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have student with your entered code')
        else:
            print(lst)
        n = input(" do you want to enter code to search another student info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def change_student():
    while True:
        code = int(input('code for search to change the information: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_s FROM student WHERE code_s = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f'SELECT * FROM student WHERE code_s = {code}')
            print(cur.fetchone())
            print("warning!! you cant change the student id !!")
            print('\t 1 - change name ')
            print('\t 2 - change last name ')
            print('\t 3 - change date  ')
            print('\t 4 - change phone number  ')
            ans = input('enterd the number of your choice : ')
            if ans == '1':
                newname = input('new name : ')
                cur.execute(f"UPDATE student SET  name_s = '{newname}' WHERE code_s = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_student()
            elif ans == '2':
                newlastname = input('new last name : ')
                cur.execute(f"UPDATE student SET  last_name_s = '{newlastname}' WHERE code_s = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '3':
                newy = int(input('new birthday year : '))
                newm = int(input('new birthday mounth : '))
                newd = int(input('new birthday day : '))
                import datetime
                try:
                    d = datetime.date(newy, newm, newd)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE student SET  dtb_s = '{d}' WHERE code_s = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_student()

            elif ans == '4':
                try:
                    newp = input('new phone number : ')
                    cur.execute(f"UPDATE student SET  phone_number_s = '{newp}' WHERE code_s = {code}")
                    con.commit()
                    print("changing was succesfully")
                    back_up_student()
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    newp = "..."

        n = input(" do you want to enter your code to change another student info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def delete_student():
    while True:
        code = int(input('enter the student code witch you want to delete : '))

        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_s FROM student WHERE code_s = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM student WHERE code_s ={code}")
            print("deleting was succesfully    ")
            back_up_student()
            con.commit()
        n = input(" do you want to enter another code ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_table_fanni():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE fanni(
                    name_f nvarchar(20) not null ,
                    last_name_f nvarchar(20) not null,
                    code_f int not null  PRIMARY KEY ,
                    dtb_f date,
                    phone_number_f nvarchar(11) not null,
                    madrak_f nvarchar(20) not null,
                    shift_f nvarchar(20) not null,
                    skill_f nvarchar(20) not null,
                    bimeh_f nvarchar(10) not null, 
                    sabeqe_f  int not null,
                    checks_f int not null,
                    zamen_f nvarchar(20) not null
                   
    
    )    
    ''')
        print('creating table fanni...')
        print(" fanni table created ")
    except Exception:
        print("fanni table already existed")


def insert_record_table_fanni():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_f FROM fanni')
            lst = cur.fetchall()
            try:
                x = int(input('enter the fanni id  : '))
            except ValueError:
                print('error')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False :
                na = input('enter the fanni name : ')
                if len(na) == 0:
                    na = '... '
                last_name = input("enter the fanni last name: ")
                if len(last_name) == 0:
                    last_name = '... '
                try:
                    phone_number = input("enter the fanni phone number :")
                    if len(phone_number) == 0:
                        phone_number = '... '
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    phone_number = "..."
                madrak = input("enter the fanni sertificate : ")
                if len(madrak) == 0:
                    madrak = '... '
                shift = input("enter the fanni shift: ")
                if len(shift) == 0:
                    shift = '... '
                y = int(input('birthday year : '))
                m = int(input('birthday mounth : '))
                d = int(input('birthday day : '))
                import datetime
                try:
                    d = datetime.date(y, m, d)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                print(d)
                skill = input("enter the fanni skill : ")
                if len(skill) == 0:
                    skill = '... '
                bimeh = input("dose fanni have insurance : ")
                if len(bimeh) == 0:
                    bimeh = '... '
                sabeqe = input(" exprience : ")
                if len(sabeqe) == 0:
                    sabeqe = '... '
                checks = input("how many checks dose fanni have : ")
                if len(checks) == 0:
                    checks = '... '
                zamen = input("zamne : ")
                if len(zamen) == 0:
                    zamen = '... '
                sql = 'INSERT INTO fanni (code_f, name_f, last_name_f, phone_number_f, madrak_f, skill_f, bimeh_f, sabeqe_f, shift_f, checks_f, zamen_f, dtb_f) VALUES (%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s)'
                val = (x, na, last_name, phone_number, madrak, skill, bimeh, sabeqe, shift, checks, zamen, d)
                cur.execute(sql, val)
                con.commit()
                print(' add fanni ...')
                back_up_fanni()
                break
            else:
                print('fanni code has existed ...')
        n = input(" do you want to enter your code to add another fanni info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def change_fanni():
    while True:
        code = int(input('code for search to change the information: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_f FROM fanni WHERE code_f = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f'SELECT * FROM fanni WHERE code_f = {code}')
            print(cur.fetchone())
            print("warning!! you cant change the fanni id !!")
            print('\t 1 - change name ')
            print('\t 2 - change last name ')
            print('\t 3 - change date  ')
            print('\t 4 - change phone number  ')
            print('\t 5 - change sertificate  ')
            print('\t 6 - change shifts  ')
            print('\t 7 - change bimeh  ')
            print('\t 8 - change exprience  ')
            print('\t 9 - change checks  ')
            print('\t 10 - change zamen  ')
            print('\t 11 - change skill  ')
            ans = input('enterd the number of your choice : ')
            if ans == '1':
                newname = input('new name : ')
                cur.execute(f"UPDATE fanni SET  name_f = '{newname}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()
            elif ans == '2':
                newlastname = input('new last name : ')
                cur.execute(f"UPDATE fanni SET  last_name_f = '{newlastname}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '3':
                newy = int(input('new birthday year : '))
                newm = int(input('new birthday mounth : '))
                newd = int(input('new birthday day : '))
                import datetime
                try:
                    d = datetime.date(newy, newm, newd)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE fanni SET  dtb_f = '{d}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '4':
                try:
                    newp = input('new phone number : ')
                    cur.execute(f"UPDATE fanni SET  phone_number_f = '{newp}' WHERE code_f = {code}")
                    con.commit()
                    print("changing was succesfully")
                    back_up_fanni()
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    newp ="..."

            elif ans == '5':
                newosertificate = input('new teacher name : ')
                cur.execute(f"UPDATE fanni SET  madrak_f = '{newosertificate}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '6':
                newshifts = input('new shifts : ')
                cur.execute(f"UPDATE fanni SET shift_f  = '{newshifts}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '7':
                newsbimeh = input('new bimeh info : ')
                cur.execute(f"UPDATE fanni SET bimeh_f  = '{newsbimeh}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '8':
                newexprience = input('new exprience info : ')
                cur.execute(f"UPDATE fanni SET sabeqe_f  = '{newexprience}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '9':
                newcheck = input('new checks info : ')
                cur.execute(f"UPDATE fanni SET checks_f  = '{newcheck}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '10':
                newzamen = input('new zamen info : ')
                cur.execute(f"UPDATE fanni SET zamen_f  = '{newzamen}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()

            elif ans == '11':
                newskill = input('new skill info : ')
                cur.execute(f"UPDATE fanni SET skill_f  = '{newskill}' WHERE code_f = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_fanni()
        n = input(" do you want to enter your code to change another fanni info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def query_code_fanni():
    while True:
        code = int(input('enter the fanni code witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM fanni  WHERE code_f ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have fanni with your entered code')
        else:
            print(lst)
        n = input(" do you want to enter your code to search another fanni info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def delete_fanni():
    while True:
        code = int(input('enter the fanni code witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_f FROM fanni WHERE code_f = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM fanni WHERE code_f ={code}")
            print("deleting was succesfully    ")
            con.commit()
            back_up_fanni()
        n = input(" do you want to enter another code ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_table_sale():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE sale(
                    name_b nvarchar(20) not null ,
                    last_name_b nvarchar(20) not null,
                    code_b int not null  PRIMARY KEY ,
                    dtb_b date,
                    phone_number_b nvarchar(11) not null,
                    madrak_b nvarchar(20) not null,
                    shift_b nvarchar(20) not null,
                    percent_b int not null,
                    bimeh_b nvarchar(10) not null, 
                    sabeqe_b  int not null,
                    checks_b int not null,
                    zamen_b nvarchar(20) not null


    )    
    ''')
        print('creating table sale...')
        print(" sale table created ")
    except Exception:
        print("sale table already existed")


def insert_record_table_sale():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_b FROM sale')
            lst = cur.fetchall()
            try:
                x = int(input('enter the saler id  : '))
            except ValueError:
                print('error')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True

            if b == False :
                na = input('enter the saler name : ')
                if len(na) == 0:
                    na = '... '
                last_name = input("enter the saler last name: ")
                if len(last_name) == 0:
                    last_name = '... '
                try:
                    phone_number = input("enter the saler phone number :")
                    if len(phone_number) == 0:
                        phone_number = '... '
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    phone_number = "..."

                madrak = input("enter the saler sertificate : ")
                if len(madrak) == 0:
                    madrak = '... '

                shift = input("enter the saler shift: ")
                if len(shift) == 0:
                    shift = '... '

                y = int(input('birthday year : '))
                m = int(input('birthday mounth : '))
                d = int(input('birthday day : '))
                import datetime
                try:
                    d = datetime.date(y, m, d)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                print(d)

                darsad = input("enter the saler percent : ")
                if len(darsad) == 0:
                    darsad = '... '

                bimeh = input("dose saler have insurance : ")
                if len(bimeh) == 0:
                    bimeh = '... '

                sabeqe = input(" exprience : ")
                if len(sabeqe) == 0:
                    sabeqe = '... '
                checks = input("how many checks dose saler have : ")
                if len(checks) == 0:
                    checks = '... '

                zamen = input("zamne : ")
                if len(zamen) == 0:
                    zamen = '... '

                sql = 'INSERT INTO sale (code_b, name_b, last_name_b, phone_number_b, madrak_b, percent_b, bimeh_b, sabeqe_b, shift_b, checks_b, zamen_b, dtb_b) VALUES (%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s)'
                val = (x, na, last_name, phone_number, madrak, darsad, bimeh, sabeqe, shift, checks, zamen, d)
                cur.execute(sql, val)
                con.commit()
                print(' add saler ...')
                back_up_sale()
                break
            else:
                print('saler code has existed ...')
        n = input(" do you want to enter your code to add another saler info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def change_saler():
    while True:
        code = int(input('code for search to change the information: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_b FROM sale WHERE code_b = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f'SELECT * FROM sale WHERE code_b = {code}')
            print(cur.fetchone())
            print("warning!! you cant change the saler id !!")
            print('\t 1 - change name ')
            print('\t 2 - change last name ')
            print('\t 3 - change date  ')
            print('\t 4 - change phone number  ')
            print('\t 5 - change sertificate  ')
            print('\t 6 - change shifts  ')
            print('\t 7 - change bimeh  ')
            print('\t 8 - change exprience  ')
            print('\t 9 - change checks  ')
            print('\t 10 - change zamen  ')
            print('\t 11 - change percent')
            ans = input('enterd the number of your choice : ')
            if ans == '1':
                newname = input('new name : ')
                cur.execute(f"UPDATE sale SET  name_b = '{newname}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()
            elif ans == '2':
                newlastname = input('new last name : ')
                cur.execute(f"UPDATE sale SET  last_name_b = '{newlastname}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()
            elif ans == '3':
                newy = int(input('new birthday year : '))
                newm = int(input('new birthday mounth : '))
                newd = int(input('new birthday day : '))
                import datetime
                try:
                    d = datetime.date(newy, newm, newd)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE sale SET  dtb_b = '{d}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '4':
                try:
                    newp = input('new phone number : ')
                    cur.execute(f"UPDATE sale SET  phone_number_b = '{newp}' WHERE code_b = {code}")
                    con.commit()
                    print("changing was succesfully")
                    back_up_sale()
                except Exception:
                    print("sorry, phone number should be 11 digit")
                    newp ="..."

            elif ans == '5':
                newosertificate = input('new sertificate name : ')
                cur.execute(f"UPDATE sale SET  madrak_b = '{newosertificate}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '6':
                newshifts = input('new shifts : ')
                cur.execute(f"UPDATE sale SET shift_b  = '{newshifts}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '7':
                newsbimeh = input('new bimeh info : ')
                cur.execute(f"UPDATE sale SET bimeh_b  = '{newsbimeh}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '8':
                newexprience = input('new exprience info : ')
                cur.execute(f"UPDATE sale SET sabeqe_b  = '{newexprience}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '9':
                newcheck = input('new checks info : ')
                cur.execute(f"UPDATE sale SET checks_b  = '{newcheck}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()

            elif ans == '10':
                newzamen = input('new zamen info : ')
                cur.execute(f"UPDATE sale SET zamen_b  = '{newzamen}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()
            elif ans == '11':
                newpercent = input('new percent info : ')
                cur.execute(f"UPDATE sale SET percent_b  = '{newpercent}' WHERE code_b = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_sale()
        n = input(" do you want to enter your code to change another saler info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def query_code_saler():
    while True:
        code = int(input('enter the saler code witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM sale  WHERE code_b ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have saler with your entered code')
        else:
            print(lst)
        n = input(" do you want to enter your code to search another saler info? (yes / no)")
        if n == "no":
            print("ok!")
            break

def delete_sale():
    while True:
        code = int(input('enter the saler code witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_b FROM sale WHERE code_b = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM sale WHERE code_b ={code}")
            print("deleting was succesfully    ")
            back_up_sale()
            con.commit()
        n = input(" do you want to enter your code to delete another saler info? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_table_classes():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE classes(
                    number_c int not null PRIMARY KEY ,
                    zarfiat_c int not null,
                    system_c int not null  ,
                    tabaqe_c int not null


    )    
    ''')
        print('creating table classes...')
        print("classes table created ")
    except Exception:
        print("classes table already existed")


def insert_record_table_classes():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT number_c FROM classes')
            lst = cur.fetchall()
            try:
                x = int(input('enter the classes number : '))
            except ValueError:
                print('you should enter the code num in digit ')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:
                z = input('enter the classes capacity: ')
                if len(z) == 0:
                    z = '...'
                system = input("how many systems dose thus class have : ")
                if len(system) == 0:
                    system = '... '
                tabaqe = input("calss floor :")
                if len(tabaqe) == 0:
                    tabaqe = '...'

                sql = 'INSERT INTO classes (number_c, zarfiat_c, system_c, tabaqe_c) VALUES (%s, %s, %s, %s)'

                val = (x, z, system, tabaqe)
                cur.execute(sql, val)
                con.commit()
                print(' add classes ...')
                back_up_classes()
                break
            else:
                print('class number exits ...')
        n = input(" do you want to enter another code to add another class? (yes / no)")
        if n == "no":
            print("ok!")
            break

def query_code_classes():
    while True:
        code = int(input('enter the class number witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM classes  WHERE number_c ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have class with your entered number')
        else:
            print(lst)
        n = input(" do you want to enter another code to search another class? (yes / no)")
        if n == "no":
            print("ok!")
            break

def change_classes():
    while True:
        code = int(input('number for search: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT number_c FROM classes WHERE number_c = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found number !')
        else:
            cur.execute(f'SELECT * FROM classes WHERE number_c = {code}')
            print(cur.fetchone())
            print("warning!! you cant change class number and floor !!")
            print('\t 1 - change capacity ')
            print('\t 2 - change class system ')

            ans = input('enterd the number of your choice : ')
            if ans == '1':
                newcapacity = input('new capacity : ')
                cur.execute(f"UPDATE classes SET  zarfiat_c = '{newcapacity}' WHERE number_c = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_classes()
            elif ans == '2':
                newsystem = input('new system number : ')
                cur.execute(f"UPDATE classes SET  system_c = '{newsystem}' WHERE number_c = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_classes()
        n = input(" do you want to enter another code to change another class? (yes / no)")
        if n == "no":
            print("ok!")
            break

def delete_clases():
    while True:
        code = int(input('enter the  classes number witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT number_c FROM classes WHERE number_c  = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM classes WHERE number_c ={code}")
            print("deleting was succesfully ")
            back_up_classes()
            con.commit()
        n = input(" do you want to enter another cod? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_table_lessons():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE lessons(
                    code_l int not null PRIMARY KEY ,
                    name_l nvarchar(20) not null,
                    saat_l int not null,
                    type_l  nvarchar(20) not null  

    )    
    ''')
        print('creating lesson table ...')
        print("lesson table created ")

    except Exception:
        print("lesson table already existed")


def query_code_lesson():
    while True:
        code = int(input('enter the lesson code witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM lessons  WHERE code_l ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have any lesson with your entered number')
        else:
            print(lst)
        n = input(" do you want to enter another code to search another one ? (yes / no)")
        if n == "no":
            print("ok!")
            break

def insert_record_table_lessons():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_l FROM lessons')
            lst = cur.fetchall()
            try:
                x = int(input('enter the lesson code : '))
            except ValueError:
                print('you should enter the digit for code')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b== False:
                na = input("enter the lesson name :")
                if len(na) == 0:
                    na ="..."
                h = input('enter the lesson hour : ')
                if len(h) == 0:
                    h = '...'
                type = input("enter the class type : ")
                if len(type) == 0:
                    type = '... '

                sql = 'INSERT INTO lessons  (code_l, name_l,  saat_l, type_l) VALUES (%s, %s, %s, %s)'

                val = (x, na, h , type)
                cur.execute(sql, val)
                con.commit()
                print(' add lessons ...')
                back_up_lessons()
                break
            else:
                print('lesson code exits ...')
        n = input(" do you want to enter another cod to add new lesson ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def change_lesson():
    while True:
        code = int(input('enter the lesson code : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_l FROM lessons WHERE code_l = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found number !')
        else:
            cur.execute(f'SELECT * FROM lessons WHERE code_l = {code}')
            print(cur.fetchone())
            print("warning!! you cant change lesson number code!!")
            print('\t 1 - change lesson name ')
            print('\t 2 - change lesson hour ')

            ans = input('enter the number of your choice : ')
            if ans == '1':
                newname = input('new name for this code : ')
                cur.execute(f"UPDATE lessons SET  name_l = '{newname}' WHERE code_l = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_lessons()
            elif ans == '2':
                newhour = input('new hour : ')
                cur.execute(f"UPDATE lessons SET  saat_l = '{newhour}' WHERE code_l = {code}")
                con.commit()
                print("changing was succesfully")
                back_up_lessons()
        n = input(" do you want to enter another cod for changing ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def delete_lesson():
    while True:
        code = int(input('enter the  lesson code witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_l FROM lessons WHERE code_l = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM lessons WHERE code_l ={code}")
            print("deleting was succesfully ")
            con.commit()
        n = input(" do you want to enter another cod? (yes / no)")
        if n == "no":
            print("ok!")
            break


def create_taghvim_a():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
                   CREATE TABLE taghvim_amozeshi(
                           code_e int not null  PRIMARY KEY ,
                           start_day date,
                           final_day date,
                           course_hour_s int not null,
                           course_hour_e int not null,
                           all_capacity int not null,
                           code_t int not null , 
                           code_l int not null,
                           
                           FOREIGN Key (code_t) REFERENCES teacher(code_t),
                           FOREIGN Key (code_l) REFERENCES lessons(code_l)
                           
                          
                           
                           
    )                        
    ''')
        print('create table taghvim amozeshi')

    except Exception:
        print("taqvim amozeshi table already exists")




def insert_taghvim():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_e FROM taghvim_amozeshi')
            lst = cur.fetchall()
            try:
                x = int(input('enter the code erae : '))
            except ValueError:
                print('you should enter the digit for code')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:
                y = int(input('course year to start : '))
                m = int(input('course mounth to start : '))
                d = int(input('course day to start : '))
                import datetime

                try:
                    d = datetime.date(y, m, d)
                except ValueError:
                    d = datetime.date(1900, 1, 1)
                print(d)
                y1 = int(input('course year to end : '))
                m1 = int(input('course mounth to end : '))
                d1 = int(input('course day to end : '))
                import datetime

                try:
                    e = datetime.date(y1, m1, d1)
                except ValueError:
                   e = datetime.date(1900, 1, 1)
                print(e)


                all_z = input("enter the course capacity : ")
                if len(all_z) == 0:
                    all_z = '... '


                try:
                    t_code = input("enter the teacher code : ")
                except Exception:
                    print("we dont have any teacher with your enterd code!!!")
                    t_code = '...'

                try:
                    l_code = input("enter the lesson code : ")
                except Exception:
                    print("we dont have any lesson with your enterd code!!!")
                    l_code = '... '

                course_s = input("enter the hour that course get start : ")
                if len(course_s) == 0:
                    course_s = '... '
                course_e = input("enter the hour that course get end : ")
                if len(course_s) == 0:
                    course_s = '... '


                sql = 'INSERT INTO taghvim_amozeshi (code_e, start_day, final_day, course_hour_s, course_hour_e, all_capacity, code_t, code_l) VALUES ( %s, %s, %s, %s,  %s, %s ,%s,%s)'

                val = (x, d, e, course_s, course_e, all_z, t_code, l_code,)
                cur.execute(sql, val)
                con.commit()
                print(' add course ...')
                break
            else:
                print('course code exits ...')
        n = input(" do you want to enter another cod to add new course ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def change_course():
    while True:
        code = int(input('enter the course code witch you want to change its information : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_e FROM taghvim_amozeshi WHERE code_e = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found number !')
        else:
            cur.execute(f'SELECT * FROM taghvim_amozeshi WHERE code_e = {code}')
            print(cur.fetchone())
            print("warning!! you cant change lesson, teachers, and course code !!")
            print('\t 1 - change start_day ')
            print('\t 2 - change final_day ')
            print('\t 3 - change course_hour_s ')
            print('\t 4 - change course_hour_e ')
            print('\t 5 _  change capacity')

            ans = input('enter the number of your choice : ')
            if ans == '1':
                newy = int(input('new year : '))
                newm = int(input('new mounth : '))
                newd = int(input('new  day : '))
                import datetime
                try:
                    q = datetime.date(newy, newm, newd)
                except ValueError:
                    q = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE taghvim_amozeshi SET  start_day = '{q}' WHERE code_e = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '2':
                newy = int(input('new year : '))
                newm = int(input('new mounth : '))
                newd = int(input('new  day : '))
                import datetime
                try:
                    t = datetime.date(newy, newm, newd)
                except ValueError:
                    t = datetime.date(1900, 1, 1)
                cur.execute(f"UPDATE taghvim_amozeshi SET  final_day = '{t}' WHERE code_e = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '3':
                news = input('new hour to start the class : ')
                cur.execute(f"UPDATE taghvim_amozeshi SET  course_hour_s = '{news}' WHERE code_e = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '4':
                newe = input('new hour to start the class : ')
                cur.execute(f"UPDATE taghvim_amozeshi SET  course_hour_e = '{newe}' WHERE code_e = {code}")
                con.commit()
                print("changing was succesfully")
            elif ans == '5':
                capacity = input('new capacity for this course : ')
                cur.execute(f"UPDATE taghvim_amozeshi SET  all_capacity = '{capacity}' WHERE code_e = {code}")
                con.commit()
                print("changing was succesfully")
        n = input(" do you want to enter another cod for changing ? (yes / no)")
        if n == "no":
            print("ok!")
            break

def query_taghvim_amozeshi():
    while True:
        code = int(input('enter the course number witch you want to query: '))
        con = connect_db_amozeshgah()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM taghvim_amozeshi  WHERE code_e ={code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('we dont have course with your entered number')
        else:
            print(lst)
        n = input(" do you want to enter another code to search another course? (yes / no)")
        if n == "no":
            print("ok!")
            break


def delete_taghvim_amozeshi():
    while True:
        code = int(input('enter the  course code witch you want to delete : '))
        con = connect_db_amozeshgah()
        cur = con.cursor()
        cur.execute(f'SELECT code_e FROM taghvim_amozeshi WHERE code_e = {code}')
        lst = cur.fetchall()
        if len(lst) == 0:
            print('not found code !')
        else:
            cur.execute(f"DELETE FROM taghvim_amozeshi WHERE code_e ={code}")
            print("deleting was succesfully ")
            con.commit()
        n = input(" do you want to enter another course ? (yes / no)")
        if n == "no":
            print("ok!")
            break

def report_teacher_zoj():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.class_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                WHERE teacher.class_t LIKE 'z%' ")
    print("teachers who have class in zoj days are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)


def report_teacher_fard():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.class_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                 WHERE teacher.class_t LIKE 'f%' ")

    lst = cur.fetchall()
    print("teachers who have class in fard days are :")
    for i in lst:
        print(i)


def report_teacher_python():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                WHERE teacher.lesson_t LIKE 'p%' ")
    print("teachers who have python class are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_teacher_java():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                WHERE teacher.lesson_t LIKE 'j%' ")
    print("teachers who have java class are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_teacher_web():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                WHERE teacher.lesson_t LIKE 'w%' ")
    print("teachers who have web class are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_lesson_python():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                WHERE lessons.name_l LIKE 'p%' ")
    print("python classes are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)


def report_lesson_java():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                WHERE lessons.name_l LIKE 'j%' ")
    print("java classes are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_lesson_web():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                WHERE lessons.name_l LIKE 'w%' ")
    print("web classes are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)
def report_lesson_online():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                WHERE lessons.type_l LIKE 'o%' ")
    print("online classes are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_lesson_inperson():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                WHERE lessons.type_l LIKE 'i%' ")
    print("inperson classes are :")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_teacher_reporter():
    ans = input(" enter the teacher code who you want to see its report :")
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute(f"SELECT\
                teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                 WHERE teacher.code_t = '{ans}' ")
    print("your request: ")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_teacher_null():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute("SELECT\
                teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM teacher\
                 LEFT JOIN taghvim_amozeshi on teacher.code_t = taghvim_amozeshi.code_t\
                WHERE code_e  is null ")
    print("these teachers have no course: ")
    lst = cur.fetchall()
    for i in lst:
        print(i)

def report_lesson_reporter():
    ans = input(" enter the teacher code who you want to see its report :")
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute(f"SELECT\
                lessons.code_l, lessons.name_l, lessons.saat_l, lessons.type_l,\
                 taghvim_amozeshi.code_e,taghvim_amozeshi.code_t, taghvim_amozeshi.start_day,taghvim_amozeshi.course_hour_s,\
                 taghvim_amozeshi.course_hour_e,taghvim_amozeshi.all_capacity,\
                  taghvim_amozeshi.final_day  FROM lessons\
                 RIGHT JOIN  taghvim_amozeshi on lessons.code_l = taghvim_amozeshi.code_l\
                 WHERE lessons.code_l = '{ans}' ")
    print("yur request is :")
    lst = cur.fetchall()
    for i in lst:
        print(i)


def create_entekhab_vahed():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
                       CREATE TABLE entekhab_vahed(
                               code_entekhab int not null PRIMARY KEY ,
                               code_e int not null ,
                               code_s int not null ,
                               number_c int not null ,
                               code_l int not null ,
                               code_t  int not null, 
                               student_name nvarchar(10),
                               vaziat_pardakht nvarchar(20),
                               FOREIGN Key (code_t) REFERENCES teacher(code_t),
                               FOREIGN Key (code_l) REFERENCES lessons(code_l),
                               FOREIGN Key (code_e) REFERENCES taghvim_amozeshi (code_e),
                               FOREIGN Key (number_c) REFERENCES classes(number_c),
                               FOREIGN Key (code_s) REFERENCES student(code_s)


        )                        
        ''')
        print('create table entekhab_vahed')
    except Exception:
        print("entekhab_vahed table already exists")

def insert_entekhab_vahed():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT code_entekhab FROM entekhab_vahed')
            lst = cur.fetchall()
            try:
                x = int(input('code entekhab vahed ra vared konid : '))
            except ValueError:
                print('you should enter the digit for code')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:

                try:
                    e = input("code erae dars ra vared konid : ")
                except Exception:
                    print("we dont have any course with your enterd code!!!")
                    e = '...'

                try:
                    t_code = input("enter the teacher code : ")
                except Exception:
                    print("we dont have any teacher with your enterd code!!!")
                    t_code = '...'

                try:
                    l_code = input("enter the lesson code : ")
                except Exception:
                    print("we dont have any lesson with your enterd code!!!")
                    l_code = '... '

                try:
                    s_code = input("enter the student code : ")
                except Exception:
                    print("we dont have any student with your enterd code!!!")
                    s_code = '...'

                try:
                    code_c = input("enter the class code : ")
                except Exception:
                    print("we dont have any class with your entered code!!!")
                    code_c = '...'

                v = input("payment status : ")
                student_name = input(" student name = ")



                sql = 'INSERT INTO entekhab_vahed (code_entekhab, code_e, code_s, number_c,code_l, code_t, student_name,vaziat_pardakht) VALUES (%s, %s, %s, %s, %s,  %s, %s,%s)'

                val = (x, e, s_code, code_c, l_code,t_code, student_name,v)
                cur.execute(sql, val)
                con.commit()
                print(' add information ...')
                break
            else:
                print('entekhab vahed code exits ...')
        n = input(" do you want to enter another cod to add new information ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def report_entekhab_vahed():
    ans = input("enter your code to see your student : ")
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute(f"SELECT\
                    teacher.code_t, teacher.last_name_t, teacher.lesson_t,\
                     entekhab_vahed.code_e,entekhab_vahed.code_t,\
                     entekhab_vahed.code_l,entekhab_vahed.code_s,entekhab_vahed.student_name,\
                     entekhab_vahed.code_entekhab  FROM teacher\
                     LEFT JOIN entekhab_vahed on teacher.code_t = entekhab_vahed.code_t\
                     WHERE teacher.code_t = '{ans}'")
    print("your request: ")
    lst = cur.fetchall()
    for i in lst:
        print(i)


def create_zarfiat():
    con = connect_db_amozeshgah()
    cur = con.cursor()
    try:
        cur.execute('''
                       CREATE TABLE zarfiat(
                                
                               lesson_num int,
                               lesson_name nvarchar(20),
                               zarfiat_kol int not null ,
                               zarfiat_por_shode int not null ,
                               zarfiat_khali int not null 
        )                        
        ''')
        print('create table zarfiat')
    except Exception:
        print("zarfiat table already exists")


def insert_zarfiat():
    while True:
        con = connect_db_amozeshgah()
        cur = con.cursor()
        while True:
            cur.execute('SELECT lesson_num FROM zarfiat')
            lst = cur.fetchall()
            x = input('enter the lesson number : ')
            b = False
            for i in lst:
                if i[0] == x:
                    b = True
            if b == False:

                n = input("lesson name: ")


                try:
                    k = int(input("zarfiat kol : "))
                except Exception:
                    print("you should enter digit!!")
                    k = '...'

                try:
                    p = int(input("zarfiat por shode : "))
                except Exception:
                    print("you should enter digit!!!")
                    p = '...'

                try:
                    kh =int(input("zarfiat baghi mande: "))
                except Exception:
                    print("we dont have any lesson with your enterd code!!!")
                    kh = '... '

                sql = 'INSERT INTO zarfiat (lesson_num, lesson_name, zarfiat_kol, zarfiat_por_shode, zarfiat_khali) VALUES (%s,%s, %s, %s, %s)'

                val = (x, n, k, p, kh)
                cur.execute(sql, val)
                con.commit()
                print(' add information ...')
                break
            else:
                print('lesson name code exits ...')
        n = input(" do you want to enter another cod to add new information ? (yes / no)")
        if n == "no":
            print("ok!")
            break


def change_zarfait():
    p=0
    j=0
    w=0
    print(lesson_name)
    name = input('adad dars entekhab shode ra vared konid: ')
    con = connect_db_amozeshgah()
    cur = con.cursor()
    cur.execute(f'SELECT lesson_num FROM zarfiat WHERE lesson_num = {name}')
    lst = cur.fetchall()
    if len(lst) == 0:
        print('not found the lesson !')
    else:
        if name == "1":
            p+=1
            if p ==50:
                print('zarfiat in dars por shode')
            else:

                por_shode = p
                baqi_mande = 50-p

                cur.execute(f"UPDATE zarfiat SET  zarfiat_por_shode = {por_shode} WHERE lesson_num = {name}")
                con.commit()
                cur.execute(f"UPDATE zarfiat SET  zarfiat_khali = {baqi_mande} WHERE lesson_num = {name}")
                con.commit()
                print("changing was succesfully")
        elif name == '2':
            w += 1
            if w == 60:
                print('zarfiat in dars por shode')
            else:


                por_shode = w
                baqi_mande = 60 - w

                cur.execute(f"UPDATE zarfiat SET  zarfiat_por_shode = '{por_shode}' WHERE lesson_num = {name}")
                con.commit()
                cur.execute(f"UPDATE zarfiat SET  zarfiat_khali = '{baqi_mande}' WHERE lesson_num = {name}")
                con.commit()
                print("DONE")
        elif name == '3':
            j += 1
            if j == 55:
                print('DONE')
            else:

                por_shode = j
                baqi_mande = 55 - j

                cur.execute(f"UPDATE zarfiat SET  zarfiat_por_shode = '{por_shode}' WHERE lesson_num = {name}")
                con.commit()
                cur.execute(f"UPDATE zarfiat SET  zarfiat_khali = '{baqi_mande}' WHERE lesson_num = {name}")
                con.commit()
                print("DONE")


if __name__ == "__main__":
    print(" its module not the main program")
    #insert_zarfiat()
    #create_zarfiat()

     #change_zarfait()
     #change_zarfait()
     # create_database()
     #
     # connect_db_amozeshgah()
     # try:
     #     create_table_teacher()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_table_student()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_table_fanni()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_table_sale()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_table_classes()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_table_lessons()
     # except Exception as x:
     #     print(x)
     # try:
     #     create_taghvim_a()
     # except Exception as x:
     #     print(x)
     # connect_db_amozeshgah()
     # try:
     #     create_entekhab_vahed()
     # except Exception as x:
     #     print(x)
     #
     # try:
     #     create_zarfiat()
     # except Exception as x:
     #     print(x)
     #report_teacher_zoj()
     #report_teacher_fard()
     #report_teacher_python()
     #report_teacher_web()
     #report_teacher_java()
     #report_lesson_python()
     #report_lesson_web()
     #report_lesson_java()
     #report_lesson_online()
     #report_lesson_inperson()
     #report_teacher_reporter()
     #report_teacher_null()
     #report_entekhab_vahed()
     #insert_record_table_classes()
     #insert_record_table_fanni()
     #insert_record_table_student()
     #insert_record_table_sale()
     #insert_record_table_lessons()
     #insert_record_table_teacher()
     #insert_taghvim()
     #insert_entekhab_vahed()
     #query_code_lesson()
     #query_code_student()
     #change_student()
     #change_teacher()
     #change_fanni()
     #change_saler()
     #change_classes()
     #change_lesson()
     #change_course()
     #delete_lesson()
     #delete_sale()
     #delete_student()
     #delete_fanni()
     #delete_taghvim_amozeshi()
     #delete_teacher()
     #delete_lesson()
     #delete_clases()
     #query_code_classes()
     #query_code_teacher()
     #query_code_lesson()
     #change_teacher()
     #insert_record_table_teacher()
     #insert_taghvim()
     #delete_table_teacher()
     #insert_record_table_teacher()
     #list_column()
     #dele()
