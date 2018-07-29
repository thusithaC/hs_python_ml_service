# Transactions Prediction service 

Based on a template using Django/python 
https://github.com/heroku/python-getting-started

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pipenv install

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
This is deployed in https://pure-bastion-26477.herokuapp.com

Example usage :
```python
# learning and prediction example. 

ML_URL = 'https://pure-bastion-26477.herokuapp.com'
TRAIN_URL = ML_URL + '/services/traingeneric'
TEST_URL = ML_URL + '/services/predgeneric'

if 1: 
    r = sendGet(train_url, None)
    if r.status_code == 200:
        print("Training Successfull")
    else:
        print("Error! is the services up?")

if 1: 
    test_data = '[{"transaction": {"transactionDay":800, "category": "AA"}}, {"transaction": {"transactionDay":850, "category": "GG"}}]'
    test_data_json = json.loads(test_data)
    r = sendPostJson(TEST_URL, test_data_json)
    jprint(r)
```
