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
export ADMIN_NAME = "Your admin name"
export ADMIN_PASSWORD = "Your admin password"
```

## Running the Program

Under *src*, the following commands could help you start the server of the website.
```
python manage.py deploy
python manage.py init_admin
export FLASK_APP=surfing_penguin.py
flask run
```

You should see the following content if it runs correctly.
```
 * Serving Flask app "surfing_penguin"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Running unit tests

Under *src*:
```
pytest
```

## Automatically deploy with Travis CI and Heroku

Here, we will teach you how to automatically deploy the website with Travis CI
and Heroku.

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
(You could get DATABASE_URL by ` heroku config:get DATABASE_URL -a "Your app name" `)
```
DATABASE_URL="Your database url" or you will use sqlite as your database
ENV="Staging" or "Production" or you will use the DevelopmentConfig
```
4. Create an account on Travis CI and link it with your repository
```
To do that you can go to https://travis-ci.org/, to make it easier create your account using your Github.

You will see the Authorize Screen telling to accept and link Travis CI with your Github account.
```
5. Set it to the heroku master branch.
```
Go to Heroku website.
At Deploy tab on the “Automatic deploys” section don't forget to check the "Wait for CI to pass before deploy" option and enable the Automatic Deploys:
```
6. After setting, it will automatically deploy the website with Travis CI
and Heroku. And you can see the website on the heroku.
```
Preference: https://medium.com/@felipeluizsoares/automatically-deploy-with-travis-ci-and-heroku-ddba1361647f
```
## Author

* Frank [zfrank7777](https://github.com/zfrank7777)

* [gameow1124](https://github.com/gameow1124)

* Allen [amjltc295](https://github.com/amjltc295)
