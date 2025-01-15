from app import db, create_app
from app.models import Company, Shareholder
from datetime import date
def seed_data():
    print("Algandmete seeding...")
    company1 = Company(name='Osaühing 1', registry_code='1234567', established_date= date(2020, 1, 1), total_capital=5000)
    company2 = Company(name='Osaühing 2', registry_code='2345671', established_date=date(2022, 2, 11), total_capital=5000)
    company3 = Company(name='Osaühing 3', registry_code='1345672', established_date=date(2022, 11, 15), total_capital=5000)
    company4 = Company(name='Osaühing 4', registry_code='1245673', established_date=date(2023, 5, 21), total_capital=5000)
    company5 = Company(name='Osaühing 5', registry_code='1235674', established_date=date(2024, 2, 2), total_capital=5000)

    db.session.add_all([company1, company2, company3, company4, company5])
    db.session.commit()

    shareholder1 = Shareholder(first_name='Mati', last_name='Mattinen', personal_code='38901011234',  share=2500,
                               is_founder=True, company_id=company1.id)
    shareholder2 = Shareholder(first_name='Kati', last_name='Kattinen', personal_code='49002022345', share=2500,
                               is_founder=False, company_id=company1.id)
    shareholder3 = Shareholder(company_name='Mingi OÜ', registry_code='5566778', share=5000, is_founder=True,
                               company_id=company2.id)
    shareholder4 = Shareholder(first_name='Toomas', last_name='Lepik', personal_code='50103033456', share=5000,
                               is_founder=True, company_id=company3.id)

    db.session.add_all([shareholder1, shareholder2, shareholder3, shareholder4])
    db.session.commit()
    print("Andmed edukalt lisatud!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_data()