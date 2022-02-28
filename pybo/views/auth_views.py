from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data), # generate_password_hash는 암호화하는 함수
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
            # flash는 필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수
            # generate_password_hash 함수로 암호화한 데이터는 복호화할 수 없다. 그래서 로그인할 대 입력받은 비밀번호는 암호화하여 저장된 비밀번호와 비교해야한다.

    # GET 방식이 defalut
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
            # 데이터베이스에 저장된 비밀번호는 암호화되었으므로 입력된 비밀번호와 바로 비교할 수 없다. 입력된 비밀번호는 반드시 check_password_hash 함수로 똑같이 암호화하여 비교해야 한다.
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# request는 요청, 응답이라는 과정에서만 사용할 수 있는 값인 반면,
# 세션은 플라스크 서버를 구동하는 동안에는 영구히 사용할 수 있는 값이므로
# 사용자 id를 저장하거나 활용하는 데 적합하다.
# 단, 세션은 시간제한이 있어서 일정 시간 접속하지 않으면 자동으로 삭제된다.

# 이 에너테이션이 적용된 함수는 라우트 함수보다 먼저 실행된다.
# g는 플라스크가 제공하는 컨텍스트 변수.
# 이 변수는 request 변수와 마찬가지로 [요청 -> 응답] 과정에서 유효하다.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None :
        g.user = None
    else :
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view) :
    @functools.wraps(view)
    def wrappend_view(**kwargs) :
        if g.user is None :
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrappend_view

