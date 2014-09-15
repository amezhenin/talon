Project deployed here: http://polar-reef-1243.herokuapp.com/

The requirements for the test project are:
===============================

Could you write me a todo list management web application where:
  + I can have my todo list displayed.
  + I can manipulate my list (add/remove/modify entries).
  + Assign priorities and due dates to the entries.
  + I can sort my entry lists using due date and priority.
  + I can mark an entry as completed.
  + Minimal UI/UX design is needed.
  + I need every client operation done using JavaScript, reloading the
page is not an option.
  - Write a RESTful API which will allow a third-party application to
trigger actions on your app (same actions available on the webpage).
  - You need to be able to pass credentials to both the webpage and the API.
  + As complementary to the last item, one should be able to create
users in the system via an interface, probably a signup/register
screen.


TODO
====
* OAuth and other for API
* factory-boy -- write tests for registration
* fabric file with deployments
* include coverage report in docs
* write down all API call that is needed by usecases


DOCS
====

## Deploy

You can deploy this application with console command:

    fab deploy

## Tests

python manage.py test

### Coverage

coverage run manage.py test
coverage report
coverage html
