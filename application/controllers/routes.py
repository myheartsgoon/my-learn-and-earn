from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user, login_user, logout_user
from application.models import db, User, Article
from sqlalchemy import desc

bp = Blueprint(
    'blog',
    __name__,
    template_folder='../templates'
)

@bp.before_request
def make_session_permant():
    session.permanent = True


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(session.get('next') or url_for('blog.home'))
        else:
            flash('用户名或密码不正确！')
            return render_template('login.html')
    elif request.method == 'GET':
        session['next'] = request.args.get('next')
        return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.home'))


@bp.route('/article')
def article():
    articles = Article.query.order_by(desc(Article.time)).all()
    return render_template('article.html', articles=articles)


@bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if request.method == 'POST':
        title = request.form['title']
        descp = request.form['descp']
        content = request.form['content']
        category = request.form['radio']
        new_article = Article(title, descp, content, category)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('blog.article'))
    elif request.method == 'GET':
        return render_template('publish.html')


@bp.route('/video')
def video():
    return render_template('video.html')
