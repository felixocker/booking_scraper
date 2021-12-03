#!/usr/bin/env python3
"""bot for booking.com"""

import os
from datetime import datetime
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import src.booking.constants as const
from src.booking.filter import BookingFilter
from src.booking.optimize import Optimizer
from src.booking.report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, wait: int = 10, headless: bool = const.HEADLESS, maximize: bool = False,
                 driver_path: str = const.CHROME_DRIVER_PATH, teardown: bool = False) -> None:
        self.wait = wait
        self.maximize = maximize
        self.teardown = teardown
        self.data: list = []
        self.optimized: list = []
        os.environ['PATH'] += ":" + driver_path
        options = Options()
        if headless:
            options.headless = True
            options.add_argument("--window-size=1920,1080")
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "\
                         "Chrome/60.0.3112.50 Safari/537.36"
            options.add_argument(f'user-agent={user_agent}')
        super().__init__(chrome_options=options)
        self.implicitly_wait(self.wait)
        if self.maximize:
            self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.teardown:
            self.quit()

    def land_first_page(self) -> None:
        self.get(const.BASE_URL)
        try:
            self.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except NoSuchElementException as e:
            pass

    def change_currency(self, currency: str) -> None:
        currency_path = f'a[data-modal-header-async-url-param*="selected_currency={currency}"'
        currency_current = self.find_element(By.XPATH, '/html/body/header/nav[1]/div[2]/div[1]/button/span/span[1]')
        if currency_current.text != currency:
            self.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]').click()
            self.find_element(By.CSS_SELECTOR, currency_path).click()

    def select_place(self, place: str) -> None:
        place_field = self.find_element(By.ID, 'ss')
        place_field.clear()
        place_field.send_keys(place)
        self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]').click()

    def select_date(self, startdate: str, enddate: str) -> None:
        # TODO: make this work for months other than current and next -> click arrow
        self.find_element(By.CSS_SELECTOR, f'td[data-date="{startdate}"]').click()
        self.find_element(By.CSS_SELECTOR, f'td[data-date="{enddate}"]').click()

    def specify_booking(self, adults: int, children: list = None, rooms: int = 1) -> None:
        self.find_element(By.ID, 'xp__guests__toggle').click()
        while int(self.find_element(By.ID, 'group_adults').get_attribute("value")) > 1:
            self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]').click()
        for _ in range(adults-1):
            self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]').click()
        if children is None:
            children = []
        for c, age in enumerate(children):
            self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Children"]').click()
            self.find_element(By.CSS_SELECTOR, f'select[aria-label="Child {c+1} age"]').send_keys(age)
        for _ in range(rooms-1):
            self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Rooms"]').click()

    def search(self) -> None:
        self.find_element(By.CLASS_NAME, "sb-searchbox__button ").click()

    def apply_filter(self, star_values: list) -> None:
        booking_filter = BookingFilter(driver=self)
        booking_filter.apply_star_rating(star_values)
        booking_filter.sort_by_lowest_price()

    def extract_data(self) -> None:
        # TODO: extract the following pages too
        hotel_list = self.find_element(By.ID, 'search_results_table')
        report = BookingReport(hotel_list)
        self.data = report.pull_data()

    def optimize(self) -> None:
        optimizer = Optimizer(self, quantity=const.LIMIT)
        self.optimized = optimizer.optimize()

    @staticmethod
    def create_results_table(data: list):
        table = PrettyTable(field_names=list(data[0].keys()))
        clean_list = [list(elem.values()) for elem in data]
        table.add_rows(clean_list)
        return table

    def report_results(self, print_to_console: bool = False) -> None:
        hotel_data = self.create_results_table(self.data)
        best_fit_data = self.create_results_table(self.optimized)
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        search_data = PrettyTable(field_names=["Search Parameter", "Value"])
        search_params = [[k, v] for k, v in const.__dict__.items() if not k.startswith('_') and
                         k not in ["BASE_URL", "CHROME_DRIVER_PATH", "HEADLESS"]]
        search_data.add_rows(search_params)
        report = f"Search conducted at: {timestamp}\n\n" +\
                 "Your best fits are:\n\n" + \
                 best_fit_data.get_string() + \
                 "\n\n" + \
                 "All results are:\n\n" +\
                 hotel_data.get_string() +\
                 "\n\n" +\
                 "Search input was:\n\n" +\
                 search_data.get_string()
        if print_to_console:
            print(report)
        # save report as file
        os.remove("report.txt")
        with open("report.txt", "w") as f:
            f.write(report)
