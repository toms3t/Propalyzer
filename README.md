# Propalyzer

![Build Status](https://github.com/toms3t/Propalyzer/actions/workflows/new_data_source_propalyzer-new.yml/badge.svg)

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

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Requesting a See deployment for notes on how to deploy the project on a live system.

### Prerequisites (MacOS and Linux Users)

- Install Python 3.8
```
https://www.python.org/downloads/
```

- Create and configure virtualenv 
```
$ mkdir Propalyzer
$ python3.8 -m pip install virtualenv
$ cd Propalyzer
$ python3.8 -m venv env
```

- Configure a secret key environment variable in your Linux/Mac environment. Alternatively, you could just set a new value for "SECRET_KEY" in the settings.py file.
```
$ export SECRET_KEY='add_a_unique_string_of_characters'
```

- Git dialed in! 
```
$ git init
$ git config --global user.name "Your Name"
$ git config --global user.email Your_email_address
$ git clone https://github.com/toms3t/Propalyzer.git
```
  
- Install packages from requirements.txt file

```
$ source env/bin/activate (run this from the directory with 'env' folder)
$ python -m pip install -r requirements.txt
```
- Prep the SQLite database
```
$ cd Propalyzer/propalyzer_site
$ python manage.py migrate
```
- Create superuser
```
$ python manage.py createsuperuser
```

- To run the local server, type the command below from the same directory as your "manage.py" file ("python manage.py runserver" is disabled to let Gunicorn handle static file collection)
```
> gunicorn wsgi
```
Test that the site homepage appears when you browse to http://127.0.0.1:8000.

### Prerequisites (Windows Users)

- Install Miniconda
```
https://conda.io/miniconda.html
```

- Create and configure virtualenv (Use Windows PowerShell, Command Prompt, or a Terminal Emulator such as ConEmu)
```
> Hit start and type "anaconda" to find the anaconda prompt -- launch the "anaconda prompt"
> mkdir Propalyzer
> cd Propalyzer
> conda create --name [virtual environment name]
> activate [virtual environment name]
```
- Configure a secret key environment variable in your Windows environment (refer to this link - https://www3.ntu.edu.sg/home/ehchua/programming/howto/Environment_Variables.html)
```
Call it "SECRET_KEY"
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
> python3.8 -m pip install -r Propalyzer/requirements.txt
```
- Prep the SQLite database
```
> cd Propalyzer/propalyzer_site
> python manage.py migrate
```
- Create superuser
```
> python manage.py createsuperuser
```
- To run the local server, type the command below from the same directory as your "manage.py" file ("python manage.py runserver" is disabled to let Gunicorn handle static file collection)
```
> gunicorn wsgi
```
Test that the site homepage appears when you browse to http://127.0.0.1:8000.

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
