from flask import Blueprint, render_template, redirect, url_for, request, session, flash, make_response, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from ..forms import LoginForm, PublishForm
from application.models import db, User, Article
from sqlalchemy import desc
import os
import time
import random
import datetime


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(session.get('next') or url_for('blog.home'))
        else:
            flash('用户名或密码不正确！')
            return render_template('login.html', form=form)
    elif request.method == 'GET':
        session['next'] = request.args.get('next')
        return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.home'))


@bp.route('/article')
def article():
    articles = Article.query.order_by(desc(Article.time)).all()
    return render_template('article.html', articles=articles)


@bp.route('/article/<id>')
def details(id):
    details = Article.query.filter_by(id=id).first()
    if details is not None:
        return render_template('details.html', details=details)
    else:
        return render_template('404.html')


@bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PublishForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('publish.html', form=form)
        title = form.title.data
        descp = form.descp.data
        content = form.content.data
        category = request.form.get('radio')
        thumbnail = request.files['thumbnail']
        if thumbnail.filename == '':
            thumb_url = ''
        else:
            fname, fext = os.path.splitext(thumbnail.filename)
            if fext.rsplit('.')[1] not in ALLOWED_EXTENSIONS:
                flash('请上传png,jpg或者gif格式图片！')
                return render_template('publish.html', form=form)
            rnd_name = '%s%s' % (gen_rnd_filename(), fext)
            filepath = os.path.join(basedir, 'static', 'img', 'thumbnail', rnd_name)
            thumbnail.save(filepath)
            thumb_url = url_for('static', filename='%s/%s/%s' % ('img', 'thumbnail', rnd_name))
        new_article = Article(title, descp, content, category, thumb_url)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('blog.article'))
    elif request.method == 'GET':
        return render_template('publish.html', form=form)


@bp.route('/searching')
def searching():
    keyword = request.args.get('keyword')
    return render_template('search.html', keyword=keyword)


@bp.route('/search')
def search():
    keyword = request.args.get('keyword')
    # simulate time taken job
    time.sleep(3)
    result = Article.query.filter(Article.content.contains(keyword)).all()
    if len(result) == 0:
        result.extend(Article.query.filter(Article.title.contains(keyword)).all())
    return render_template('result.html', result=result, keyword=keyword)


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@bp.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(basedir, 'static', 'img', 'article', rnd_name)
        # check if path exists, if not create it
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s/%s' % ('img', 'article', rnd_name))
    else:
        error = 'post error'
    res = """
<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@bp.route('/video')
def video():
    return render_template('video.html')


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
