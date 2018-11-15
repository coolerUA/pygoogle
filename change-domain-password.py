from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string
from random import *
import datetime


def genpas():
    # characters = string.ascii_letters + string.punctuation + string.digits
    characters = string.ascii_letters + string.digits
    password = "".join(choice(characters) for x in range(randint(16, 16)))
    return password


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'


def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        # flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('admin', 'directory_v1', http=creds.authorize(Http()))

    # Call the Admin SDK Directory API
    # print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=50, orderBy='email').execute()
    users = results.get('users', [])

    creds = {}

    if not users:
        print('No users in the domain.')
    else:
        # print('Users:')
        for user in users:
            password = genpas()
            body = {"password" : password}
            service.users().update(userKey=user['primaryEmail'], body=body).execute()
            creds[user['primaryEmail']] = password
            # print(u'{0} ({1}) [{2}]'.format(user['primaryEmail'], user['name']['fullName'],password))

    # print(creds)
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    log = './save/' + filename + '.txt'
    with open(log, 'w') as f:
        f.write(str(creds))


if __name__ == '__main__':
    main()
