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
4. install libraries
```
pip install -r requirements.txt
```
5. create tables
```
flask run dropdb
flask run createdb
```

# Run program
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
