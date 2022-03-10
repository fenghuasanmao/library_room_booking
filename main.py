from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime


login_manager = LoginManager()

app=Flask(__name__)
login_manager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yxs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="yanxiushi"
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Yxs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    user_section = db.Column(db.String(250), nullable=False)
    user_phone = db.Column(db.String(250), nullable=False)
    yanxiushi = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.String(250), nullable=False)
    end_date = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_section = request.form["user_section"]
        user_phone = request.form["user_phone"]
        yanxiushi = request.form["yanxiushi"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        if not (user_name and user_section and user_phone and start_date and end_date):
            print(start_date)
            flash("表格中数据不能为空")
            return redirect(url_for('home'))

        else:
            new_yxs = Yxs(
                user_name=user_name,
                user_section=user_section,
                user_phone=user_phone,
                yanxiushi=yanxiushi,
                start_date=start_date,
                end_date=end_date,
                status=0
            )
            db.session.add(new_yxs)
            db.session.commit()
            return redirect(url_for('get_all_yxs'))
    return render_template('index.html', logged_in=current_user.is_authenticated)


@app.route("/status")
def get_all_yxs():
    all_yxs = db.session.query(Yxs).all()
    return render_template("status.html", all_yxs=all_yxs, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]
        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            flash("用户不存在")
            return redirect(url_for('login'))
        elif user.password != password:
            flash("密码错误")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("admin"))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        yxs_id = request.form["yxs.id"]
        if request.form["action"] == "agree":
            yxs_to_update = Yxs.query.get(yxs_id)
            yxs_to_update.status = 1
            db.session.commit()
            return redirect(url_for('admin'))
        elif request.form["action"] == "edit":
            return redirect(url_for('edit', yxs_id=yxs_id))
        elif request.form["action"] == "delete":
            yxs_to_delete = Yxs.query.get(yxs_id)
            db.session.delete(yxs_to_delete)
            db.session.commit()
            return redirect(url_for('admin'))
    all_yxs = db.session.query(Yxs).all()
    return render_template("admin.html", all_yxs=all_yxs, logged_in=current_user.is_authenticated)


@app.route("/edit/<int:yxs_id>", methods=["GET", "POST"])
@login_required
def edit(yxs_id):
    yxs_to_update = Yxs.query.get(yxs_id)
    if request.method == "POST":
        yxs_to_update.user_name = request.form["user_name"]
        yxs_to_update.user_section = request.form["user_section"]
        yxs_to_update.user_phone = request.form["user_phone"]
        yxs_to_update.yanxiushi = request.form["yanxiushi"]
        yxs_to_update.start_date = request.form["start_date"]
        yxs_to_update.end_date = request.form["end_date"]
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("edit.html", yxs_to_update=yxs_to_update, logged_in=current_user.is_authenticated)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_yxs"))


if __name__ == "__main__":
    app.run(debug=True)