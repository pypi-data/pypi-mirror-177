import requests as rq
import json

url = "https://www.1secmail.com/api/v1/"


def get_random_mail(count=1):
    mails = rq.get(url, params={'action': 'genRandomMailbox', 'count': count}).json()

    return mails


def get_domain_list():
    return rq.get(url, params={'action': 'getDomainList'}).json()


class Mail:
    def __init__(self, mail=None):
        domains = get_domain_list()
        if not mail:
            mail = get_random_mail()[0]
        elif '@' not in mail:
            mail += '@' + domains[0]
        elif mail.split('@')[-1] not in domains:
            mail = mail.split('@')[0] + '@' + domains[0]

        self.mail = mail

    def check(self, domain, user):
        return rq.get(url, params={'action': 'getMessages', 'login': user, 'domain': domain}).json()

    def get_letter(self, let_id):
        mail = self.mail
        login, domain = mail.split('@')
        return rq.get(url, params={'action': 'readMessage', 'login': login, 'domain': domain, 'id': let_id}).json()

    def __str__(self):
        return self.mail
