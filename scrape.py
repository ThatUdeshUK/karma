from bs4 import BeautifulSoup as bs, element
import http.cookiejar as cookiejar
import mechanize
import json
from datetime import datetime, timedelta

# URLs 
LOGIN_URL = 'https://ugvle.ucsc.cmb.ac.lk/login/index.php'
CALENDER_URL = 'https://ugvle.ucsc.cmb.ac.lk/calendar/view.php?view=day&course=1&time='

cj = cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

def login_get_index():
    br.open(LOGIN_URL)

    br.select_form(nr=0)
    br.form['username'] = '2017cs091'
    br.form['password'] = 'uc*cCE0980uk'
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
            'date': str(date).split(" ")[0]
        })

    return assignments


def main():
    # index_bs = bs(login_get_index(), features="html5lib")
    # course_list = get_course_list(index_bs)
    # print(json.dumps(course_list, indent=4))

    login_get_index()

    def init_day(date):
        return datetime(date.year, date.month, date.day)

    def increment_day(date):
        date += timedelta(days=1)
        return date

    assignments = []
    day = init_day(datetime.now())
    for _ in range(30):
        assignments.extend(get_assignments(day))
        day = increment_day(day)

    print(json.dumps(assignments, indent=4))
    print(len(assignments))


if __name__=="__main__":
    main() 