"""
Usage: janus [--debug] add LABEL [--tag=TAG]... [--link=URI] [--username=USERNAME] --password=PASSWORD
       janus [--debug] delete LABEL
       janus [--debug] init
       janus [--debug] list (labels|tags)
       janus [--debug] set LABEL [--tag=TAG]... [--link=URI] [--username=USERNAME] --password=PASSWORD
       janus [--debug] show LABEL
       janus [--debug] tag LABEL TAG...
       janus -h | --help
       janus --version

Options:
       -d, --debug                  Display state throughout execution
       -l, --link=URI               Include URI in record
       -p, --password=PASSWORD      Provide password for record
       -t, --tag=TAG...             Associate record with tags
       -u, --username=USERNAME      Include username in record
"""

from cryptography.fernet import Fernet
from docopt import docopt
import os, yaml

# This function assumes that datastore[label]['tags']
# contains a list; this may not be the case.
def get_tags():
    tag_list = []
    for label in datastore:
        for tag in datastore[label]['tags']:
            if not tag in tag_list:
                tag_list.append(tag)
    tag_list.sort()
    return tag_list

def janus_add():
    if cli_args['LABEL'] in datastore:
        pass # ERROR
    else:
        label = cli_args['LABEL']
        datastore[label] = {}
        if cli_args['--tag']:
            tags = cli_args['--tag']
            datastore[label]['tags'] = tags
        if cli_args['--link']:
            datastore[label]['uri'] = cli_args['--link']
        if cli_args['--username']:
            datastore[label]['username'] = cli_args['--username']
        datastore[label]['password'] = cli_args['--password']

def janus_delete():
    if not cli_args['LABEL'] in datastore:
        pass # ERROR
    else:
        label = cli_args['LABEL']
        del datastore[label]

def janus_init():
    pass

def janus_list():
    if cli_args['labels']:
        for label in datastore:
            print label
    if cli_args['tags']:
        tags = get_tags()
        for tag in tags:
            print tag

def janus_show():
    if not cli_args['LABEL'] in datastore:
        pass # ERROR
    else:
        label = cli_args['LABEL']
        print datastore[label]

def janus_tag():
    if not cli_args['LABEL'] in datastore:
        pass # ERROR
    else:
        label = cli_args['LABEL']
        for tag in cli_args['--tag']:
            if tag not in datastore[label]['tags']:
                datastore[label]['tags'].append(tag)
            datastore['tags'].sort()

def open_datastore(cipher):
    in_file = open('encrypted_file', 'r')
    ciphertext = in_file.read()
    in_file.close()
    plaintext = cipher.decrypt(ciphertext)
    if cli_args['--debug']:
        print 'YAML plaintext, pre-execution:'
        print plaintext
    datastore = yaml.load(plaintext)
    if cli_args['--debug']:
        print 'YAML dictionary, pre-execution:'
        print datastore
    return datastore

def close_datastore(cipher):
    if cli_args['--debug']:
        print 'YAML dictionary, post-execution:'
        print datastore
    plaintext = yaml.dump(datastore)
    if cli_args['--debug']:
        print 'YAML plaintext, post-execution:'
        print plaintext
    ciphertext = cipher.encrypt(plaintext)
    out_file = open('encrypted_file', 'w')
    out_file.truncate()
    out_file.write(ciphertext)
    out_file.close

if __name__ == '__main__':
    cli_args = docopt(__doc__, version='janus v0.0.1')
    if cli_args['--debug']:
        print cli_args
    key = os.environ['JANUS_KEY']
    cipher = Fernet(key)
    datastore = open_datastore(cipher)
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
    if cli_args['tag']:
        janus_tag()
    close_datastore(cipher)
