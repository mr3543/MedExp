from flask import Flask, url_for, request, \
                  render_template, redirect, flash, session, Response
from time import sleep
from werkzeug.security import check_password_hash, \
                              generate_password_hash
import pymongo
import sqlite3
import database
import search
import recommend
from config import Config

app = Flask(__name__)
app.secret_key = b"\xb0\xcd\x1b4\xcc\x19\x14\x19\xca'\xaf\xad^\xc0\x9b\x82"
  
cfg  = Config()
srch = search.Search(cfg.num_search_results)

def fill_data(rows,user_id):
    data = {'titles':[],'links':[],'statuses':[],'article_ids':[],'user_id':user_id}
    for r in rows:
        title = r['title']
        if len(title) > 75:
            title = title[:75] + "..."
        data['titles'].append(title)
        data['links'].append(r['url'])
        data['article_ids'].append(r['article_id'])
        if r['lib_id']:
            data['statuses'].append('saved')
        else:
            data['statuses'].append('unsaved')
    return data

@app.route('/')
def home():
    user_id = login_user()
    db = database.Db(cfg.db_file)
    num_articles = cfg.num_articles_home
    rows = db.get_articles_by_time(user_id,num_articles)
    data = fill_data(rows,user_id)
    return render_template('articles.html',data=data,
                user_id=user_id,msg=None,page_type="home")
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/user_login',methods = ['POST'])
def user_login():
    uname = request.form['username']
    pwd   = request.form['password']

    if not uname:
        flash('Enter username')
        return redirect(url_for('login'))
    if not pwd:
        flash('Enter password')
        return redicrect(url_for('login'))

    db = database.Db(cfg.db_file)
    pw_hash = generate_password_hash(pwd)
    user_info = db.get_user_info(uname)
    if not user_info:
        flash('Username does not exist')
        return redirect(url_for('login'))
    if not check_password_hash(user_info[0]['pw_hash'],pwd):
        flash('Invalid password')
        return redirect(url_for('login'))

    else:
        session['user_id'] = user_info[0]['user_id']
        return redirect(url_for('home'))

@app.route('/new_user',methods = ['POST'])
def new_user():
    uname = request.form['username']
    pwd   = request.form['password']
    cpwd  = request.form['confirm_password']
    db = database.Db(cfg.db_file)
    if not uname: 
        flash('Enter a valid username')
        return redirect(url_for('signup'))
    elif not pwd:
        flash('Enter a valid password')
        return redirect(url_for('signup'))
    elif pwd != cpwd:
        flash('Passwords must match')
        return redirect(url_for('signup'))
    else:
        pw_hash = generate_password_hash(pwd)
        user_id = db.add_user(uname,pw_hash)
        if user_id < 0:
            flash('An account already exists with that username')
            return redirect(url_for('signup'))
        else:
            session['user_id'] = user_id
            return redirect(url_for('home'))
        
@app.route('/logout',methods = ['GET'])
def logout():
    session.pop('user_id',None)
    return redirect(url_for('home'))


@app.route('/search', methods=['GET'])
def search_articles():
    user_id = login_user()
    token = request.args['search_token']
    db = database.Db(cfg.db_file)
    ids  = srch.search_articles(token)
    rows = db.get_articles_by_id(user_id,ids) 
    data = fill_data(rows,user_id)
    return render_template('articles.html',data=data,
                user_id=user_id,msg=None,page_type="search")

@app.route('/save/<article_id>',methods=['GET'])
def save_article(article_id):
    user_id = login_user()
    if user_id < 0:
        #flash('Login to save articles')
        return {'status':False}
    else:
        db = database.Db(cfg.db_file)
        db.add_article_to_lib(user_id,article_id)
        return {'status':True}


@app.route('/remove/<article_id>',methods=['GET'])
def remove_article(article_id):
    user_id = login_user()
    if user_id < 0:
        #should never hit this
        #flash('Login to remove articles')
        return {'status':False}
    else:
        db = database.Db(cfg.db_file)
        db.remove_article_from_lib(user_id,article_id)
        return {'status':True}

@app.route('/library',methods = ['GET'])
def library():
    user_id = login_user()
    msg = None
    data = None
    if user_id < 0:
        msg = "Please login or create an account to add articles to the library"
    else:
        db = database.Db(cfg.db_file)
        rows = db.get_user_articles(user_id)
        data = fill_data(rows,user_id)

    return render_template('articles.html',data=data,
                user_id=user_id,msg=msg,page_type="library")

@app.route('/recommended',methods = ['GET'])
def recs():
    user_id = login_user()
    msg = None
    data = None
    if user_id < 0:
        msg = "Please login or create an accout to access recommendations"
    else:
        db = database.Db(cfg.db_file)
        rec  = recommend.Rec(db,cfg.xfile,cfg.num_recs)
        ids = rec.get_user_recs(user_id)
        if ids:
            rows = db.get_articles_by_id(user_id,ids)
            data = fill_data(rows,user_id)
        else:
            msg = "Please add articles to your library in order to access recommendations"
    
    return render_template('articles.html',data=data,
                user_id=user_id,msg=msg,page_type="recommended")


def login_user():
    user_id = session.get('user_id')
    db = database.Db(cfg.db_file)
    if user_id:
        user = db.get_user(user_id)
        return user_id if user else -1
    else:
        return -1

if __name__ == '__main__':
    app.debug = True
    app.run()