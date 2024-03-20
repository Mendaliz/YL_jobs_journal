from flask import Flask, render_template, redirect

from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments

from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            password=form.password.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            poisition=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login')
def login():
    return "Вы зарегистрированы."


def main():
    db_session.global_init("db/mars_explorer.db")

    app.run()

    # session = db_session.create_session()
    #
    # dep = Departments()
    # dep.title = "Исследование звёзд"
    # dep.chief = 1
    # dep.members = "1, 2, 3"
    # dep.email = "the_one@dep.ru"
    #
    # session.add(dep)
    # session.commit()
    #
    #
    # session = db_session.create_session()
    #
    # user = User()
    # user.surname = "Scott"
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # user.hashed_password = "cap"
    #
    # session.add(user)
    # session.commit()
    #
    # job = Jobs()
    # job.team_leader = 1
    # job.job = 'deployment of residential modules 1 and 2'
    # job.work_size = 15
    # job.collaborators = '2, 3'
    # job.is_finished = False
    #
    # session.add(job)
    # session.commit()
    #
    # user = User()
    # user.surname = "Sovenish"
    # user.name = "James"
    # user.age = 35
    # user.position = "navigator"
    # user.speciality = "universe researcher"
    # user.address = "module_2"
    # user.email = "james_navi@mars.org"
    # user.hashed_password = "nav"
    #
    # session.add(user)
    # session.commit()
    #
    # user = User()
    # user.surname = "Kazinski"
    # user.name = "Rachel"
    # user.age = 23
    # user.position = "doctor"
    # user.speciality = "nurse, surgeon, psychologist"
    # user.address = "module_3"
    # user.email = "rache_healer@mars.org"
    # user.hashed_password = "doc"
    #
    # session.add(user)
    # session.commit()
    #
    # user = User()
    # user.surname = "Gishzen"
    # user.name = "Red"
    # user.age = 28
    # user.position = "mechanic"
    # user.speciality = "hand engineer"
    # user.address = "module_4"
    # user.email = "red_crafty@mars.org"
    # user.hashed_password = "mech"
    #
    # session.add(user)
    # session.commit()


if __name__ == '__main__':
    main()
