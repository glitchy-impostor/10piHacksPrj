from flask import Flask, request, render_template, session, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
import random, math, time, threading, json
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cedostwcinnpxv:f35f12f120dd847c2351c1ea3ccdd75c728b349e128b4d8ba620c450614e1d3b@ec2-54-158-232-223.compute-1.amazonaws.com:5432/d6281ta6lftjep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'dcvbhjuygfvbnjm,.hnbvcxswdfdertgfvbnnjhgbvfcerty67654324567uhbvcxz'

class Users(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)#hashed password
    def __repr__(self):
        return '<Task %s>' %self.username

class tasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    repitition = db.Column(db.String(), nullable=False)# Mo#Tu#We#Th#Fr#Sa#Su
    duration = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    last_completed = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.String(8), nullable=False)
    pause = db.Column(db.Boolean(), nullable=False)
    pause_start_time = db.Column(db.String(8), nullable=False)
    time_paused = db.Column(db.String(8), nullable=False)
    def __repr__(self):
        return '<Task %s>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        username = session['username']
        user_tasks = tasks.query.filter_by(username=username).all()
        list = []
        upcoming_tasks = []
        for task in user_tasks:
            array = task.repitition.split('#')[:-1]

        

            date = datetime.today().weekday()


            numToDay = {
                0 : "Mo",
                1 : "Tu" ,
                2 : "We",
                3 : "Th",
                4 : "Fr",
                5 : "Sa",
                6 : "Su"
            }


            #day stores the today's day.
            day = numToDay.get(date)
            print("Todays day is " +day)

            print(array)


            count = 0
            for x in array:
                print("x = " + x)
                if x == day:
                    #This task has to be done today.
                    count = count + 1

            display = False
            if(count > 0):
                list.append(task)
            else:
                upcoming_tasks.append(task)

            print(display)


        return render_template('index.html', tasks=list)
        
    else:
        return redirect('/login')


@app.route('/', methods= ['POST', 'GET'])
def upcoming_tasks():
    if 'username' in session:
        username = session['username']
        user_tasks = tasks.query.filter_by(username=username).all()
        list = []
        upcoming_tasks = []
        for task in user_tasks:
            array = task.repitition.split('#')[:-1]

        

            date = datetime.today().weekday()


            numToDay = {
                0 : "Mo",
                1 : "Tu" ,
                2 : "We",
                3 : "Th",
                4 : "Fr",
                5 : "Sa",
                6 : "Su"
            }


            #day stores the today's day.
            day = numToDay.get(date)
            print("Todays day is " +day)

            print(array)


            count = 0
            for x in array:
                print("x = " + x)
                if x == day:
                    #This task has to be done today.
                    count = count + 1

            display = False
            if(count > 0):
                list.append(task)
            else:
                upcoming_tasks.append(task)

            print(display)

            upcoming = upcoming_tasks


        return render_template('index.html', upcoming = upcoming_tasks)
        
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/api/login', methods=['POST'])
def login_api():
    username = request.form['username']
    password = request.form['password']#hashed
    user_log = Users.query.get(username)
    if user_log:
        if user_log.password == password:
            session['username'] = username
            return jsonify({'conf': 0})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf': 1})

@app.route('/api/signup', methods=['POST'])
def signup_api():
    username = request.form['username']
    password = request.form['password']#hashed
    user_log = Users.query.get(username)
    if user_log:
        return jsonify({'conf': 1})
    else:
        db.session.add(Users(username=username, password=password))
        db.session.commit()
        session['username'] = username
        return jsonify({'conf': 0})

@app.route('/add/task', methods=['GET'])
def add_task():
    if 'username' in session:
        return render_template('add_task.html')
    else:
        session['redirect'] = '/add/task'
        return redirect('/login')

@app.route('/task/<int:id>', methods=['GET', 'POST'])
def expand_task(id):
    if 'username' in session:
        task = tasks.query.get(id)
        if task.start_time == 'NONE':
            s_l = ['00', '00', '00']
        else:
            s_l = task.start_time.split(':')
        d_l = task.duration.split(':')
        print(s_l)
        print(d_l)

        if task.time_paused != 'NONE':
            tp_l = task.time_paused.split(':')
            time_left = str(int(s_l[0]) + int(d_l[0]) + int(tp_l[0])) + ':' + str(int(s_l[1]) + int(d_l[1]) + int(tp_l[1])) + ':' + str(int(s_l[2]) + int(d_l[2]) + int(tp_l[2]))
        else:
            time_left = str(int(s_l[0]) + int(d_l[0])) + ':' + str(int(s_l[1]) + int(d_l[1])) + ':' + str(int(s_l[2]) + int(d_l[2]))
        print(time_left)
        return render_template('expand_task.html', task_name=task.name, task_duration=task.duration, task_repitition=task.repitition.replace('#', ', '), time_left=time_left)
    else:
        session['redirect'] = '/task/' + str(id)
        return redirect('/login')

