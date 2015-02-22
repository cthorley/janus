"""
Usage: janus add LABEL [--tags=<TAG>...] [--uri=<URI>] [--username=<USERNAME>] --password=<PASSWORD>
       janus delete LABEL
       janus init
       janus list (labels|tags)
       janus show LABEL
       janus -h | --help
       janus --version
"""

from cryptography.fernet import Fernet
from docopt import docopt
import yaml

def janus_add():
    if cli_args['LABEL'] in datastore:
        pass # ERROR
    else:
        label = cli_args['LABEL']
        datastore[label] = {}
        if cli_args['--tags']:
            datastore[label]['tags'] = cli_args['--tags']
        if cli_args['--uri']:
            datastore[label]['uri'] = cli_args['--uri']
        if cli_args['--username']:
            datastore[label]['username'] = cli_args['--username']
        datastore[label]['password'] = cli_args['--password']

def janus_delete():
    if cli_args['LABEL'] in datastore:
        del datastore[LABEL]
    else:
        pass # ERROR

def janus_init():
    pass

def janus_list():
    if cli_args['labels']:
        for label in datastore:
            print label
    if cli_args['tags']:
        pass # do interesting things

def janus_show():
    label =  cli_args['LABEL']
    if not datastore[label]:
        pass # ERROR
    else:
        print datastore[label]

def open_datastore(cypher):
    in_file = open('encrypted_file', 'r')
    cyphertext = in_file.read()
    plaintext = cypher.decrypt(cyphertext)
    datastore = yaml.load(plaintext)
    in_file.close()
    return datastore

def close_datastore(cypher):
    plaintext = yaml.dump(datastore)
    cyphertext = cypher.encrypt(plaintext)
    out_file = open('encrypted_file', 'w')
    out_file.truncate()
    out_file.write(cyphertext)
    out_file.close

if __name__ == '__main__':
    cli_args = docopt(__doc__, version='janus v0.0.1')
    key = 'jlIEOZJiMsnxNOX8Dd7pybilwwFo2q7QrcBcFotgwXU='
    cypher = Fernet(key)
    datastore = open_datastore(cypher)
    #print datastore
    if cli_args['add']:
        janus_add()
    if cli_args['delete']:
        janus_delete()
    if cli_args['init']:
        janus_init()
    if cli_args['list']:
        janus_list()
    if cli_args['show']:
        janus_show()
    close_datastore(cypher)
