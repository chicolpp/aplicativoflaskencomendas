from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///encomendas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Encomenda
class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    porteiro = db.Column(db.String(100), nullable=False)
    morador = db.Column(db.String(100), nullable=False)
    pagina = db.Column(db.String(50), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Encomenda morador={self.morador}, porteiro={self.porteiro}>'

# Rota inicial
@app.route('/')
def home():
    return render_template('home.html')

# Rota para registrar encomenda
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        porteiro = request.form['porteiro']
        morador = request.form['morador']
        pagina = request.form['pagina']
        data = request.form['data']
        hora = request.form['hora']

        nova_encomenda = Encomenda(
            porteiro=porteiro,
            morador=morador,
            pagina=pagina,
            data=data,
            hora=hora
        )
        db.session.add(nova_encomenda)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('registrar.html')

# Rota para listar encomendas
@app.route('/encomendas')
def encomendas():
    todas_encomendas = Encomenda.query.all()
    return render_template('encomendas.html', encomendas=todas_encomendas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
