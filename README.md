# Webhook Catchall
A simple HTTP service based on Django that was built to catch and show webhook data in a testing environment.
Includes a Django admin page what shows the url that was hit, and the data that was received.

**THIS IS FOR DEVELOPMENT PURPOSES ONLY IT IS NOT RECOMMENDED FOR PRODUCTION USE**

## Requirements
 - A Postgres Database.
 - Python 3.8+ or Docker

## Installation

There are 2 ways to use this:
1. Use the Docker image (easiest)
2. Run this as a local Python service using the built in Django server

### Docker Service
The latest docker image is available at my docker hub. [You can find it here]()

#### Options
The image provides options to change the database settings via environment variables
so that you can adjust to fit your system. The variables are:
 - `DB_NAME`: The name of the database (e.g., `webhook_catchall`)
 - `DB_USER`: The username of the database (e.g., `postgres`)
 - `DB_PASS`: The password of the database (e.g., `postgres`)
 - `DB_HOST`: The host of the database (e.g., `127.0.0.1`)
 - `DB_PORT`: The port of the database (e.g., `5432`)

You can also change the default admin username and password as well. To do so simply pass in the
environment params of `ADMIN_USER` and `ADMIN_PASS` (defaults to `admin`:`admin`)

##### Demo docker-compose.yml
Included in the project is an example `docker-compose.yml` that will bring up the project
with a postgres database and have it running on port 8181. You can then simply point your
webhooks to `http://localhost:8181/`, and your browser to `http://localhost:8181/admin/` to login
with the default admin to see what was captured.


### Local Django server
You can of course run this locally using Django's build in test server. Please don't
forget to update parameters here with those of your system and choosing.

1. Clone this repo.
2. Create a local Python virtual environment and activate it (e.g., `python -m venv ./.venv && source ./.venv/bin/activate`)
3. Install the requirements using pip (e.g., `pip install -r requirements.txt`)
4. Create a file called `.env` in the project root (this file is git ignored FYI)
5. Copy this code block and replace it with the settings from your database setup:
   ```bash
   DB_NAME=webhook_catchall
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```
6. Run the Django migrations: `python manage.py migrate`
7. Run Django's static collection: `python manage.py collectstatic`
8. Run the `create_default_superuser` management command to create the admin user:
   `python manage.py create_default_superuser --username="admin" --password="admin"`
9. Run the Django testserver: `python manage.py testserver 127.0.0.2:8181` to start the server.
10. Open your browser to `http://localhost:8181/admin/` and login to the admin.

## Usage
Once you have the service up and running, it will support receiving data from any HTTP method on
any path (except those being with `/admin/` or `/static/`). The system will dump all data into a
`TEXT` field and additionally attempts to store the incoming data that has the `Content-Type`
header of `application/json` into a JSON field for easy viewing. It also will keep track of the
method used, the time the webhook was received, the incoming path, any query parameters as well as
any headers in the request. The service will always save the data no matter what and return a 204
response (no content) unless it fails to decode the json, in which case it will return a 400
instead with the error from the json decoder and the data only stored in the `TEXT` field.

### Example:
`curl -X POST http://127.0.0.1:8181/foo/bar?process=webhook -H "Content-Type: application/json" -d "{\"test\":{\"data\": \"nested\"}}"`

You can login to the Django Admin and see all the details of the call. The view of the data in the
admin is read-only.


## Help and support
If you need help or find a bug or would like to ask for a feature (you could build it, see
contributing below). Please first search to see if the issue exists on the github page. If not,
please open a new ticket and explain in as much detail as possible how to recreate the issue or
what feature you'd like to see.

## Contributing and development
This is an opensource project, contributions are welcome. Please follow the guidelines to
contribute to this project.

### Setup
1. Use `pip` to install the additional `dev-requirements.txt`.

### Coding standards
Before submitting any code please be sure you have done the following:
- Run coding stands tools, these are isort, black and flake8. They should all pass.
- Run tox and check all tests have passed and that your code coverage is 95% or above.

### Testing
Every bit of code you submit must be fully tested.
All testing is done using pytest, please follow pytest style testing (not unittest).
You can simply use tox to run the tests: `tox -e py39`. This supports environments
`py36` - `py39`.
