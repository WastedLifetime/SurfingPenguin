# Back End
This code provide the simple structure of Surfing Penguin website.

### Prerequisites
Python 3 is required.
All packages needed are listed in requirements.txt.
You may use the following command to load them if you already have python 3.
```
pip install -r requirements.txt
```

### Running the Program
Under src, the following commands help you start the server of the website.
```
export FLASK_APP=surfing_penguin.py
(export ENV == "Staging" or "Production")
(export DATABASE_URL= "Your local database url" )
flask run
```

You should see the following content if it runs correctly.
```
 * Serving Flask app "surfing_penguin"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Some api for developers has been added, check them out in route.py.
The HTML templates are to represent the view of administrators.

### Developing Requirement
Attention: All codes committed should pass flake8 syntax check.

### Author
Frank
