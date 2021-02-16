from flask_restful import Resource, reqparse
from flask_apispec.views import MethodResource
from http import HTTPStatus

from models.book import Book


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', type=str, required=True, help="title is a required parameter!")
parser.add_argument('price', type=str, required=True, help="price is a required parameter!")
parser.add_argument('description', type=str, required=True, help="description is a required parameter!")


class BookListResource(MethodResource, Resource):

    def get(self):
        rows = Book.query.all()
        return [Book.serializer(row) for row in rows]

    def post(self):
        args = parser.parse_args()
        book = Book(title=args['title'], price=args['price'], description=args['description'])
        book.save()
        return Book.serializer(book), HTTPStatus.CREATED


class BookResource(MethodResource, Resource):
    _id =None
    not_found_msg = 'Book with id={} not found'.format(_id)

    def get(self, book_id):
        self._id = book_id
        return Book.serializer(
            Book.query.filter_by(book_id=book_id).first_or_404(description=self.not_found_msg))

    def put(self, book_id):
        self._id = book_id
        book = Book.query.filter_by(book_id=book_id).first_or_404(description=self.not_found_msg)
        args = parser.parse_args()
        book.title = args['title']
        book.price = args['price']
        book.description = args['description']
        book.save()
        return Book.serializer(book), HTTPStatus.CREATED

    def delete(self, book_id):
        self._id = book_id
        book = Book.query.filter_by(book_id=book_id).first_or_404(description=self.not_found_msg)
        book.delete()
        return '', HTTPStatus.NO_CONTENT

