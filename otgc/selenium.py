"""Module containing only the GetOnboard class, to get ICS files.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class GetOnboard:
    '''Get ICS files from OnBoard schedule using Selenium.'''
    def __init__(
            self,
            credentials="",
            export_dir="",
            nb_months=2,
            gecko_path=""):
        self.credentials = credentials
        self.export_dir = export_dir
        self.nb_months = nb_months
        self.gecko_path = gecko_path

        fx_profile = webdriver.FirefoxProfile()
        head_option = webdriver.FirefoxOptions()
        head_option.add_argument("--headless")
        fx_profile.set_preference("browser.download.folderList", 2)
        fx_profile.set_preference("browser.download.manager.showWhenStarting",
                                  False)
        fx_profile.set_preference("browser.download.dir",
                                  export_dir)
        fx_profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                  "text/calendar")
        fx_profile.set_preference("browser.helperApps.neverAsk.openFile",
                                  "text/calendar")
        fx_profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/octet-stream doc xls pdf txt ics")
        fx_profile.set_preference(
            "browser.helperApps.neverAsk.openFile",
            "application/octet-stream doc xls pdf txt ics")
        driver = webdriver.Firefox(firefox_profile=fx_profile,
                                   options=head_option,
                                   executable_path=gecko_path)
        driver.get("https://onboard.ec-nantes.fr/faces/Login.xhtml")
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def authenticate(self):
        '''Get the credentials from the clear text
        file and authenticate on OnBoard Welcome Page'''
        with open(self.credentials, "r") as file:
            lines = file.readlines()
        username = lines[0]
        password = lines[1]

        element = self.driver.find_element_by_id("username")
        element.send_keys(username)

        element = self.driver.find_element_by_id("password")
        element.send_keys(password)

        del username
        del password
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div[6]/form[1]/div[4]/button/span"
        ).click()

    def go_to_schedule(self):
        '''Navigate from the first page after authentification
        to the schedule page (by month)'''
        planning = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/form/div[2]/div[2]/div/div[1]\
                    /div[1]/div/div/div[2]/ul/li[7]/a/span[2]")))
        planning.click()

        mon_planning = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/form/div[2]/div[2]/div/div[1]\
                    /div[1]/div/div/div[2]/ul/li[7]/ul/li[1]/a/span")))
        mon_planning.click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, '''/html/body/div[1]/form/div[1]/div[1]/div''')))
        mon_mois = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/form/div[2]/div[2]/div/div[2]\
                    /div/div/div[2]/div[6]/div/div[1]/div[2]/button[1]")))
        mon_mois.click()

    def get_month_ics_and_next(self):
        '''Download a ICS file and go the the next month'''
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, '''/html/body/div[1]/form/div[1]/div[1]/div''')))
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        telecharger = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/form/div[2]/div[2]/div/div\
                    [2]/div/div/div[2]/div[8]/div[1]/a[1]/i")))
        telecharger.click()

        suivant = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/form/div[2]/div[2]/div/\
                    div[2]/div/div/div[2]/div[6]/div/div[1]/div[1]/button[4]"
                 )))
        suivant.click()

    def get_ics(self):
        '''Get the ICS files for the given number of months,
        using the provided credentials'''
        self.authenticate()
        self.go_to_schedule()
        for _ in range(self.nb_months):
            self.get_month_ics_and_next()
        self.driver.quit()
        print(self.nb_months, 'file(s) downloaded with success.')


if __name__ == '__main__':

    directory = './Downloads'
    nb_months = 2

    onboard_planning = GetOnboard(credentials='./Credentials/OnBoard',
                                  export_dir=directory,
                                  nb_months=nb_months)
    onboard_planning.get_ics()
