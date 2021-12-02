#!/usr/bin/env python3
"""bot for booking.com"""

import os
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By
import src.booking.constants as const
from src.booking.filter import BookingFilter
from src.booking.report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, wait: int = 10, maximize: bool = False, driver_path: str = const.CHROME_DRIVER_PATH,
                 teardown: bool = False) -> None:
        self.wait = wait
        self.maximize = maximize
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += ":" + driver_path
        super().__init__()
        self.implicitly_wait(self.wait)
        if self.maximize:
            self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.teardown:
            self.quit()

    def land_first_page(self) -> None:
        self.get(const.BASE_URL)
        self.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

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
        self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    def apply_filter(self, star_values: list):
        booking_filter = BookingFilter(driver=self)
        booking_filter.apply_star_rating(star_values)
        booking_filter.sort_by_lowest_price()

    def report_results(self):
        # TODO: extract the following pages too
        hotel_list = self.find_element(By.ID, 'search_results_table')
        report = BookingReport(hotel_list)
        table = PrettyTable(field_names=["Hotel Name", "Stars", "Price", "Avg. Review,", "No. of Reviews"])
        clean_list = [list(elem.values()) for elem in report.pull_data()]
        table.add_rows(clean_list)
        # TODO: save report as file
        print(table)
