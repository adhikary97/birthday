import time
import util
import re
import applescript
import datetime
import subprocess
from icalevents.icalevents import events


def get_phone_num(name):
    r = applescript.tell.app('Address Book', f'get the value of phone of the first person whose name is "{name}"')
    return r.out


def get_names():
    pattern = r'([A-Za-z]+)\sBirthday'
    people = list()
    es = events(util.calUrl, fix_apple=True, end=(datetime.datetime.now() + datetime.timedelta(30)))
    for i in es:
        match = re.match(pattern, i.summary)
        if match:
            people.append((i.start.replace(tzinfo=None), match[1]))
    return people


def clean_phone(num):
    num = num.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+1', '').strip()
    num = num.split(',')[0]
    return num


def send_message(num, message):
    subprocess.call('bash runner.bash %s %s' % (f'{num}', f'"{message}"'), shell=True)


if __name__ == '__main__':
    while True:
        names = get_names()
        for ind, val in enumerate(names):
            if val[0].date() == datetime.datetime.today().replace(tzinfo=None).date():
                phone = clean_phone(get_phone_num(val[1]))
                print("texting...", phone)
                send_message(phone, "Happy Birthday!")
                names.remove(val)
        time.sleep(86400)