@app.route('/api/add/task', methods=['POST'])
def add_task_api():
    if 'username' in session:
        name = request.form['name']
        duration = request.form['duration']
        reps = request.form['repitition']
        username = session['username']
        db.session.add(tasks(name=name, duration=duration, repitition=reps, username=username, last_completed='Never', start_time='NONE', pause=False, pause_start_time='NONE', time_paused='NONE'))
        db.session.commit()
        return jsonify({'conf':0})
    else:
        return jsonify({'conf': 1})

@app.route('/api/start/task', methods=['POST'])
def start_task_api():
    if 'username' in session:
        id = request.form['id']
        username = session['username']
        task = tasks.query.get(int(id))
        if task.username == username:
            if task.start_time == 'NONE':
                task.start_time = time.strftime('%H:%M:%S', time.localtime())
                task.pause = False
                task.pause_start_time = 'NONE'
                task.time_paused = 'NONE'
                db.session.commit()
                start_time = task.start_time.split(':')
                d_l = task.duration.split(':')
                time_left = str(int(start_time[0]) + int(d_l[0])) + ':' + str(int(start_time[1]) + int(d_l[1])) + ':' + str(int(start_time[2]) + int(d_l[2]))
                return jsonify({'conf': 0, 'time_left': time_left})
            else:
                return jsonify({'conf': 3})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf': 1})

@app.route('/api/pause/task', methods=['POST'])
def pause_task_api():
    if 'username' in session:
        id = request.form['id']
        username = session['username']
        task = tasks.query.get(int(id))
        if task.username == username:
            if task.start_time != 'NONE':
                if task.pause == False:
                    task.pause_start_time = time.strftime('%H:%M:%S', time.localtime())
                    task.pause = True
                    db.session.commit()
                    return jsonify({'conf': 0})
                else:
                    return jsonify({'conf': 3})
            else:
                return jsonify({'conf': 4})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf': 1})

@app.route('/api/resume/task', methods=['POST'])
def resume_task_api():
    if 'username' in session:
        id = request.form['id']
        username = session['username']
        task = tasks.query.get(int(id))
        if task.username == username:
            if task.start_time != 'NONE':
                if task.pause == True:
                    st_t = task.pause_start_time
                    task.pause_start_time = 'NONE'
                    task.pause = False
                    t_l = st_t.split(':')
                    tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
                    print(tn_l)
                    print(t_l)
                    if task.time_paused == 'NONE':
                        task.time_paused = str(int(tn_l[0]) - int(t_l[0])) + ':' + str(int(tn_l[1]) - int(t_l[1])) + ':' + str(int(tn_l[2]) - int(t_l[2]))
                    else:
                        pt_l = task.time_paused.split(':')
                        task.time_paused = str(int(pt_l[0]) + (int(tn_l[0]) - int(t_l[0]))) + ':' + str(int(pt_l[1]) + (int(tn_l[1]) - int(t_l[1]))) + ":" + str(int(pt_l[2]) + (int(tn_l[2]) - int(t_l[2])))
                    print(task.time_paused)
                    db.session.commit()
                    start_time = task.start_time.split(':')
                    tp_l = task.time_paused.split(':')
                    d_l = task.duration.split(':')
                    tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
                    time_left = str(int(tn_l[0]) - int(start_time[0]) + int(tp_l[0]) + int(d_l[0])) + ':' + str(int(tn_l[1]) - int(start_time[1]) + int(tp_l[1]) + int(d_l[0])) + ':' + str(int(tn_l[2]) - int(start_time[2]) + int(tp_l[2]) + int(d_l[0]))
                    print(time_left)
                    print(task.time_paused)
                    return jsonify({'conf':0, 'time_left': time_left})
                else:
                    return jsonify({'conf': 4})
            else:
                return jsonify({'conf': 3})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf': 1})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000, threaded=True)
