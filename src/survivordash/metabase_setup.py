import requests
import pandas as pd
import json
import os
import sys

def get_setup_token():
    response = requests.get('http://metabase:3000/api/session/properties')
    return response.json()['setup-token']


def setup_metabase_session(token):

    setup_params = {
        'token': token,
        'user':{
            'email': 'test@local.host',
            'first_name': 'Mister',
            'last_name': 'Foo',
            'password': 'fakepass1',
        },
        "database": {
            'name': 'mydatabase',
        },
        "prefs": {
            'site_name': 'mysitename',
        }
    }

    # TODO: on our initial setup. this request shoudl return our session_id
    # So we should implment logic to use this sessionid and reduce redundancy
    # For now we can just just get the session we created, this can make our function idempotent
    res = requests.post('http://metabase:3000/api/setup', json=setup_params)

    # get session
    response = requests.post('http://metabase:3000/api/session',
                            json={'username': setup_params['user']['email'],
                                'password': setup_params['user']['password']})

    session_id = response.json()['id']
    return session_id


def add_source(headers):
    # add source
    source_params = {
        'name': os.environ['POSTGRES_DB'],
        'engine': 'postgres',
        "details": {
            "host": os.environ['POSTGRES_HOST'],
            "port": os.environ['POSTGRES_PORT'],
            "db": os.environ['POSTGRES_DB'],
            "user": os.environ['POSTGRES_USER'],
            "password": os.environ['POSTGRES_PASSWORD'],
        }
    }

    requests.post('http://metabase:3000/api/database', headers=headers, json=source_params)

def add_data_to_metabase():
    setup_token = get_setup_token()
    session_id = setup_metabase_session(setup_token)
    headers = {'X-Metabase-Session': session_id}
    add_source(headers)
    

def run():
    add_data_to_metabase()
    print("Metabase populated.")

if __name__ == '__main__':
    run()