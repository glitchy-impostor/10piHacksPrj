from flask import Flask, request, render_template, session, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
import random, math, time, threading, json, requests
from datetime import date, datetime, timedelta

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
    repitition = db.Column(db.String(), nullable=False)# Mo#Tu#We#Th#Fr#Sa#Su#
    duration = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    last_completed = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.String(8), nullable=False)
    pause = db.Column(db.Boolean(), nullable=False)
    pause_start_time = db.Column(db.String(8), nullable=False)
    time_paused = db.Column(db.String(8), nullable=False)
    minitask_list = db.Column(db.String(), nullable=False) # id1#id2#id3#
    def __repr__(self):
        return '<Task %s>' %self.id

class longTermTasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    checkListTasks = db.Column(db.String(), nullable=False) # id1#id2#id3#
    tasksList = db.Column(db.String(), nullable=False) # id1#id2#id3#
    completed = db.Column(db.Boolean(), nullable=False)
    def __repr__(self):
        return '<Task %s>' %self.id

class checkListForLongTermTasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    lognTermTaskId = db.Column(db.Integer(), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    tasksList = db.Column(db.String(), nullable=False) # id1#id2#id3#
    estTimeReq = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False)
    def __repr__(self):
        return '<Task %s>' %self.id

@app.route('/')
def a():
    return redirect('/today')

