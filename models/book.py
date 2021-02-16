from extensions import db


class Book(db.Model):
    __tablename__ = 'book'

    book_id = db.Column(db.Integer, primary_key=True)
    # nullable false e unique true
    title = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.String(10))
    description = db.Column(db.Text)
    url = db.Column(db.String(300), unique=True)

    def serializer(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'url': self.url
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()