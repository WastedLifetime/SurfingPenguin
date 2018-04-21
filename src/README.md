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
We will teach you how to use Heroku Cli to deploy the website
First, create a heroku app and then connect it.
```
heroku create
heroku git:remote -a "Your app name"
```

If you want to create a postgresql, the following command can help you.
```
heroku addons:create heroku-postgresql:hobby-dev
```

You should create a .ENV file includeing the following content.
```
DATABASE_URL="Your database url" or you will use sqlite as your database
ENV="Staging" or "Production" or you will use the DevelopmentConfig
```

Push it to the heroku master branch.
```
git push heroku master
heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
heroku ps:scale web=1
heroku open
```
After open, you can see the website on the heroku.
### Developing Requirement
Attention: All codes committed should pass flake8 syntax check.

### Author
Frank
