import re
from datetime import date, datetime, timedelta

from requests import Session


class Onboard:
    '''Implementation of manual requests to get a planning from OnBoard'''

    URL_LOGIN_PAGE = 'https://onboard.ec-nantes.fr/faces/Login.xhtml'
    URL_POST_LOGIN = 'https://onboard.ec-nantes.fr/login'
    URL_MENU = 'https://onboard.ec-nantes.fr/faces/MainMenuPage.xhtml'
    URL_PLANNING = 'https://onboard.ec-nantes.fr/faces/Planning.xhtml'
    DATE = date.today().strftime("%d/%m/%Y")
    WEEK = str(date.today().isocalendar().week)
    #YEAR = date.today().strftime("%Y")
    YEAR = '2022'

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    BEGINNING = ''.join(str(timestamp - 86400).split(
        '.'))[:13]  # on retire 24h pour inclure le planning du jour
    # END = '1653948000000'  #choix arbitraire, fin au 31-05-2022
    timestamp = now + timedelta(days=250)
    timestamp = datetime.timestamp(timestamp)
    END = ''.join(str(timestamp).split('.'))[:13]

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = Session()
        self.view_state = ""
        self.cookies = ""
        self.last_request = None

    def update_view_state(self, request):
        regex_view_state = re.compile(
            r'id="j_id1:javax.faces.ViewState:0" value="[0-9-:]*" autocomplete="off"'
        )
        view_state = regex_view_state.search(request.text)[0]
        view_state = view_state.split('"')
        view_state = view_state[3]
        self.view_state = view_state

    def post_login(self):
        data_post = {
            'username': self.username,
            'password': self.password,
            'j_idt27': ''
        }
        headers = {
            'Accept': ('text/html,application/xhtml+xml,application'
                       '/xml;q=0.9,image/avif,image/webp,image/apng,*'
                       '/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            'Sec-Fetch-Site':
            'same-origin',
            'Sec-Fetch-Mode':
            'navigate',
            'Sec-Fetch-User':
            '?1',
            'Sec-Fetch-Dest':
            'document',
            'Referer':
            'https://onboard.ec-nantes.fr/faces/Login.xhtml',
            'Accept-Encoding':
            'gzip, deflate',
            'Accept-Language':
            'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        post_login = self.session.post(url=Onboard.URL_POST_LOGIN,
                                       data=data_post,
                                       headers=headers)
        self.cookies = post_login.cookies.get_dict()
        self.last_request = post_login

    def get_main(self):
        get_main = self.session.get(url=Onboard.URL_MENU, cookies=self.cookies)
        #print(get_main.text[2700:3000])
        self.update_view_state(get_main)

    def post_planning(self):
        data_post = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:j_idt52",
            "javax.faces.partial.execute": "form:j_idt52",
            "javax.faces.partial.render": "form:sidebar",
            "form:j_idt52": "form:j_idt52",
            "webscolaapp.Sidebar.ID_SUBMENU": "submenu_8817755",
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:sauvegarde": "",
            "form:j_idt826_focus": "",
            "form:j_idt826_input": "44323",
            "javax.faces.ViewState": self.view_state
        }
        self.last_request = self.session.post(url=Onboard.URL_MENU,
                                              data=data_post,
                                              cookies=self.cookies)

    def post_my_planning(self):
        data_post = {
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:sauvegarde": "",
            "form:j_idt826_focus": "",
            "form:j_idt826_input": "44323",
            "javax.faces.ViewState": self.view_state,
            "form:sidebar": "form:sidebar",
            "form:sidebar_menuid": "6_0"
        }
        self.last_request = self.session.post(url=Onboard.URL_MENU,
                                              data=data_post,
                                              cookies=self.cookies)

    def get_my_planning(self):
        my_planning_get = self.session.get(url=Onboard.URL_PLANNING,
                                           cookies=self.cookies)
        self.update_view_state(my_planning_get)
        #print(my_planning_get.text[2500:2700])
        self.last_request = my_planning_get

    def post_planning_month(self):
        data_post = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:j_idt117",
            "javax.faces.partial.execute": "form:j_idt117",
            "javax.faces.partial.render": "form:j_idt117",
            "form:j_idt117": "form:j_idt117",
            "form:j_idt117_start": "1639951200000",  #pas a jour
            "form:j_idt117_end": "1641682800000",  #idem
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:date_input": Onboard.DATE,
            "form:week": Onboard.WEEK + '-' + Onboard.YEAR,
            "form:j_idt117_view": "agendaWeek",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state
        }
        self.last_request = self.session.post(url=Onboard.URL_PLANNING,
                                              data=data_post,
                                              cookies=self.cookies)

    def post_planning_year(self):
        data_post = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:j_idt117",
            "javax.faces.partial.execute": "form:j_idt117",
            "javax.faces.partial.render": "form:j_idt117",
            "form:j_idt117": "form:j_idt117",
            "form:j_idt117_start": Onboard.BEGINNING,
            "form:j_idt117_end": Onboard.END,
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:date_input": Onboard.DATE,
            "form:week": Onboard.WEEK + '-' + Onboard.YEAR,
            "form:j_idt117_view": "agendaWeek",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state
        }
        self.last_request = self.session.post(url=Onboard.URL_PLANNING,
                                              data=data_post,
                                              cookies=self.cookies)

    def post_download(self):
        data_post = {
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:date_input": Onboard.DATE,
            "form:week": Onboard.WEEK + '-' + Onboard.YEAR,
            "form:j_idt117_view": "month",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state,
            "form:j_idt120": "form:j_idt120"
        }
        post_download_month = self.session.post(url=Onboard.URL_PLANNING,
                                                data=data_post,
                                                cookies=self.cookies)
        self.last_request = post_download_month


if __name__ == '__main__':
    import time

    start = time.time()
    with open("./Credentials/OnBoard", "r") as file:
        lines = file.readlines()
        username = lines[0].rstrip()
        password = lines[1].rstrip()
    essai = Onboard(username, password)
    essai.post_login()
    essai.get_main()
    essai.post_planning()
    essai.post_my_planning()
    essai.get_my_planning()
    essai.post_planning_year()
    essai.post_download()
    print(essai.last_request.text[:200])
    print(time.time() - start)
