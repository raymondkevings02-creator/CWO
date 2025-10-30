from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import lazy_gettext as _l

class ConducteurForm(FlaskForm):
    nom = StringField(_l('Nom'), validators=[DataRequired()])
    gain = FloatField(_l('Gain ($)'), validators=[DataRequired(), NumberRange(min=0)])
    miles = IntegerField(_l('Miles'), validators=[DataRequired(), NumberRange(min=0)])
    itineraire = StringField(_l('Itinéraire'), validators=[DataRequired()])
    date = StringField(_l('Date (AAAA-MM-JJ)'), validators=[DataRequired()])
    submit = SubmitField(_l('Ajouter'))

class InvestisseurForm(FlaskForm):
    nom = StringField(_l('Nom'), validators=[DataRequired()])
    montant = FloatField(_l('Montant ($)'), validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField(_l('Ajouter'))

class AccessCodeForm(FlaskForm):
    code = PasswordField(_l('Code d\'Accès'), validators=[DataRequired()])
    submit = SubmitField(_l('Valider'))
