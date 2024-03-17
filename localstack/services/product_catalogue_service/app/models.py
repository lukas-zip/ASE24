from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }