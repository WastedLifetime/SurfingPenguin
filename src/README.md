# Back End
This code provide the simple structure of Surfing Penguin website.

### Prerequisites
Python 3 is required.
All packages needed are listed in requirements.txt.
You may use the following command to load them if you already have python 3.
```
pip install -r requirements.txt
```
### Setting Environment
If you like to use postgresql, you should set your DATABASE_URL with the head of
"postgres+psycopg2://"
```
export ENV = "Staging" or "Production" or you will use the DevelopmentConfig
export DATABASE_URL= "Your database url" or you will use sqlite as your database
```

### Running the Program
Under src, the following commands help you start the server of the website.
```
export FLASK_APP=surfing_penguin.py
flask run
```

You should see the following content if it runs correctly.
```
 * Serving Flask app "surfing_penguin"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Some api for developers has been added, check them out in route.py.
The HTML templates are to represent the view of administrators.

### Deploying on Heroku
You should set the environment on the Heroku first
```
heroku config:set ENV = "Staging" or "Production" or you will use the DevelopmentConfig
heroku config:set DATABASE_URL= "Your database url" or you will use sqlite as your database
```
Push it to the heroku master branch.
```
git push heroku master
heroku ps:scale web=1
heroku open
```
After open, you can see the website on the heroku.
### Developing Requirement
Attention: All codes committed should pass flake8 syntax check.

### Author
Frank
