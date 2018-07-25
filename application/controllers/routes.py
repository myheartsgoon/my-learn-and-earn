from flask import Blueprint, render_template, redirect, url_for, request, session, flash, make_response, current_app, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from ..forms import LoginForm, PublishForm
from application.models import db, User, Article
from sqlalchemy import desc, or_
import os
import random
import datetime


basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bp = Blueprint(
    'blog',
    __name__,
    template_folder='../templates'
)


@bp.before_request
def make_session_permant():
    """Make session permanent to avoid flask expires the session once close
    the browser. To limit permanent session lifetime, please go to
    configs.py and set variable PERMANENT_SESSION_LIFETIME.
    """
    session.permanent = True


@bp.route('/')
def home():
    """Home page route for the web site. This func will first order articles
    based on likes and select top 5 to list.
    :return: render the home page with query result.
    """
    feat_articles = Article.query.order_by(desc(Article.likes)).limit(5).all()
    return render_template('home.html', feat_articles=feat_articles)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route for admin to login to system.
    :return: redirect to home page if a success login, else it will render the
             page with error messages.
    """
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
def logout():
    """Logout the current user.
    :return: redirect to home page.
    """
    logout_user()
    return redirect(url_for('blog.home'))


@bp.route('/articles/page/<int:page>')
def articles(page=1):
    """Paginate and list articles by requested page number
    :param page: integer type, the page number to show.
    :return: render articles.html.
    """
    articles = Article.query.order_by(desc(Article.time)).paginate(
                page, current_app.config['PER_PAGE'], error_out=False)
    return render_template('article.html', articles=articles)


@bp.route('/article/<int:id>')
def details(id):
    """Show contents of an article.
    :param id: article id.
    :return: render contents if id exists, else render 404 page.
    """
    details = Article.query.filter_by(id=id).first()
    if details is not None:
        return render_template('details.html', details=details)
    else:
        return render_template('404.html')


@bp.route('/category/<category>/page/<int:page>')
def category(category, page=1):
    """Return articles under certain category.
    :param category: article category.
    :param page: integer type, page number.
    :return: render category.html
    """
    result = Article.query.filter_by(category=category).order_by(desc(Article.time)).paginate(
                page, current_app.config['PER_PAGE'], error_out=False)
    return render_template('category.html', result=result, category=category)


@bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    """Publish an article with CKEditor integrated.
    :return: redirect to all articles page if a success publish, else render
    the template with error messages.
    """
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
            # upload thumbnail images
            fname, fext = os.path.splitext(thumbnail.filename)
            if fext.rsplit('.')[1] not in current_app.config['ALLOWED_EXTENSIONS']:
                flash('请上传png,jpg或者gif格式图片！')
                return render_template('publish.html', form=form)
            rnd_name = '%s%s' % (gen_rnd_filename(), fext)
            filepath = os.path.join(basedir, 'static', 'img', 'thumbnail', rnd_name)
            thumbnail.save(filepath)
            thumb_url = url_for('static', filename='%s/%s/%s' % ('img', 'thumbnail', rnd_name))
        new_article = Article(title, descp, content, category, thumb_url)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('blog.articles', page=1))
    elif request.method == 'GET':
        return render_template('publish.html', form=form)


@bp.route('/manage')
@login_required
def manage():
    """Admin management interface. Admin can publish, delete and view
    information for the articles.
    :return: render template manage.html.
    """
    articles = Article.query.order_by(desc(Article.time)).all()
    return render_template('manage.html', articles=articles)


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    """Delete requested articles. This will receive POST request from manage
    interface(using jQuery ajax), and delete articles based on form parameter
    'ids'.
    :return: redirect to manage page with flash messages.
    """
    ids = request.form.get('ids')
    filter_args = (Article.id == int(i) for i in ids.split(','))
    result = Article.query.filter(or_(filter_args)).delete()
    db.session.commit()
    if result > 0:
        flash('{0}篇文章已删除'.format(str(result)))
        return redirect(url_for('blog.manage'))
    else:
        flash('所选文章不存在或已删除'.format(str(result)))
        return redirect(url_for('blog.manage'))


@bp.route('/like_article')
def like_article():
    """ Like an article. This route is used by jQuery ajax function in article
    details page.
    :return: return json object with success value(1 if success else 0).
    """
    id = request.args.get('id')
    if id is not None:
        article = Article.query.filter_by(id=int(id)).first()
        article.likes = Article.likes + 1
        db.session.commit()
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0})


@bp.route('/searching')
def searching():
    """Search keyword render page. This route will show search result which jQuery
    ajax call gets.
    :return: render page if keyword is not None, else redirect to home page.
    """
    keyword = request.args.get('keyword')
    if keyword is not None:
        return render_template('search.html', keyword=keyword)
    else:
        return redirect(url_for('blog.home'))


@bp.route('/search')
def search():
    """Search keyword from database. This is the method which jQuery ajax
    will call. The return object will be rendered in search keyword page.
    :return: render result.html with query result.
    """
    keyword = request.args.get('keyword')
    # simulate time taken job
    # time.sleep(1)
    result = Article.query.filter(Article.content.contains(keyword)).all()
    if len(result) == 0:
        result.extend(Article.query.filter(Article.title.contains(keyword)).all())
    return render_template('result.html', result=result, keyword=keyword)


def gen_rnd_filename():
    """Generate random filename based on current time.
    :return:
    """
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@bp.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor image upload. CKEditor will call this method when uploading
    a image. The URL is defined in publish page('filebrowserUploadUrl').
    """
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
    """Video page.
    :return: render video.html.
    """
    return render_template('video.html')


@bp.app_errorhandler(404)
def page_not_found(error):
    """Error handler for 404.
    :param error: error param.
    :return:
    """
    return render_template('404.html'), 404
