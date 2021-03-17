# library-management
this project is only used for demo purpose.

### Brief explanation
To build rest service, I saparate program into 3 layers
1. controller: mainly responsible for routing
2. service: responsible for business logic
3. model: responsible for interaction between server and database

### Prerequisite
- docker [optional: if you already have postgres server, you don't need this]
- python3.8
- pipenv
- pip3

# Installation step
1. clone git repository
```
git clone https://github.com/sarocht/library-management.git
```
2. go to library-management directory
```
cd library-management
```
3. create virtual environment
```
pipenv install
```
4. Activate virtual environment
```
pipenv shell
```
5. install libraries
```
pip install -r requirements.txt
```
6. set up postgres database [optional: if you already have postgres server, you can skip this step]
```
docker run -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=postgres -p 5432:5432 library/postgres
```
7. set up database configuration, please replace your database information.
[optional: if you set up postgres database by step 6 you can skip this step]
```
export POSTGRES_DATABASE_USERNAME=admin
export POSTGRES_DATABASE_PASSWORD=mysecretpassword
export POSTGRES_DATABASE_URL=localhost
export POSTGRES_DATABASE_PORT=5432
export POSTGRES_DATABASE_NAME=postgres
```
8. create tables
```
flask run dropdb
flask run createdb
```

### Run unit test
```
pytest
```

### Run program
To run program, please set postgres config by using environment variable as below before run the program
```
flask run
```

### Test program
One way to test program, you can test by using postman. please import postman collection by using the following link
https://www.getpostman.com/collections/0e8956d672be5c2dba9d

### Shortly API Explanation and Example (This should be done in Swagger file)
1. Add book, isbn must be existing in Google Books API
```
curl --location --request POST 'http://localhost:5000/book' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "isbn:1501124021"
}'
```
2. Search or Get book information, you can search book by isbn or book title 
```
curl --location --request GET 'http://localhost:5000/book?typ=isbn&isbn=isbn:1501124021'
curl --location --request GET 'http://localhost:5000/book?typ=title&title=Principles'
```
3. Update book information
```
curl --location --request PUT 'http://localhost:5000/book' \
--header 'Content-Type: application/json' \
--data-raw '{
    "created_date": "2021-03-13",
    "info_link": "http://books.google.co.th/books?id=okk1DwAAQBAJ&dq=isbn:1501124021&hl=&source=gbs_api!",
    "isbn": "isbn:1501124021",
    "page_count": 10,
    "published_date": "2017-09-13",
    "publisher": "Simon and Schuster!",
    "status": "Available",
    "subtitle": "Life and Work!",
    "title": "Principles!"
}'
```
4. Delete book
```
curl --location --request DELETE 'http://localhost:5000/book' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "isbn:1501124021"
}'
```
5. Get all books in library
```
curl --location --request GET 'http://localhost:5000/books'
```
6. Borrowed book
```
curl --location --request POST 'http://localhost:5000/book/borrow' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "isbn:1501124021",
    "created_by": "nat",
    "borrowed_by": "note"
}'
```



# TODO
- Set logging
- Read config from YAML file
- Add Swagger
