# soundoftext-python
Sound of Text, written in Python, using Flask.

# Build Instructions

## Clone Repo

    $ git clone https://github.com/ncpierson/soundoftext-python.git
    $ cd soundoftext-python

## Install Dependencies

Using Virtualenv:

    $ virtualenv ./

Without Virtualenv:

    $ sudo pip install -r requirements.txt

## Set up database

    $ sqlite3 sounds.db < schema.sql

## Run it

    $ python soundoftext.py
