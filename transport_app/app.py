import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel, gettext as _, lazy_gettext as _l
from flask_socketio import SocketIO, emit
from config import Config
from forms import ConducteurForm, InvestisseurForm, AccessCodeForm

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Babel ---
def get_locale():
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

babel = Babel(app, locale_selector=get_locale)

@app.before_request
def before_request():
    if 'lang' in request.args:
        session['lang'] = request.args.get('lang')
    g.lang_code = session.get('lang', app.config['BABEL_DEFAULT_LOCALE'])
    if g.lang_code not in app.config['LANGUAGES']:
        g.lang_code = app.config['BABEL_DEFAULT_LOCALE']

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Modèles de la base de données ---
class Conducteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    gain = db.Column(db.Float)
    miles = db.Column(db.Integer)
    itineraire = db.Column(db.String(150))
    date = db.Column(db.String(20))

class Investisseur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    montant = db.Column(db.Float)

# --- Routes principales ---
@app.route('/')
def index():
    # Page d'accueil avec vidéo + GIF
    return render_template('index.html')

@app.route('/conducteurs')
def conducteurs():
    search = request.args.get('search', '')
    if search:
        data = Conducteur.query.filter(
            (Conducteur.nom.contains(search)) |
            (Conducteur.miles.cast(db.String).contains(search)) |
            (Conducteur.date.contains(search))
        ).all()
    else:
        data = Conducteur.query.all()
    return render_template('conducteurs.html', data=data, search=search)

@app.route('/investisseurs')
def investisseurs():
    search = request.args.get('search', '')
    if search:
        data = Investisseur.query.filter(
            (Investisseur.nom.contains(search)) |
            (Investisseur.montant.cast(db.String).contains(search))
        ).all()
    else:
        data = Investisseur.query.all()
    return render_template('investisseurs.html', data=data, search=search)

@app.route('/add_investisseur', methods=['GET', 'POST'])
def add_investisseur():
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    form = InvestisseurForm()
    if form.validate_on_submit():
        nom = form.nom.data
        montant = form.montant.data
        i = Investisseur(nom=nom, montant=montant)
        db.session.add(i)
        db.session.commit()
        flash(_('Investisseur ajouté avec succès.'), 'success')
        socketio.emit('update_investisseurs', {'action': 'add', 'data': {'id': i.id, 'nom': i.nom, 'montant': i.montant}})
        return redirect(url_for('admin'))
    return render_template('add_investisseur.html', form=form)

# --- Routes pour modifier un investisseur ---
@app.route('/edit_investisseur/<int:id>', methods=['GET', 'POST'])
def edit_investisseur(id):
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    i = Investisseur.query.get_or_404(id)
    if request.method == 'POST':
        i.nom = request.form['nom']
        i.montant = float(request.form['montant'])
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_investisseur.html', investisseur=i)

# --- Route pour supprimer un investisseur ---
@app.route('/delete_investisseur/<int:id>', methods=['POST'])
def delete_investisseur(id):
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    i = Investisseur.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    flash(_('Investisseur supprimé avec succès.'), 'success')
    socketio.emit('update_investisseurs', {'action': 'delete', 'data': {'id': id}})
    return redirect(url_for('admin'))

@app.route('/liaison')
def liaison():
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    form = ConducteurForm()
    return render_template('liaison.html', form=form)

# --- Route pour ajouter un conducteur (exemple de liaison DB) ---
@app.route('/ajouter_conducteur', methods=['POST'])
def ajouter_conducteur():
    nom = request.form['nom']
    gain = float(request.form['gain'])
    miles = int(request.form['miles'])
    itineraire = request.form['itineraire']
    date = request.form['date']
    c = Conducteur(nom=nom, gain=gain, miles=miles, itineraire=itineraire, date=date)
    db.session.add(c)
    db.session.commit()
    flash(_('Conducteur ajouté avec succès.'), 'success')
    socketio.emit('update_conducteurs', {'action': 'add', 'data': {'id': c.id, 'nom': c.nom, 'gain': c.gain, 'miles': c.miles, 'itineraire': c.itineraire, 'date': c.date}})
    return redirect(url_for('admin'))

# --- Routes pour modifier un conducteur ---
@app.route('/edit_conducteur/<int:id>', methods=['GET', 'POST'])
def edit_conducteur(id):
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    c = Conducteur.query.get_or_404(id)
    if request.method == 'POST':
        c.nom = request.form['nom']
        c.gain = float(request.form['gain'])
        c.miles = int(request.form['miles'])
        c.itineraire = request.form['itineraire']
        c.date = request.form['date']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_conducteur.html', conducteur=c)

# --- Route pour supprimer un conducteur ---
@app.route('/delete_conducteur/<int:id>', methods=['POST'])
def delete_conducteur(id):
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    c = Conducteur.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash(_('Conducteur supprimé avec succès.'), 'success')
    socketio.emit('update_conducteurs', {'action': 'delete', 'data': {'id': id}})
    return redirect(url_for('admin'))

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {request.url}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"500 error: {e}")
    db.session.rollback()
    return render_template('500.html'), 500

# --- Route pour le code d'accès ---
@app.route('/access_code', methods=['GET', 'POST'])
def access_code():
    form = AccessCodeForm()
    if form.validate_on_submit():
        code = form.code.data
        if code == app.config['ACCESS_CODE']:
            session['access_granted'] = True
            return redirect(url_for('admin'))
        else:
            flash(_('Code d\'accès incorrect.'), 'danger')
    return render_template('access_code.html', form=form)

@app.route('/protected')
def protected():
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    return render_template('protected.html')

@app.route('/admin')
def admin():
    if not session.get('access_granted'):
        return redirect(url_for('access_code'))
    conducteurs = Conducteur.query.all()
    investisseurs = Investisseur.query.all()
    return render_template('admin.html', conducteurs=conducteurs, investisseurs=investisseurs)

@app.route('/logout')
def logout():
    session.pop('access_granted', None)
    flash(_('Vous avez été déconnecté.'), 'info')
    return redirect(url_for('index'))

# --- API Routes for Kivy App ---
from flask import jsonify

@app.route('/api/conducteurs')
def api_conducteurs():
    conducteurs = Conducteur.query.all()
    data = [{'id': c.id, 'nom': c.nom, 'gain': c.gain, 'miles': c.miles, 'itineraire': c.itineraire, 'date': c.date} for c in conducteurs]
    return jsonify(data)

@app.route('/api/investisseurs')
def api_investisseurs():
    investisseurs = Investisseur.query.all()
    data = [{'id': i.id, 'nom': i.nom, 'montant': i.montant} for i in investisseurs]
    return jsonify(data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0')
