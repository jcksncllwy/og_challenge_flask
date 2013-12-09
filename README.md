og_challenge_flask
==================

**[DEMO](http://fierce-river-3865.herokuapp.com/)**

This is a basic application for parsing csv transaction data from OpenGov and returning an aggregate annual report in JSON.

Setup
--------

1. Clone this repo
2. Install [virtualenv](https://pypi.python.org/pypi/virtualenv)
3. cd og_challenge_flask
4. virtualenv venv --distribute
5. ./venv/bin/pip install -r requirements.txt
6. ./venv/bin/python og_challenge_flask.py 
7. Open http://127.0.0.1:5000/
8. Upload [a csv file](https://www.dropbox.com/s/0s0q7uybmixltys/02_medium.csv)
9. ???
10. Profit

Details
---------

Python floats were used to parse incoming dollar values, but considering that accuracy is more important than performance where money is concerned, Decimal objects may have been more appropriate.

Additionally, the csv parsing system is not expected to be robust as it was only tested with a given sample file. Other csv formats may not behave as expected.
