from flask import Blueprint, render_template, redirect, url_for, request, session, flash, make_response
from flask_login import login_required, current_user, login_user, logout_user
from application.models import db, User, Article
from sqlalchemy import desc
import os, random, datetime


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


@bp.route('/article/<id>')
def details(id):
    details = Article.query.filter_by(id=id).first()
    return render_template('details.html', details=details)


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


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@bp.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    print(request.args)
    callback = request.args.get("CKEditorFuncNum")
    print(callback, 123)
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(basedir, 'static', 'img', rnd_name)
        print(filepath)
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
            url = url_for('static', filename='%s/%s' % ('img', rnd_name))
            print(url)
    else:
        error = 'post error'
    res = """
<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    print(response)
    return response


@bp.route('/video')
def video():
    return render_template('video.html')
