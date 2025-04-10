
from src.core.database import db
from sqlalchemy import Numeric
from datetime import datetime


class PaymentRecord(db.Model):
    __tablename__ = 'payment_record'

    id = db.Column(db.Integer, primary_key=True)


    payment_date = db.Column(db.Date, default = datetime.now().date)
    amount = db.Column(Numeric(precision=10, scale=2), nullable=False) #dos números dps del decimal, y máximo 10 numeros antes del .
    payment_type = db.Column(db.Enum('Honorarios', 'Proveedor', 'Gastos varios', name='payment_type'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False)

    # Relación opcional con Employee para el caso de pago de honorarios
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    employee = db.relationship('Employee', back_populates='payment_records')

    def get_payment_type_display(self):
        return self.payment_type