from bs4 import BeautifulSoup as bs, element
import http.cookiejar as cookiejar
from mechanize import Browser
import json
from datetime import datetime, timedelta
import argparse
from tqdm import tqdm
from tinydb import TinyDB, Query
from utility.files import create_if_not_exist, create_dir_if_not_exist

# URLs
LOGIN_URL = 'https://ugvle.ucsc.cmb.ac.lk/login/index.php'
CALENDER_URL = 'https://ugvle.ucsc.cmb.ac.lk/calendar/view.php?view=day&course=1&time='

cj = cookiejar.CookieJar()
br = Browser()
br.set_cookiejar(cj)

db = None


def login_get_index(username, password):
    br.open(LOGIN_URL)

    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()

    return br.response().read()


def get_course_list(index_bs):
    course_list_wrapper = index_bs.select(".block_course_list")

    def get_course_list_item(item):
        return list(item.children)[0].attrs

    return list(map(get_course_list_item, course_list_wrapper[0].select(".column")))


def get_assignments(date):
    br.open(CALENDER_URL + str(int(date.timestamp())))

    calender_bs = bs(br.response().read(), features="html5lib")
    main_bs = calender_bs.select(".maincalendar")[0]
    events_bs = main_bs.select(".event")

    assignments = []
    for event in events_bs:
        box_bs = event.select(".box")[0]

        url = list(box_bs.select(".referer")[0].children)[0].attrs['href']
        event_id = url.split("=")[1]
        title = list(box_bs.select(".referer")[0].children)[0].contents[0]
        time = list(box_bs.select(".date")[0].children)[0]
        if type(time) is not element.NavigableString:
            time = time.contents[0]
        course = list(box_bs.select(".course")[0].children)[0].contents[0]
        des = list(event.select(".description"))
        if len(des) > 0:
            des = str(''.join(list(map(lambda x: str(x), des[0].contents))))
        else:
            des = ""

        assignments.append({
            'id': event_id,
            'title': title,
            'course': course,
            'url': url,
            'description': des,
            'time': str(time),
            'date': str(date).split(" ")[0],
            'synced': False
        })

    return assignments


def main():
    parser = argparse.ArgumentParser(description='Scrape UGVLE assignments.')
    parser.add_argument('username', type=str, help='UGVLE username')
    parser.add_argument('password', type=str, help='UGVLE password')
    parser.add_argument('-d', '--days', type=int,
                        help='Count of days to be scraped', default=30)
    parser.add_argument('-s', '--store', type=str,
                        help='Data store directory', default='data')

    args = parser.parse_args()

    username = args.username
    password = args.password
    days = args.days
    store = args.store

    print("Initiallizing store")
    store_path = store + "/assignments.json"
    create_dir_if_not_exist(store)
    create_if_not_exist(store_path, data={})

    global db
    db = TinyDB(store_path)
    print("No. assignments in store:", len(db), '\n')

    print("Fetching assignments for", days, "days\n")
    print("Logging into UGVLE\n")
    login_get_index(username, password)

    def init_day(date):
        return datetime(date.year, date.month, date.day)

    def increment_day(date):
        date += timedelta(days=1)
        return date

    print("Collecting assignments")
    assignments = []
    day = init_day(datetime.now())
    for _ in tqdm(range(days)):
        assignments.extend(get_assignments(day))
        day = increment_day(day)

    print("\nStoring assignments")
    added_count = 0

    Assignment = Query()
    for assignment in tqdm(assignments):
        existing = db.get(Assignment.id == assignment['id'])
        if not existing:
            db.insert(assignment)
            added_count += 1

    print("\nAdded", added_count, "documents\n")

    print("Scraping finished")


if __name__ == "__main__":
    main()
