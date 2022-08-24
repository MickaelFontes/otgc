import re
from datetime import date, datetime, timedelta

from requests import Session


class Onboard:
    """Implementation of manual requests to get a planning from OnBoard"""

    URL_LOGIN_PAGE = "https://onboard.ec-nantes.fr/faces/Login.xhtml"
    URL_POST_LOGIN = "https://onboard.ec-nantes.fr/login"
    URL_MENU = "https://onboard.ec-nantes.fr/faces/MainMenuPage.xhtml"
    URL_PLANNING = "https://onboard.ec-nantes.fr/faces/Planning.xhtml"
    DATE = date.today().strftime("%d/%m/%Y")
    WEEK = str(date.today().isocalendar().week)
    YEAR = date.today().strftime("%Y")

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    BEGINNING = "".join(str(timestamp - 86_400).split("."))[
        :13
    ]  # 86_400 sec = 24h, we remove them to get the events of the current day
    timestamp = now + timedelta(days=250)
    timestamp = datetime.timestamp(timestamp)
    END = "".join(str(timestamp).split("."))[:13]

    timestamp = now + timedelta(days=30)
    timestamp = datetime.timestamp(timestamp)
    END_MONTH = "".join(str(timestamp).split("."))[:13]

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = Session()
        self.view_state = ""
        self.cookies = ""
        self.last_request = None

    def update_view_state(self):
        """Extract the unique ViewState of the last request.
        The ViewState is needed to perform other requests to OnBoard.
        """
        regex_view_state = re.search(
            r'id="j_id1:javax.faces.ViewState:0" value="([0-9-:]*)" autocomplete="off"',
            self.last_request.text,
        )
        if regex_view_state:
            view_state = regex_view_state.group(1)
        self.view_state = view_state

    def get_planning_menu_id(self):
        """Method to get the menu_id of the My Schedule section

        Returns:
            string: menu_id to provide to the next POST request
        """
        # Matches the first element (see '_0'), it should be the My Schedule
        # May change with major updates with the menus
        regex_menu_id = re.search(
            r"form:sidebar_menuid':'([0-9]*_0)'", self.last_request.text
        )
        if regex_menu_id:
            menu_id = regex_menu_id.group(1)
        return menu_id

    def is_auth(self):
        get_title = re.search(
            r"\<title\>([a-zA-Z \']*)\s*\<\/title>", self.last_request.text
        )
        if get_title:
            title = get_title.group(1)
            if title.lower() in ["page d'accueil", "home page"]:
                return True

    def post_login(self):
        data_post = {
            "username": self.username,
            "password": self.password,
            "j_idt27": "",
        }
        headers = {
            "Accept": (
                "text/html,application/xhtml+xml,application"
                "/xml;q=0.9,image/avif,image/webp,image/apng,*"
                "/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            ),
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://onboard.ec-nantes.fr/faces/Login.xhtml",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        self.last_request = self.session.post(
            url=Onboard.URL_POST_LOGIN, data=data_post, headers=headers
        )
        # Check if authentification was successful
        if self.is_auth():
            print("Authentification successful")
        self.cookies = self.last_request.cookies.get_dict()

    def get_main(self):
        self.last_request = self.session.get(url=Onboard.URL_MENU, cookies=self.cookies)
        self.update_view_state()

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
            "javax.faces.ViewState": self.view_state,
        }
        self.last_request = self.session.post(
            url=Onboard.URL_MENU, data=data_post, cookies=self.cookies
        )

    def post_my_planning(self):
        menu_id = self.get_planning_menu_id()
        data_post = {
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:sauvegarde": "",
            "form:j_idt826_focus": "",
            "form:j_idt826_input": "44323",
            "javax.faces.ViewState": self.view_state,
            "form:sidebar": "form:sidebar",
            "form:sidebar_menuid": menu_id,
        }
        self.last_request = self.session.post(
            url=Onboard.URL_MENU, data=data_post, cookies=self.cookies
        )

    def get_my_planning(self):
        self.last_request = self.session.get(
            url=Onboard.URL_PLANNING, cookies=self.cookies
        )
        self.update_view_state()

    def post_planning_month(self):
        data_post = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:j_idt117",
            "javax.faces.partial.execute": "form:j_idt117",
            "javax.faces.partial.render": "form:j_idt117",
            "form:j_idt117": "form:j_idt117",
            "form:j_idt117_start": Onboard.BEGINNING,
            "form:j_idt117_end": Onboard.END_MONTH,
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:date_input": Onboard.DATE,
            "form:week": Onboard.WEEK + "-" + Onboard.YEAR,
            "form:j_idt117_view": "agendaWeek",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state,
        }
        self.last_request = self.session.post(
            url=Onboard.URL_PLANNING, data=data_post, cookies=self.cookies
        )

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
            "form:week": Onboard.WEEK + "-" + Onboard.YEAR,
            "form:j_idt117_view": "agendaWeek",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state,
        }
        self.last_request = self.session.post(
            url=Onboard.URL_PLANNING, data=data_post, cookies=self.cookies
        )

    def post_download(self):
        data_post = {
            "form": "form",
            "form:largeurDivCenter": "923",
            "form:date_input": Onboard.DATE,
            "form:week": Onboard.WEEK + "-" + Onboard.YEAR,
            "form:j_idt117_view": "month",
            "form:offsetFuseauNavigateur": "-3600000",
            "form:onglets_activeIndex": "0",
            "form:onglets_scrollState": "0",
            "form:j_idt236_focus": "",
            "form:j_idt236_input": "44323",
            "javax.faces.ViewState": self.view_state,
            "form:j_idt120": "form:j_idt120",
        }
        self.last_request = self.session.post(
            url=Onboard.URL_PLANNING, data=data_post, cookies=self.cookies
        )


if __name__ == "__main__":
    import time

    start = time.time()
    with open("./Credentials/OnBoard", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        username_text = lines[0].rstrip()
        password_text = lines[1].rstrip()
    essai = Onboard(username_text, password_text)
    essai.post_login()
    essai.get_main()
    essai.post_planning()
    essai.post_my_planning()
    essai.get_my_planning()
    essai.post_planning_year()
    essai.post_download()
    print(time.time() - start)
