#############################################################################################################################
###CONNECTION WITH LOCAL SERVER###
from flask import Flask,render_template,request,session
from sqlalchemy import create_engine
app = Flask(__name__)
import time
import psycopg2
import random
#conn = psycopg2.connect(database = 'mydb',user = 'postgres',password = '********',port = '5432',host = '127.0.0.1')===========using only psycopg2
#cur = conn.cursor()
db_string = 'postgresql+psycopg2://postgres:password@localhost:5432/mydb'
db = create_engine(db_string)
conn = db.connect()


######################################################################################################################################################################################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/netbanking1')
def deposit():
    return render_template('transact.html',msg = 'Amount to Deposit',link = 'deposit1')

@app.route('/netbanking2')
def debit():
    return render_template('transact.html',msg = 'Amount to Withdraw',link = 'withdraw1')

@app.route('/netbanking3')
def transfer():
    return render_template('transfer.html')

@app.route('/netbanking4')
def delete():
    return render_template('delete.html')

@app.route('/netbanking5')
def review():
    return render_template('review.html')



@app.route('/createnew',methods=['POST','GET'])
def create1():

    name1 = request.form.get("name")
    #acc_no1 = request.form.get("acc_no")
    acc_no1 = random.randint(1000000000000,9999999999999)
    ph_no1 = request.form.get("ph_no")
    address1 = request.form.get("address")
    email1 = request.form.get("email")
    id1 = request.form.get("pin")
    bal = request.form.get("balance")
    conn.execute("INSERT INTO ACCOUNTS (ID,ADDRESS,BALANCE,ACC_NO,NAME,PH_NO,EMAIL) \
      VALUES (%s,%s,%s,%s,%s,%s,%s)", (id1,address1,bal,acc_no1,name1,ph_no1,email1));
    #conn.commit()
    #print('Account created successfully')
    #print('Account Number = ',acc_no1)
    #print('Please Note your Account Number it will disappear after 5 Seconds')
    #time.sleep(5)
    return render_template('success.html',name=name1,acno=acc_no1,message = "Created")


@app.route('/deposit1',methods=['POST','GET'])
def deposit1():
    temp_accno = request.form.get("acc_no")
    temp_pass = request.form.get("pin")
    temp_amt = int(request.form.get("balance"))
    info = conn.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
               FROM accounts
               WHERE id = %s and acc_no = %s''',
            (str(temp_pass), str(temp_accno))).fetchall()
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    #new_trans.credit(temp_amt,temp_accno)
    temp_amt += info[0][6]
    conn.execute(
        "UPDATE accounts set balance = %s where acc_no = %s",(temp_amt,temp_accno)
        )
    bal = conn.execute(
        "select balance from accounts where acc_no = %s",(temp_accno)
        ).fetchone()
    return render_template('show.html',bal=bal[0],acc_no = temp_accno,msg = 'Credited')

@app.route('/withdraw',methods=['POST','GET'])
def withdraw1():
    temp_accno = request.form.get("acc_no")
    temp_pass = request.form.get("pin")
    temp_amt = int(request.form.get("balance"))
    info = conn.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
               FROM accounts
               WHERE id = %s and acc_no = %s''',
            (str(temp_pass), str(temp_accno))).fetchone()
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    #new_trans.credit(temp_amt,temp_accno)
    bala = info[6]
    if (temp_amt > bala):
        return render_template('error.html',message = 'Insufficient Balance')
    else:
        bala = bala - temp_amt
        conn.execute(
            "UPDATE accounts set balance = %s where acc_no = %s",(bala,temp_accno)
            )
        bal = conn.execute(
            "select balance from accounts where acc_no = %s",(temp_accno)
            ).fetchone()
        return render_template('show.html',bal=bal[0],acc_no = temp_accno,msg = 'Debited')

@app.route('/nb1',methods=['POST','GET'])
def transfer1():
    temp_accno = request.form.get("acc_no")
    temp_pass = request.form.get("pin")
    temp_amt = int(request.form.get("balance"))
    ntemp_accno = request.form.get("tacc_no")
    info = conn.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
               FROM accounts
               WHERE id = %s and acc_no = %s''',
            (str(temp_pass), str(temp_accno))).fetchone()
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    #new_trans.credit(temp_amt,temp_accno)
    bala = info[6]
    if (temp_amt > bala):
        return render_template('error.html',message = 'Insufficient Balance')
    else:
        bala = bala - temp_amt
        conn.execute(
            "UPDATE accounts set balance = %s where acc_no = %s",(bala,temp_accno)
            )
        bal = conn.execute(
            "select balance from accounts where acc_no = %s",(temp_accno)
            ).fetchone()


        info1 = conn.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
                   FROM accounts
                   WHERE acc_no = %s''',
                str(ntemp_accno)).fetchone()
        #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
        #new_trans.credit(temp_amt,temp_accno)
        temp_amt += info[6]
        conn.execute(
            "UPDATE accounts set balance = %s where acc_no = %s",(temp_amt,temp_accno)
            )
        return render_template('show.html',bal=bal[0],acc_no = temp_accno,msg = 'Debited')

@app.route('/nbr',methods=['POST','GET'])
def review1():
    temp_accno = request.form.get("acc_no")
    temp_pass = request.form.get("pin")
    info = conn.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
               FROM accounts
               WHERE id = %s and acc_no = %s''',
            (str(temp_pass), str(temp_accno))).fetchone()
    return render_template('view.html',info=info)


@app.route('/delete',methods=['POST','GET'])
def delete1():
    delt = True
    while(delt):
        temp_accno = request.form.get("acc_no")
        temp_pass = request.form.get("pin")
        conn.execute('''DELETE FROM accounts
                   WHERE id = %s and acc_no = %s''',
                (str(temp_pass), str(temp_accno)));
        return render_template('success.html',message = 'Deleted')







#@app.route('/more')
#def more():
#    return render_template('more.html')
#@app.route('/hello',methods=['GET','POST'])
#def hello():
    #if request.method =='GET':
        #return 'please submit the form instead'
    #else:
        #name = request.form.get("name")
        #return render_template('new.html',name=name)

if __name__=='__main__':
    app.run(debug=True)
