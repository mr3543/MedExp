
# medium explorer

This project is a web-service which allows users to browse medium articles and find topics of interest. A user can sign in and get individualized article recommendations based on articles they add to a library. 

### code overview

In order to serve recommendations we need to create tfidf vectors for each article in our database. When a user requests recommendations we take the articles they've saved to thier library and fit a SVM which uses the tfidf vectors to attempt to classify saved and not-saved articles. We use the scores from this SVM to rank article suggestions. 

To host the site you must have the following dependencies installed: 

- pandas/numpy
- sqlite3 
- pymongo
- sklearn
- flask
- werkzeug
- tornado

First we need to download the data, set up our databases and build the tfidf vectors. If you are installing mongodb for the first time you may need to run the following: 

```bash
$ sudo mkdir -p /data/db
$ sudo chown mongodb:mongodb /data/db
```

To download the data and build the tfidf vectors run:

```bash
$ chmod +x data/dl_data.sh
$ ./data/dl_data.sh
$ chmod +x db_create.sh
$ ./db_create.sh
$ python build_db.py
```

Running `build_db.py` may take several minutes. Then we can start the service.

```bash
$ python routes.py
```

We use mongodb to provide text search for the articles in our dataset. 

`search.py` - handles the search logic

`recommend.py` - handles training new SVM when user makes a recommendation request

`database.py` - interface to our sqlite database 

`routes.py` - contains web endpoints


