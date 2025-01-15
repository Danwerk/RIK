from flask import Blueprint, render_template, flash, redirect, request, url_for, session

from app.forms import CompanyForm, EditShareholdersForm
from app.models import Company, Shareholder
from app import db
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('index.html', title='Avaleht', companies=companies)

@bp.route('/add_company', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()
    if request.method == 'POST':
        print("POST data:", request.form)

    if form.validate_on_submit():
        # todo: this checking should be done in forms
        total_share = 0
        for shareholder_data in form.shareholders.data:
            total_share += shareholder_data.get('share') or 0

        if total_share != form.capital.data:
            flash("Osanike osade summa peab olema võrdne kogukapitaliga.", "danger")
            return render_template('add_company.html', form=form)


        existing_company = Company.query.filter(
            (Company.registry_code == form.registry_code.data) | (Company.name == form.name.data)).first()

        if existing_company:
            if existing_company.registry_code == form.registry_code.data:
                flash(f"Osaühing registrikoodiga {form.registry_code.data} on juba olemas!", "danger")
            elif existing_company.name == form.name.data:
                flash(f"Osaühing nimega {form.name.data} on juba olemas!", "danger")
            return render_template('add_company.html', form=form)

        company = Company(
            name=form.name.data,
            registry_code=form.registry_code.data,
            established_date=form.established_date.data,
            total_capital=form.capital.data,
        )
        db.session.add(company)
        db.session.commit()

        # create shareholders


        for shareholder_data in form.shareholders.data:
            if shareholder_data['is_individual'] == 'individual':
                if not shareholder_data['first_name'] or not shareholder_data['last_name'] or not shareholder_data[
                    'personal_code']:
                    flash("Füüsilise isiku puhul on eesnimi, perekonnanimi ja isikukood kohustuslikud.", "danger")
                    return render_template('add_company.html', form=form)
                elif shareholder_data['is_individual'] == 'legal':
                    # Juriidiline isik
                    if not shareholder_data['company_name'] or not shareholder_data['registry_code']:
                        flash("Juriidilise isiku puhul on nimi ja registrikood kohustuslikud.", "danger")
                        return render_template('add_company.html', form=form)
            shareholder = Shareholder(
                first_name=shareholder_data.get('first_name'),
                last_name=shareholder_data.get('last_name'),
                company_name=shareholder_data.get('company_name'),
                personal_code=shareholder_data.get('personal_code'),
                registry_code=shareholder_data.get('registry_code'),
                share=shareholder_data.get('share'),
                is_founder=True,
                company_id=company.id
            )
            db.session.add(shareholder)



        db.session.commit()

        flash(f'Osaühing "{company.name}" ja osanikud on edukalt lisatud', 'success')
        return redirect(url_for('main.index'))
    else:
        print("Shareholder data after validation:", form.shareholders.data)
        print("Form errors: ", form.errors)
    return render_template('add_company.html', title="Lisa osaühing", form=form)

@bp.route('/company/<int:company_id>')
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company_details.html', title=company.name, company=company)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q')
    results = []
    if query:
        companies = Company.query.filter(
            (Company.name.ilike(f"%{query}%")) | (Company.registry_code.ilike(f"%{query}%"))
        ).all()

        shareholders = Shareholder.query.filter(
            (Shareholder.first_name.ilike(f"%{query}%")) | (Shareholder.last_name.ilike(f"%{query}%"))
        ).all()

        shareholder_companies = {shareholder.company for shareholder in shareholders}

        # Kombineerime mõlemad tulemused ilma duplikaatideta
        results = list(set(companies).union(shareholder_companies))




    return render_template('search.html', title="Otsingutulemused", results=results, query=query)

@bp.route('/company/<int:company_id>/edit-shareholders', methods=['GET', 'POST'])
def edit_shareholders(company_id):
    company = Company.query.get_or_404(company_id)
    form = EditShareholdersForm()

    if not company:
        flash('Ettevõtet ei leitud.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        print("POST data:", request.form)


        # Uuendame olemasolevaid osanikke
        for i, shareholder_form in enumerate(form.shareholders):
            shareholder = Shareholder.query.get(shareholder_form.data['id'])
            if shareholder:
                shareholder.share = shareholder_form.data['share']
                shareholder.is_founder = shareholder_form.data['is_founder']

            else:  # Uus osanik
                new_shareholder = Shareholder(
                    first_name=shareholder_form.first_name.data,
                    last_name=shareholder_form.last_name.data,
                    company_name=shareholder_form.company_name.data,
                    personal_code=shareholder_form.personal_code.data,
                    registry_code=shareholder_form.registry_code.data,
                    share=shareholder_form.share.data,
                    is_founder=shareholder_form.is_founder.data,
                    company_id=company_id,
                )
                db.session.add(new_shareholder)

        # Uuendame ettevõtte kogukapitali
        company.total_capital = sum([sh.share for sh in company.shareholders])

        db.session.commit()
        flash('Osanike andmed on edukalt uuendatud!', 'success')
        return redirect(url_for('main.company_details', company_id=company_id))


    # Lisame olemasolevad osanikud vormi
    if not form.shareholders:
        form.shareholders = company.shareholders

    return render_template('edit_shareholders.html', form=form, company=company)

