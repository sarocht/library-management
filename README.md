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

### Run program
To run program, please set postgres config by using environment variable as below before run the program
```
flask run
```

### Test program
One way to test program, you can test by using postman. please import postman collection by using the following link
https://www.getpostman.com/collections/0e8956d672be5c2dba9d


### Run unit test
```
pytest
```

# TODO
- Set logging
- Read config from YAML file
- Add Swagger
