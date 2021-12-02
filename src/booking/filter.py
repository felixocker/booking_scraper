#!/usr/bin/env python3
"""filter results at booking.com"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFilter:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def apply_star_rating(self, star_values: list):
        star_filter_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        star_child_elems = star_filter_box.find_elements(By.CSS_SELECTOR, '*')
        for star_value in star_values:
            for sce in star_child_elems:
                if f'{star_value} star' in str(sce.get_attribute('innerHTML')):
                    sce.click()

    def sort_by_lowest_price(self):
        self.driver.find_element(By.CSS_SELECTOR, 'li[data-id="price"]').click()