@app.route('/today', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        username = session['username']
        user_tasks = tasks.query.filter_by(username=username).all()
        list = []
        for task in user_tasks:
            array = task.repitition.split('#')[:-1]
            date_ = datetime.today().weekday()
            numToDay = {
                0 : "Mo",
                1 : "Tu" ,
                2 : "We",
                3 : "Th",
                4 : "Fr",
                5 : "Sa",
                6 : "Su"
            }
            day = numToDay.get(date_)
            print("Todays day is " +day)
            count = 0
            for x in array:
                print("x = " + x)
                if x == day:
                    count = count + 1
            display = False
            if(count > 0):
                list.append(task)
        return render_template('index.html', tasks=list, date=str(date.today()))
    else:
        return redirect('/login')

@app.route('/all', methods=['GET'])
def index_3():
    if 'username' in session:
        username = session['username']
        all_tasks = tasks.query.filter_by(username=username).all()
        mon = []
        tue = []
        wed = []
        thu = []
        fri = []
        sat = []
        sun = []
        for task in all_tasks:
            array = task.repitition.split('#')[:-1]
            for a in array:
                if a == 'Mo':
                    mon.append(task)
                elif a == 'Tu':
                    tue.append(task)
                elif a == 'We':
                    wed.append(task)
                elif a == 'Th':
                    thu.append(task)
                elif a == 'Fr':
                    fri.append(task)
                elif a == 'Sa':
                    sat.append(task)
                elif a == 'Su':
                    sun.append(task)
        d = str(date.today())
        d_2 = str((datetime.now() + timedelta(days=1)).date())
        d_3 = str((datetime.now() + timedelta(days=2)).date())
        d_4 = str((datetime.now() + timedelta(days=3)).date())
        d_5 = str((datetime.now() + timedelta(days=4)).date())
        d_6 = str((datetime.now() + timedelta(days=5)).date())
        d_7 = str((datetime.now() + timedelta(days=6)).date())
        due_tasks = longTermTasks.query.filter(or_(longTermTasks.date==d, longTermTasks.date==d_2, longTermTasks.date==d_3, longTermTasks.date==d_4, longTermTasks.date==d_5, longTermTasks.date==d_6, longTermTasks.date==d_7)).all()
        return render_template('index_3.html', mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, sun=sun, due_tasks=due_tasks)
    else:
        session['redirect'] = '/all'
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
        return render_template('a.html')
    else:
        session['redirect'] = '/add/task'
        return redirect('/login')

@app.route('/add/t')
def add_t():
    return render_template('a.html')

@app.route('/task/<int:id>', methods=['GET', 'POST'])
def expand_task(id):
    if 'username' in session:
        task = tasks.query.get(id)
        d_l = task.duration.split(':')
        tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
        if task.start_time == 'NONE':
            state = 0
            s_l = ['00', '00', '00']
            time_left = task.duration
        else:
            if task.pause == True:
                state = 2
            else:
                state = 1
            s_l = task.start_time.split(':')
            if task.time_paused != 'NONE':
                tp_l = task.time_paused.split(':')
                h = (-(int(tn_l[0]) - int(s_l[0])) + int(d_l[0]) + int(tp_l[0]))
                m = (-(int(tn_l[1]) - int(s_l[1])) + int(d_l[1]) + int(tp_l[1]))
                s = (-(int(tn_l[2]) - int(s_l[2])) + int(d_l[2]) + int(tp_l[2]))
                if s < 0:
                    m -= 1
                    s = 60 +s
                if m < 0:
                    h -= 1
                    m = 60 + m
                time_left = str(h) + ':' + str(m) + ':' + str(s)
            else:
                h = (-(int(tn_l[0]) - int(s_l[0])) + int(d_l[0]))
                m = (-(int(tn_l[1]) - int(s_l[1])) + int(d_l[1]))
                s = (-(int(tn_l[2]) - int(s_l[2])) + int(d_l[2]))
                if s < 0:
                    m -= 1
                    s = 60 +s
                if m < 0:
                    h -= 1
                    m = 60 + m
                time_left = str(h) + ':' + str(m) + ':' + str(s)
        return render_template('expand_task.html', task_name=task.name, task_duration=task.duration, task_repitition=task.repitition.replace('#', ', '), time_left=time_left, state=state)
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
        db.session.add(tasks(name=name, duration=duration, repitition=reps, username=username, last_completed='Never', start_time='NONE', pause=False, pause_start_time='NONE', time_paused='NONE', minitask_list=''))
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
                return jsonify({'conf': 0, 'time_left': task.duration})
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
                    if task.time_paused == 'NONE':
                        task.time_paused = str(int(tn_l[0]) - int(t_l[0])) + ':' + str(int(tn_l[1]) - int(t_l[1])) + ':' + str(int(tn_l[2]) - int(t_l[2]))
                    else:
                        pt_l = task.time_paused.split(':')
                        task.time_paused = str(int(pt_l[0]) + (int(tn_l[0]) - int(t_l[0]))) + ':' + str(int(pt_l[1]) + (int(tn_l[1]) - int(t_l[1]))) + ":" + str(int(pt_l[2]) + (int(tn_l[2]) - int(t_l[2])))
                    db.session.commit()
                    start_time = task.start_time.split(':')
                    tp_l = task.time_paused.split(':')
                    d_l = task.duration.split(':')
                    tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
                    h = (-(int(tn_l[0]) - int(start_time[0])) + int(tp_l[0]) + int(d_l[0]))
                    m = (-(int(tn_l[1]) - int(start_time[1])) + int(tp_l[1]) + int(d_l[1]))
                    s = (-(int(tn_l[2]) - int(start_time[2])) + int(tp_l[2]) + int(d_l[2]))
                    if s < 0:
                        m -= 1
                        s = 60 + s
                    if m < 0:
                        h -= 1
                        m = 60 + m
                    time_left = str(h) + ':' + str(m) + ':' + str(s)
                    return jsonify({'conf':0, 'time_left': time_left})
                else:
                    return jsonify({'conf': 4})
            else:
                return jsonify({'conf': 3})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf': 1})

@app.route('/api/check/done', methods=['POST'])
def check_done_api():
    if 'username' in session:
        id = int(request.form['id'])
        task = tasks.query.get(id)
        username = session['username']
        if task.username == username:
            if task.pause == False and task.start_time != 'NONE':
                if task.time_paused != 'NONE':
                    start_time = task.start_time.split(':')
                    tp_l = task.time_paused.split(':')
                    d_l = task.duration.split(':')
                    tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
                    h = (-(int(tn_l[0]) - int(start_time[0])) + int(tp_l[0]) + int(d_l[0]))
                    m = (-(int(tn_l[1]) - int(start_time[1])) + int(tp_l[1]) + int(d_l[1]))
                    s = (-(int(tn_l[2]) - int(start_time[2])) + int(tp_l[2]) + int(d_l[2]))
                    if s < 0:
                        m -= 1
                        s = 60 + s
                    if m < 0:
                        h -= 1
                        m = 60 + m
                    if h <= 0:
                        task.last_completed = str(date.today())
                        task.start_time = 'NONE'
                        task.pause = False
                        task.pause_start_time = 'NONE'
                        task.time_paused = 'NONE'

                        db.session.commit()
                        return jsonify({'conf':0})
                    else:
                        return jsonify({'conf': 1, 'time_left': (str(h) + ':' + str(m) + ':' + str(s))})
                else:
                    s_l = task.start_time.split(':')
                    d_l = task.duration.split(':')
                    tn_l = time.strftime('%H:%M:%S', time.localtime()).split(':')
                    h = (-(int(tn_l[0]) - int(s_l[0])) + int(d_l[0]))
                    m = (-(int(tn_l[1]) - int(s_l[1])) + int(d_l[1]))
                    s = (-(int(tn_l[2]) - int(s_l[2])) + int(d_l[2]))
                    if s < 0:
                        m -= 1
                        s = 60 +s
                    if m < 0:
                        h -= 1
                        m = 60 + m
                    print(h,m,s)
                    if h <= 0:
                        task.last_completed = str(date.today())
                        task.start_time = 'NONE'
                        task.pause = False
                        task.pause_start_time = 'NONE'
                        task.time_paused = 'NONE'
                        li = task.minitask_list.split('#')[:-1]
                        for t in li:
                            minitask = checkListForLongTermTasks.query.get(int(t))
                            est_time_l = minitask.estTimeReq.split(':')
                            d_l = task.duration.split(':')
                            h = int(est_time_l[0]) - int(d_l[0])
                            m = int(est_time_l[1]) - int(d_l[1])
                            s = int(est_time_l[2]) - int(d_l[2])
                            if s < 0:
                                m -=1
                                s = 60 +s
                            if m < 0:
                                h -=1
                                m = 60 +m
                            if h < 0:
                                h=0
                                m=0
                                s=0
                            minitask.estTimeReq = str(h) + ':' + str(m) + ':' + str(s)
                            db.session.commit()
                        db.session.commit()
                        return jsonify({'conf':0})
                    else:
                        return jsonify({'conf': 1, 'time_left': (str(h) + ':' + str(m) + ':' + str(s))})
            else:
                return jsonify({'conf': 1, 'time_left': task.duration})
        else:
            return jsonify({'conf': 2})
    else:
        return jsonify({'conf':2})

@app.route('/api/add/longTermTask', methods=['POST'])
def add_lognTermTask_api():
    if 'username' in session:
        name = request.form['name']
        date = request.form['date']
        username = session['username']
        db.session.add(longTermTasks(name=name, date=date, username=username, checkListTasks='0/0', tasksList='', completed=False))
        db.session.commit()
        return jsonify({'conf': 0})
    else:
        return jsonify({'conf':1})


@app.route('/add/longTermTask', methods=['GET'])
def add_longTermTask():
    if 'username' in session:
        return render_template('add_longTermTask.html')
    else:
        session['redirect'] = '/add/longTermTask'
        return redirect('/login')

@app.route('/add/checkListTask', methods=['GET'])
def add_checkListTask():
    if 'username' in session:
        return render_template('add_checkListTask.html')
    else:
        session['redirect'] = '/add/checkListTask'
        return redirect('/login')

@app.route('/show/longTermTasks', methods=['GET'])
def show_longTermTasks():
    if 'username' in session:
        username = session['username']
        tasks = longTermTasks.query.filter_by(username=username).all()
        return render_template('index_2.html', tasks=tasks)
    else:
        session['redirect'] = '/show/longTermTasks'
        return redirect('/login')

@app.route('/longTermTask/<int:id>', methods=['GET'])
def longTermTask_single(id):
    if 'username' in session:
        username = session['username']
        longTermTask = longTermTasks.query.get(id)
        if longTermTask:
            if longTermTask.username == username:
                cl = longTermTask.checkListTasks.split('#')[:-1]
                minitasks = checkListForLongTermTasks.query.filter_by(username=username).filter_by(lognTermTaskId=id).all()
                return render_template('longTermTask.html', task=longTermTask, minitasks=minitasks)
            else:
                session['redirect'] = '/login'
                return redirect('/login')
        else:
            return 'NO SUCH ITEM FOUND!'
    else:
        session['redirect'] = '/login'
        return redirect('/login')

@app.route('/add/minitask/<int:id>', methods=['GET'])
def add_minitask(id):
    if 'username' in session:
        username = session['username']
        return render_template('add_minitask.html')
    else:
        session['redirect'] = '/add/minitask/' + str(id)
        return redirect('/login')

@app.route('/api/add/minitask', methods=['POST'])
def add_minitask_api():
    if 'username' in session:
        id = int(request.form['id'])
        name = request.form['name']
        date = request.form['date']
        username = session['username']
        estTimeReq = request.form['estTimeReq']
        db.session.add(checkListForLongTermTasks(name=name, date=date, lognTermTaskId=id, username=username, tasksList='', completed=False, estTimeReq=estTimeReq))
        lTT = longTermTasks.query.get(id)
        l = lTT.checkListTasks.split('/')
        lTT.checkListTasks = l[0] + '/' + str(int(l[1]) + 1)
        db.session.commit()
        return jsonify({'conf': 0})
    else:
        return jsonify({'conf': 1})

@app.route('/minitask/<int:id>', methods=['GET'])
def minitask(id):
    if 'username' in session:
        task = checkListForLongTermTasks.query.get(id)
        name = longTermTasks.query.get(task.lognTermTaskId).name
        list = task.tasksList.split('#')[:-1]
        print(list)
        send_list = []
        for item in list:
            send_list.append(tasks.query.get(int(item)))
        print(send_list)
        d_l = task.date.split('-')
        print(d_l)
        days_left = (date(int(d_l[0]), int(d_l[1]), int(d_l[2])) - date.today()).days
        t_l = task.estTimeReq.split(':')
        print(days_left)
        hPerDay = int(t_l[0])/days_left
        mPerDay = int(t_l[1])/days_left
        print(hPerDay, 'h')
        print(mPerDay, 'm')
        return render_template('minitask.html', task=task, send_list=send_list, name=name)
    else:
        session['redirect'] = '/minitask/' + str(id)
        return redirect('/login')

@app.route('/link/tasks/<int:id>', methods=['GET'])
def link_tasks(id):
    if 'username' in session:
        username = session['username']
        task_list = tasks.query.filter_by(username=username).all()
        selected_list = checkListForLongTermTasks.query.get(id).tasksList.split('#')
        return render_template('task_linker.html', tasks=task_list, selected_list=selected_list)
    else:
        session['redirect'] = '/link/tasks/' + str(id)
        return redirect('/login')

@app.route('/api/link/tasks', methods=['POST'])
def link_tasks_api():
    if 'username' in session:
        username = session['username']
        id = request.form['id']
        str_list = request.form['str_list']
        print(str_list)
        task = checkListForLongTermTasks.query.get(int(id))
        task.tasksList = str_list
        li = str_list.split('#')[:-1]
        for t in li:
            task = tasks.query.get(int(t))
            task.minitask_list += id + '#'
            db.session.commit()
        db.session.commit()
        print('aa')
        return jsonify({'conf':0})
    else:
        print('lg')
        return jsonify({'conf':1})

@app.route('/api/minitask/completed', methods=['POST'])
def minitask_completed_api():
    if 'username' in session:
        id = int(request.form['id'])
        task = checkListForLongTermTasks.query.get(id)
        task.completed = True
        lTT = longTermTasks.query.get(task.lognTermTaskId)
        li = lTT.checkListTasks.split('/')
        lTT.checkListTasks = str(int(li[0]) + 1) + '/' + li[1]
        db.session.commit()
        return jsonify({'conf': 0, 'longTermTaskId': task.lognTermTaskId})
    else:
        return jsonify({'conf':1})

@app.route('/api/longTermTask/completed', methods=['POST'])
def longTermTask_completed_api():
    if 'username' in session:
        id = int(request.form['id'])
        task = longTermTasks.query.get(id)
        li = task.checkListTasks.split('/')
        if int(li[0]) == int(li[1]):
            task.completed = True
            db.session.commit()
            return jsonify({'conf': 0})
        else:
            return jsonify({'conf':2})
    else:
        return jsonify({'conf': 1})

@app.route('/show/minitasks', methods=['GET'])
def show_minitasks():
    if 'username' in session:
        username = session['username']
        tasks = checkListForLongTermTasks.query.filter_by(username=username).all()
        names = {}
        for task in tasks:
            names[task.id] = longTermTasks.query.get(task.lognTermTaskId).name
        return render_template('show_minitasks.html', tasks=tasks, name=names)
    else:
        session['redirect'] = '/show/minitasks'
        return redirect('/login')

@app.route('/api/task/complete', methods=['POST'])
def task_complete_api():
    if 'username' in session:
        username = session['username']
        id = int(request.form['id'])
        task = tasks.query.get(id)
        task.last_completed = str(date.today())
        task.start_time = 'NONE'
        task.pause = False
        task.pause_start_time = 'NONE'
        task.time_paused= 'NONE'
        li = task.minitask_list.split('#')[:-1]
        for t in li:
            minitask = checkListForLongTermTasks.query.get(int(t))
            est_time_l = minitask.estTimeReq.split(':')
            d_l = task.duration.split(':')
            h = int(est_time_l[0]) - int(d_l[0])
            m = int(est_time_l[1]) - int(d_l[1])
            s = int(est_time_l[2]) - int(d_l[2])
            if s < 0:
                m -=1
                s = 60 +s
            if m < 0:
                h -=1
                m = 60 +m
            if h < 0:
                h=0
                m=0
                s=0
            minitask.estTimeReq = str(h) + ':' + str(m) + ':' + str(s)
            db.session.commit()
        db.session.commit()
        return jsonify({'conf': 0})
    else:
        return jsonify({'conf': 1})

@app.route('/majors', methods=['GET'])
def majors_page():
    r = requests.get('http://98.207.110.6/majors')
    return render_template('majors.html', json=r.json())

@app.route('/major/<name>', methods=['GET'])
def major_page(name):
    r = requests.get('http://98.207.110.6/major/?' + name)
    li = r.json()['Message']['Top 5 Colleges'].split('.')
    a = li[1][:-1]
    b = li[2][:-1]
    c = li[3][:-1]
    d = li[4][:-1]
    e = li[5][:-1]
    return render_template('major.html', json=r.json(), major_name=name, a=a,b=b,c=c,d=d,e=e)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000, threaded=True)
