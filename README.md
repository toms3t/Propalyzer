# Propalyzer

Web app that helps investors evaluate investment property opportunities. The user inputs a US residential property address and the app uses Zillow's API to pull property details. The app presents the property details to the user for inspection and the ability to edit. With the details finalized, the app will crunch the data and return information about the property including:
- Operating Income
- Operating Expenses
- Cash on Cash Return
- Debt Coverage Ratio
- Monthly Cash Flow
- Scoring of area Livability, Crime, Cost of Living, Education, Employment, Housing, Weather relative to local and national averages

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites (MacOS and Linux Users)

- Install Python 3.6.2
```
https://www.python.org/downloads/
```
- Obtain a Zillow account and Zillow API Key (ZWS-ID)
```
https://www.zillow.com/webservice/Registration.htm
```
- Obtain a Google MAPs API Key. Go to the site below and click 'GET A KEY' at the top
```
https://developers.google.com/maps/documentation/geocoding/start
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
$ git clone https://github.com/toms3t/Propalyzer.git
```
- Create a secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_app' folder and enter the following:
```
class Secret():
  ZWSID = '[enter your Zillow key here without brackets]'
  GMAPS_API_KEY = '[enter your Google Maps API key here without brackets]'
## now save the file ##
```
- Create a second secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_site' folder and enter the following:
```
class Secret():
  SECRET_KEY = '[enter a secret key here without brackets]'
## now save the file ##
```
- Install packages from requirements.txt file

```
$ source env/bin/activate (run this from the directory you created to activate the virtual environment)
$ pip install -r Propalyzer/requirements.txt
```
- Prep the SQLite database
```
$ cd Propalyzer/propalyzer_site
$ python manage.py makemigrations propalyzer_app
$ python manage.py migrate
```
- Create superuser
```
$ python manage.py createsuperuser
```

- Run local webserver and test the home page
```
$ python manage.py runserver
```
Test that the site homepage appears when you browse to http://127.0.0.1:8000/propalyzer.

Log in with your superuser credentials

### Prerequisites (Windows Users)

- Install Miniconda
```
https://conda.io/miniconda.html
```
- Obtain a Zillow account and Zillow API Key (ZWS-ID)
```
https://www.zillow.com/webservice/Registration.htm
```

- Create and configure virtualenv (Use Windows PowerShell, Command Prompt, or a Terminal Emulator such as ConEmu)
```
> mkdir [directory name]
> cd [directory name]
> conda create --name [virtual environment name]
> activate [virtual environment name]
```
- Git dialed in! 
```
> git init
> git config --global user.name "John Doe"
> git config --global user.email johndoe@example.com
> git clone https://github.com/toms3t/Propalyzer.git
```
- Install packages from requirements.txt file

```
> pip install -r Propalyzer/requirements.txt
```
- Create a secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_app' folder and enter the following:
```
class Secret():
  ZWSID = '[enter your Zillow key here without brackets]'
  GMAPS_API_KEY = '[enter your Google Maps API key here without brackets]'
## now save the file ##
```
- Create a second secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_site' folder and enter the following:
```
class Secret():
  SECRET_KEY = '[enter a secret key here without brackets]'
## now save the file ##
```

- Prep the SQLite database
```
> cd Propalyzer/propalyzer_site
> python manage.py makemigrations propalyzer_app
> python manage.py migrate
```
- Create superuser
```
> python manage.py createsuperuser
```

- Run local webserver and test the home page
```
> python manage.py runserver
```
Test that the site homepage appears when you browse to http://127.0.0.1:8000/propalyzer.

Log in with your superuser credentials

## Deployment

Not yet deployed in a live environment.

## Built With

* [Django](http://www.djangoproject.com) - The web framework used

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Authors

* **Tom Setliffe** - *Initial work* - [toms3t](https://github.com/toms3t)

See also the list of [contributors](https://github.com/toms3t/Propalyzer/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks [PurpleTooth](https://github.com/PurpleTooth) for the readme template!
* Zillow for their outstanding API
 