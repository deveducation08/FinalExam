import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, nullable=False)
    alunos = db.relationship('Aluno', backref='disciplina', lazy='dynamic')


class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'))


with app.app_context():
    db.create_all()
    if Disciplina.query.count() == 0:
        for nome in ['DSWA5', 'GPSA5', 'IHCA5', 'SODA5', 'TCOA5']:
            db.session.add(Disciplina(nome=nome))
        db.session.commit()

@app.context_processor
def injetar_data_hora():
    return {'current_time': datetime.utcnow()}

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/teste')
def teste():
    return 'Flasky funcionando perfeitamente!'


@app.route('/cadinvalido')
def cadinvalido():
    return render_template('errorcad.html')


@app.route('/cadAluno')
def cadAluno():
    return redirect(url_for('alunos'))


@app.route('/professores')
def professores():
    return render_template('errorcad.html', current_time=datetime.utcnow())


@app.route('/disciplinas')
def disciplinas():
    return render_template('errorcad.html', current_time=datetime.utcnow())


@app.route('/cursos')
def cursos():
    return render_template('errorcad.html', current_time=datetime.utcnow())


@app.route('/ocorrencias')
def ocorrencias():
    return render_template('errorcad.html', current_time=datetime.utcnow())


@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        disciplina_id = request.form.get('disciplina_id')
        if nome and disciplina_id:
            db.session.add(Aluno(nome=nome, disciplina_id=int(disciplina_id)))
            db.session.commit()
        return redirect(url_for('alunos'))

    lista_disciplinas = Disciplina.query.order_by(Disciplina.nome).all()
    lista_alunos = Aluno.query.all()
    return render_template('cadAluno.html',
                           disciplinas=lista_disciplinas,
                           alunos=lista_alunos,
                           current_time=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)