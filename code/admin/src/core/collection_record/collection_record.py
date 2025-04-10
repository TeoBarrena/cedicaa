from src.core.database import db

class CollectionRecord(db.Model):
    __tablename__ = 'collection_record'
    
    id = db.Column(db.Integer, primary_key=True)
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'), nullable=False)
    rider = db.relationship('Rider')

    payment_date = db.Column(db.Date, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    received_by_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    received_by = db.relationship('Employee')

    notes = db.Column(db.Text, nullable=True)
    is_pay = db.Column(db.Boolean, default=False)

    is_deleted = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<CollectionRecord {self.rider.first_name} {self.rider.last_name} - {self.payment_date}>'
