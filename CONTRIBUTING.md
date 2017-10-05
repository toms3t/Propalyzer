### Prerequisites

- Install Python 3.6.2
```
https://www.python.org/downloads/
```
- Obtain a Zillow account and Zillow API Key (ZWS-ID)
```
https://www.zillow.com/webservice/Registration.htm
```

- Create and configure virtualenv 
```
$ mkdir [directory name]
$ pip install virtualenv
$ cd [directory name]
$ virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 env
```
- Git dialed in! 
```
$ git init
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
$ git clone https://github.com/toms3t/Propinator.git
```
- Install packages from requirements.txt file

```
$ source env/bin/activate (run this from the directory you created to activate the virtual environment)
$ pip install -r Propinator/requirements.txt
```
- Enter secret key in your /Users/[your username]/[directory name]/propinator_site/propinator_site/settings.py file
```
secret_key = '[enter new key here without the brackets - you can make the key whatever you want]'
[save settings.py file]
```
- Enter your ZWSID into the '/Users/[username]/[directory name]/propinator_site/propinator_app/views.py' file
```
ZWSID = '[enter your key here without brackets]'
```

- Prep the SQLite database
```
$ cd Propinator/propinator_site
$ python manage.py makemigrations propinator_app
$ python manage.py migrate
```

- Run local webserver and test the home page
```
$ python manage.py runserver
```
Test that the site homepage appears when you browse to http://127.0.0.1:8000/propinator

## Deployment

This web app uses a SQLite database which is installed by Django by default.

## Built With

* [Django](http://www.djangoproject.com) - The web framework used

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
