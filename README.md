# Django Survey App ⚡

This django web application allows an admin user to create survey questions with multiple choice answers. When a guest user visits the application  it present a random survey question which the user can answer it record answers and display the survey results in an admin interface. It also avoid showing a previously answered question to the same guest once the user is done he can do another round
if he wants to

## Requirements

1. [python 3.5.x](https://www.python.org/) or higher with [pip](https://pypi.org/project/pip/)
2. Whatever you prefer to manage your python dependencies [VirtualEnv](https://docs.python.org/3/tutorial/venv.html), [Pipenv](https://docs.pipenv.org/en/latest/), [Conda](https://docs.conda.io/en/latest/) or anything that alllows you to use `pip install`
3. **Optional** if you want to use MySQL over sqlite3 you will need to install [MySQL 5.6 or higer](https://dev.mysql.com/downloads/mysql/) and it's required drivers according to your OS

## Setup

1. Create your virtual enviroment for this I will use `Conda` but feel free to use whatever your prefer

    ```bash
    conda create --name surveyenv pip python=3.7
    ```

2. Activate your virtual environment

    ```bash
    activate surveyenv
    ```

3. With your virtual environment active navigate to the root of the project where the `manage.py` and `requirements.txt` files are located and execute:

    ```bash
    pip install -r requirements.txt
    ```

## Add local configuration

Note: You must run the following commands from the root of your project

1. Create your `local_settings.py` file from template

    ```bash
    cp django_survey_app/local_settings.py.template django_survey_app/local_settings.py
    ```

2. Open `local_settings.py` and uncomment the database block corresponding to the database server you will use

3. **Optional** If you will use mySQL create your `my.cnf` file from template

    ```bash
    cp my.cnf.template my.cnf
    ```

    Open the `my.cnf` and add your database connection string data

    **Important**: Remember to manually create the Database on mySQL Server

## Running the project

Note: For the following commands you must have already configured your database settings and make sure you have your virtual environment activated. You must also be located on the root of the project

1. Run migrations

    ```sh
    python manage.py migrate
    ```

    **Note** If using mySQL you run into `Incorrect string value` make sure you set charset of your mySQL db to `utf8mb4` it should be the default for newer version

2. Create super user

    ```sh
    python manage.py createsuperuser
    ```

3. Run the server

    ```sh
    python manage.py runserver
    ```

4. You should now be able to navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and start answering some questions as the migrations contains initial data or go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and enter your superuser data to check the answers or add more questions

## Running tests

From the root of the project with your virtual environment active run

```sh
python manage.py test
```

## Running linting

This project uses flake8 as a linter you can check the config on the `setup.cfg`  in order to run it make sure your virtual environment is active and from the root of the project run

```sh
flake8
```

If no output you are 👌. It is recommended that you configure your editor to use flake8.


Have fun 🎉
