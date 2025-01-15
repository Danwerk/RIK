from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, SubmitField, RadioField, FieldList, FormField, \
    HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from datetime import date

class ShareholdersForm(FlaskForm):
    id = HiddenField()
    is_individual = RadioField(
        'Osaniku tüüp',
        choices=[('individual', 'Füüsiline isik'), ('legal', 'Juriidiline isik')],
        validators=[DataRequired()],
        default='individual'
    )
    first_name = StringField('Eesnimi', validators=[Length(max=50)])
    last_name = StringField('Perenimi', validators=[Length(max=50)])
    company_name = StringField('Juriidilise isiku nimi', validators=[Length(max=100)])
    personal_code = StringField('Isikukood', validators=[Length(max=11)])
    registry_code = StringField('Registrikood', validators=[Length(max=7)])
    share = IntegerField('Osa suurus (€)', validators=[ NumberRange(min=1)])
    is_founder = BooleanField('Asutaja')

    def validate(self):
        super_valid = super().validate()
        all_valid = True

        # Kui on füüsiline isik
        if self.is_individual.data == 'individual':
            if not self.first_name.data:
                self.first_name.errors.append('Füüsilise isiku puhul on eesnimi kohustuslik.')
                all_valid = False
            if not self.last_name.data:
                self.last_name.errors.append('Füüsilise isiku puhul on perekonnanimi kohustuslik.')
                all_valid = False
            if not self.personal_code.data:
                self.personal_code.errors.append('Füüsilise isiku puhul on isikukood kohustuslik.')
                all_valid = False

        # Kui on juriidiline isik
        elif self.is_individual.data == 'legal':
            if not self.company_name.data:
                self.company_name.errors.append('Juriidilise isiku puhul on nimi kohustuslik.')
                all_valid = False
            if not self.registry_code.data:
                self.registry_code.errors.append('Juriidilise isiku puhul on registrikood kohustuslik.')
                all_valid = False

        return super_valid and all_valid


class CompanyForm(FlaskForm):
    name = StringField('Firma nimi', validators=[DataRequired(), Length(min=3, max=100)])
    registry_code = StringField('Registrikood', validators=[DataRequired(), Length(min=7, max=7)])
    established_date = DateField('Asutamiskuupäev', validators=[DataRequired()])
    capital = IntegerField('Kogukapital', validators=[DataRequired(), NumberRange(min=2500)])
    shareholders = FieldList(FormField(ShareholdersForm), min_entries=0, max_entries=10)
    submit = SubmitField('Salvesta')

    def validate_established_date(self, field):
        if field.data > date.today():
            raise ValidationError("Asutamiskuupäev ei saa olla tulevikus.")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False

        success = True
        for i, shareholder in enumerate(self.shareholders):
            # Kutsume välja shareholder.form.validate(), et vältida viga
            if not shareholder.form.validate():
                # Kogume kõik vead ja lisame need üldisesse self.shareholders.errors listi
                for field_name, field_errors in shareholder.form.errors.items():
                    for error in field_errors:
                        self.shareholders.errors.append(
                            f"Osanik {i + 1} ({field_name}): {error}"
                        )
                success = False

            shareholder.form.is_founder.data = True

        return success


class EditShareholdersForm(FlaskForm):
    shareholders = FieldList(FormField(ShareholdersForm))
    submit = SubmitField("Salvesta muudatused")
