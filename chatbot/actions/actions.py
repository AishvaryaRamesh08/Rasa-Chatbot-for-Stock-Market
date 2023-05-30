# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# python .\manage.py runserver
# rasa run actions
# rasa run -m models --enable-api --cors "*" --debug



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from yahoo_fin import stock_info
import datetime
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class ActionCurrentPrice(Action):
    def name(self) -> Text:
        return "action_current_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            tckr = tracker.get_slot('ticker')
            price = stock_info.get_live_price(tckr)
            if tckr[-2:] == 'NS' or tckr[-2] == 'BO':
                message = "Current price of " + tckr + " is " + str(price) + " INR."
                dispatcher.utter_message(text=message)
            else:
                message = "Current price of " + tckr + " is " + str(price) + " USD."
                dispatcher.utter_message(text=message)
        except:
            m = "Sorry data could not be fetched. Please ensure that you have typed the ticker symbol correctly."
            dispatcher.utter_message(text=m)

        return []


class ActionTimeNow(Action):

    def name(self) -> Text:
        return "action_time_now"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            current_time = datetime.datetime.now()
            message = "Time now is " + str(datetime.date.today()) + '\t' + str(current_time.hour) + ':' + str(
                current_time.minute)
            dispatcher.utter_message(text=message)

        except:
            m = "Sorry data could not be fetched. Please try again!"
            dispatcher.utter_message(text=m)

        return []


class ActionStWeb(Action):

    def name(self) -> Text:
        return "action_st_web"

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        url = "https://stockmarketview.herokuapp.com/"
        dispatcher.utter_message("Openning StockMarketView..")
        webbrowser.open(url)
        return []


class ActionChart(Action):
    def name(self) -> Text:
        return "action_chart"

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ticker = tracker.get_slot('chart_ticker')
        dispatcher.utter_message(text='Openning the chart..')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        url = "https://stockmarketview.herokuapp.com/"
        driver.get(url)
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]').click()
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/span/span').click()
        element = driver.find_element(By.XPATH,
                                      '/html/body/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/input')
        element.send_keys(ticker)
        element.send_keys(Keys.ENTER)
        return []


class ActionChartA(Action):
    def name(self) -> Text:
        return "action_chart_a"

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ticker = tracker.get_slot('chart_a_ticker')
        interval = tracker.get_slot('interval')
        if interval == 'hourly':
            period = '3mon'
        elif interval == 'weekly':
            period = '5y'
        elif interval == 'monthly':
            period = 'all'
        else:
            period = '1y'
        dispatcher.utter_message(text='Opening the chart..')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        url = "https://stockmarketview.herokuapp.com/"
        driver.get(url)
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]').click()
        t_element = driver.find_element(By.XPATH,
                                        '/html/body/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/input')
        t_element.send_keys(ticker)
        t_element.send_keys(Keys.ENTER)
        p_element = driver.find_element(By.XPATH,
                                        '/html/body/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/input')
        p_element.send_keys(period)
        p_element.send_keys(Keys.ENTER)
        return []


class ActionChartB(Action):
    def name(self) -> Text:
        return "action_chart_b"

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        interval = []
        period = []
        ticker = tracker.get_slot('chart_b_ticker')
        interval.append(tracker.get_slot('int_a'))
        interval.append(tracker.get_slot('int_b'))
        interval.append(tracker.get_slot('int_c'))
        for i in range(3):
            if interval[i] == 'hourly':
                period.append('3mon')
            elif interval[i] == 'weekly':
                period.append('5y')
            elif interval[i] == 'monthly':
                period.append('all')
            else:
                period.append('1y')
        dispatcher.utter_message(text='Opening the chart..')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        url = "https://stockmarketview.herokuapp.com/"
        driver.get(url)
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]').click()
        driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]').click()
        t_ele = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/input')
        t_ele.send_keys(ticker)
        t_ele.send_keys(Keys.ENTER)
        p1_ele = driver.find_element(By.XPATH,
                                     '/html/body/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[2]/input')
        p1_ele.send_keys(period[0])
        p1_ele.send_keys(Keys.ENTER)
        p2_ele = driver.find_element(By.XPATH,
                                     '/html/body/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div[2]/input')
        p2_ele.send_keys(period[1])
        p2_ele.send_keys(Keys.ENTER)
        p3_ele = driver.find_element(By.XPATH,
                                     '/html/body/div/div/div/div[2]/div[4]/div[1]/div/div/div/div/div[2]/input')
        p3_ele.send_keys(period[2])
        p3_ele.send_keys(Keys.ENTER)
        return []


class ActionChartC(Action):
    def name(self) -> Text:
        return "action_chart_c"

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ticker = tracker.get_slot('chart_c_ticker')
        interval = tracker.get_slot('int_ind')
        indicator = tracker.get_slot('indicator')
        if interval == 'hourly':
            period = '3mon'
        elif interval == 'weekly':
            period = '5y'
        elif interval == 'monthly':
            period = 'all'
        else:
            period = '1y'
        dispatcher.utter_message(text='Opening the chart..')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        url = "https://stockmarketview.herokuapp.com/"
        driver.get(url)
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]').click()
        t_element = driver.find_element(By.XPATH,
                                        '/html/body/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/input')
        t_element.send_keys(ticker)
        t_element.send_keys(Keys.ENTER)
        p_element = driver.find_element(By.XPATH,
                                        '/html/body/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/input')
        p_element.send_keys(period)
        p_element.send_keys(Keys.ENTER)
        ind_ele = driver.find_element(By.XPATH,
                                      '/html/body/div/div/div/div[2]/div[1]/div[5]/div/div/div/div/div[2]/input')
        ind_ele.send_keys(indicator)
        ind_ele.send_keys(Keys.ENTER)
        return []
