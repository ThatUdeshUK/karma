from bs4 import BeautifulSoup as bs
import http.cookiejar as cookiejar
import mechanize
import json

# URLs 
LOGIN_URL = 'https://ugvle.ucsc.cmb.ac.lk/login/index.php'

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


def main():
    index_bs = bs(login_get_index(), features="html5lib")

    course_list = get_course_list(index_bs)
    print(json.dumps(course_list, indent=4))


if __name__=="__main__":
    main() 