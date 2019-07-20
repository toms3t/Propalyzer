# Propalyzer

[![Build Status](https://tomset.visualstudio.com/Propalyzer/_apis/build/status/toms3t.Propalyzer?branchName=master)](https://tomset.visualstudio.com/Propalyzer/_build/latest?definitionId=7&branchName=master)

Try it!   http://propalyzer.info

**Time to get up and running = less than 10 minutes**

Web app that helps investors evaluate investment property opportunities. The user inputs a US residential property address and the app uses Zillow's API to pull property details. The app presents the property details to the user for inspection and the ability to edit. With the details finalized, the app will crunch the data and return information about the property including:
- Operating Income
- Operating Expenses
- Cash on Cash Return
- Debt Coverage Ratio
- Monthly Cash Flow
- Scoring of area Livability, Crime, Cost of Living, Education, Employment, Housing, Weather relative to local and national averages
- Local natural disaster information
- Local school information

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites (MacOS and Linux Users)

- Install Python 3.6
```
https://www.python.org/downloads/
```
- Obtain a Zillow account and Zillow API Key (REQUIRED)
```
https://www.zillow.com/webservice/Registration.htm
```
- Obtain a GreatSchools API Key (NOT REQUIRED, BUT RECOMMENDED)
```
https://www.greatschools.org/api/request-api-key/
```

- Create and configure virtualenv 
```
$ mkdir Propalyzer
$ python3.6 -m pip install virtualenv
$ cd Propalyzer
$ python3.6 -m venv env
```
- Git dialed in! 
```
$ git init
$ git config --global user.name "Your Name"
$ git config --global user.email Your_email_address
$ git clone https://github.com/toms3t/Propalyzer.git
```
**The project includes a secret.py file to store API keys on your machine.
secret.py is referenced in the .gitignore file to prevent the secret.py file from being uploaded to GitHub by accident**

- Create a secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_app' folder and enter the following:
```
class Secret():
  ZWSID = '[enter your Zillow key here without brackets]'
  GSCHOOL_API_KEY = '[enter your GreatSchools key here without brackets]'
## now save the file ##
```
  
- Install packages from requirements.txt file

```
$ source env/bin/activate (run this from the directory with 'env' folder)
$ python -m pip install -r requirements.txt
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
Test that the site homepage appears when you browse to http://127.0.0.1:8000.

Log in with your superuser credentials

### Prerequisites (Windows Users)

- Install Miniconda
```
https://conda.io/miniconda.html
```
- Obtain a Zillow account and Zillow API Key (REQUIRED)
```
https://www.zillow.com/webservice/Registration.htm
```
- Obtain a GreatSchools API Key (NOT REQUIRED BUT RECOMMENDED)
```
https://www.greatschools.org/api/request-api-key/
```

- Create and configure virtualenv (Use Windows PowerShell, Command Prompt, or a Terminal Emulator such as ConEmu)
```
> Hit start and type "anaconda" to find the anaconda prompt -- launch the "anaconda prompt"
> mkdir Propalyzer
> cd Propalyzer
> conda create --name [virtual environment name]
> activate [virtual environment name]
```
- Git dialed in! 
```
> git init
> git config --global user.name "Your Name"
> git config --global user.email Your_email_address
> git clone https://github.com/toms3t/Propalyzer.git
```
- Install packages from requirements.txt file

```
> python3.6 -m pip install -r Propalyzer/requirements.txt
```
**The project includes a "secret.py" file to store API keys on your machine.
secret.py is referenced in the .gitignore file so don't worry about accidentally uploading your API keys**

- Create a secret.py file in the 'Propalyzer/propalyzer_site/propalyzer_app' folder and enter the following:
```
class Secret():
  ZWSID = '[enter your Zillow key here without brackets]'
  GSCHOOL_API_KEY = '[enter your GreatSchools key here without brackets]'
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
Test that the site homepage appears when you browse to http://127.0.0.1:8000.

Log in with your superuser credentials

## Deployment

http://propalyzer.info

## Built With

* [Django](http://www.djangoproject.com) - The web framework used

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Authors

* **Tom Setliffe** - [toms3t](https://github.com/toms3t)

See also the list of [contributors](https://github.com/toms3t/Propalyzer/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks [PurpleTooth](https://github.com/PurpleTooth) for the readme template!
* Zillow for their outstanding API
