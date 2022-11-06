# KhoshHal

KhoshHal is a place for seeking online medical advice. You can register as a doctor, and our admins will verify that ASAP! you can also look for your counselor, rate those you had an appointment with and favorite your counselors of choice. You can also comment on the counselor's page which you've had at least one appointment with.

## Team Members

- Hamila Mailee
- Mehraneh Najafi
- Rosta Roghani

## Run the project


1. Generate the SQL commands for preinstalled apps:

```sh
$ python manage.py makemigrations
```

2. Execute those SQL commands in the database file:

```sh
$ python manage.py migrate
```

3. Create an admin:

```sh
$ python manage.py createsuperuser
```

4. Run the server:

```sh
$ python manage.py runserver
```

5. Open your browser and go to [localhost](http://127.0.0.1:8000).

6. Enjoy!
