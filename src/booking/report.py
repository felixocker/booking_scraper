#!/usr/bin/env python3
"""create report for results from booking.com"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import src.booking.constants as const


class BookingReport:
    def __init__(self, hotel_list: WebElement) -> None:
        self.hotel_list = hotel_list
        self.hotel_boxes = self.get_hotel_elems()

    def get_hotel_elems(self):
        return self.hotel_list.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_data(self):
        all_hotel_data = []
        currencies = {
            "USD": "US$",
            "EUR": "€ ",
            "GBP": "£",
            "CHF": "CHF ",
        }
        assert const.CURRENCY in currencies, f"currency not supported, please choose one of {list(currencies.keys())}"
        for hotel_box in self.hotel_boxes:
            name = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            try:
                star_images = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="rating-stars"]')
            except NoSuchElementException as e:
                star_images = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="rating-squares"]')
            rating = len(star_images.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]'))
            price = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="price-and-discounted-price"]').text
            price_low = float(price.split(currencies[const.CURRENCY])[-1].replace(",", ""))
            try:
                review = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text
                review_rating = float(review.split('\n')[0])
                review_amount = int(review.split('\n')[-1].split(" ")[0].replace(",", ""))
            except NoSuchElementException as e:
                review_rating, review_amount = "", 0
            dist_str = hotel_box.find_element(By.CSS_SELECTOR, 'span[data-testid="distance"]').get_attribute('innerHTML').strip()
            if " km " in dist_str:
                distance = float(dist_str.split(" km ")[0])
            elif " m " in dist_str:
                distance = float(dist_str.split(" m ")[0].replace(",", ""))/1000
            else:
                distance = ""
            link = hotel_box.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_attribute('href')
            hotel_data = {
                "name": name,
                "stars": rating,
                "price": price_low,
                "average review": review_rating,
                "number of reviews": review_amount,
                "distance [km]": distance,
                "quick link": link,
            }
            all_hotel_data.append(hotel_data)
        return all_hotel_data
