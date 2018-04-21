# Back End

Back end of Surfing Penguin website

## Prerequisites

Python 3.6+ is required.
All packages needed are listed in requirements.txt.
You may use the following command to load them if you already have python 3.
```
pip install -r requirements.txt
```

## Setting Environment

```
export ENV = "Staging" or "Production" or you will use the DevelopmentConfig
export DATABASE_URL= "Your database url" or you will use sqlite as your database
```

## Running the Program

Under *src*, the following commands could help you start the server of the website.
```
export FLASK_APP=surfing_penguin.py
flask run
```

You should see the following content if it runs correctly.
```
 * Serving Flask app "surfing_penguin"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Deploying on Heroku

Here, we will teach you how to use Heroku Cli to deploy the website.

1. First, create a heroku app and then connect it.
```
heroku create  --buildpack heroku/python
heroku git:remote -a "Your app name"
```

2. If you want to create a postgresql database, the following command can help you.
```
heroku addons:create heroku-postgresql:hobby-dev
```

3. You should create a .env file including the following content.
```
DATABASE_URL="Your database url" or you will use sqlite as your database
ENV="Staging" or "Production" or you will use the DevelopmentConfig
(DATABASE_URL could be got using ` heroku config:get DATABASE_URL -a "Your app name" `)
```

4. Push it to the heroku master branch.
```
git push heroku <branch-to-deploy>:master
heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
heroku ps:scale web=1
heroku open
```

5. After open, you can see the website on the heroku.

## Author

Frank [zfrank7777](https://github.com/zfrank7777)

[gameow1124](https://github.com/gameow1124)

Allen [amjltc295](https://github.com/amjltc295)
