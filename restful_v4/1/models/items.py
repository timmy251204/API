from db import db


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)

    def __str__(self):
        return "User(id='%s')" % self.id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @staticmethod
    def get_item(name):
        return Items.query.filter_by(name=name).first()

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

    @staticmethod
    def get_all():
        return Items.query.all()
