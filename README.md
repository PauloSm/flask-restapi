# flask-restapi
Flask api developed using Flask, Flask Restful, SQLAlchemy and PostgreSQL

## Installation
1. Clone this repository \
git clone https://github.com/PauloSm/flask-restapi.git

2. Create a virtual enviroment \
python -m venv venv

3. Install requirements.txt \
pip install -r requirements.txt

4. Install PostgreSQL \
https://www.postgresql.org/download/

5. Create a database called books

## Run the application
1. Open the config.py file and edit the database information in the dictionary 'DATABASE_PARAMS': 
* host: localhost
* database: books
* user: the username you configured in the postgresql
* password: the password you configured in the postgresql

2. Run the scraper: \
python scraper.py

3. Run the API: \
python app.py

4. Make a get request to http://127.0.0.1:5000/books 

## API usage
* **URL** \
/books
* **Method** \
Get
* **URL Parameters** \
None
* **Data Parameters** \
None

* **URL** \
/books
* **Method** \
Post
* **URL Parameters** \
None
* **Data Parameters** \
```{'title': 'book title', 'price': 'book price', 'description': 'book description'}```

* **URL** \
/books/:id
* **Method** \
Get
* **URL Parameters** \
book id eg books/10
* **Data Parameters** \
None

* **URL** \
/books/:id
* **Method** \
Put
* **URL Parameters** \
book id eg books/10
* **Data Parameters** \
```{'title': 'book title', 'price': 'book price', 'description': 'book description'}```


* **URL** \
/books/:id
* **Method** \
Delete
* **URL Parameters** \
book id eg books/10
* **Data Parameters** \
None

 **Go to http://127.0.0.1:5000/swagger-ui/#/ for more information about the API**

