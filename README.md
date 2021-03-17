# library-management
this project is only used for demo purpose.

### Prerequisite
- postgres server
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
6. set up database configuration, please replace your database information
```
export POSTGRES_DATABASE_USERNAME=YOUR_DATABASE_USERNAME
export POSTGRES_DATABASE_PASSWORD=YOUR_POSTGRES_DATABASE_PASSWORD
export POSTGRES_DATABASE_URL=YOUR_POSTGRES_DATABASE_URL
export POSTGRES_DATABASE_PORT=YOUR_POSTGRES_DATABASE_PORT
export POSTGRES_DATABASE_NAME=YOUR_POSTGRES_DATABASE_NAME
```
7. create tables
```
flask run dropdb
flask run createdb
```

# Run program
To run program, please set postgres config by using environment variable as below before run the program
```
flask run
```

# Run unit test
```
pytest
```

### TODO
- Set logging
- Read config from YAML file
- Add Swagger
