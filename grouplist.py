import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'grouplist.db'),
    DEBUG=True,
    SECRET_KEY='god is good all the time',
    '''USERNAME='admin',
    PASSWORD='default' '''
))
app.config.from_envvar('GROUPLIST_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
    	db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/user_page')
def user_page():
    db = get_db()
    cur_user = db.execute('select username from users where username = g.user')
    groups = db.execute('select groupname, groupmember from groups where groupowner = g.user')
    return render_template('user.html', groups=groups)

@app.route('/add', methods=['POST'])
def add_to_groups_list():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into groups (groupname, groupowner, groupmember) values (?, ?, ?)',
                 [request.form['groupname'], g.user, request.form['groupmember']])
    db.commit()
    flash('New user was successfully added')
    return redirect(url_for('user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	db = get_db()

    	this_username = request.form['username']
    	this_password = request.form['password']
    	
    	username_check = db.execute('select username from users where username = this_username') 
    	if username_check != None
    		db.execute('insert into users (username, password) values (?, ?)',
                 [request.form['username'], request.form['password']])
    		db.commit()
    		session['logged_in'] = True;
    		g.user = username
    		flash('You were logged in successfuly!')
    		return redirect(url_for('user_page'))
    	
    	password_check = db.execute('select password from users where password = this_password')
    	if password_check != None
    		error = 'Wrong password'
    	
    	else: 
    		session['logged_in'] = True;
    		g.username = username
    		flash('You were logged in successfuly!')
    		return redirect(url_for('user_page'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))









