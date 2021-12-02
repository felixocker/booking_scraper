#!/usr/bin/env python3
"""create report for results from booking.com"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class BookingReport:
    def __init__(self, hotel_list: WebElement) -> None:
        self.hotel_list = hotel_list
        self.hotel_boxes = self.get_hotel_elems()

    def get_hotel_elems(self):
        return self.hotel_list.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_data(self):
        all_hotel_data = []
        for hotel_box in self.hotel_boxes:
            new_entry = False
            name = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            try:
                star_images = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="rating-stars"]')
            except NoSuchElementException as e:
                new_entry = True
                star_images = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="rating-squares"]')
            rating = len(star_images.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]'))
            price = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="price-and-discounted-price"]').text[3:]
            # TODO: the following is specific for USD - make generic
            price_low = price.split("US$")[-1].replace(",", "")
            if not new_entry:
                review = hotel_box.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text
                review_rating = review.split('\n')[0]
                review_amount = review.split('\n')[-1].split(" ")[0]
            else:
                review_rating, review_amount = "-", 0
            hotel_data = {
                "name": name,
                "stars": rating,
                "price": price_low,
                "average review": review_rating,
                "number of reviews": review_amount,
            }
            all_hotel_data.append(hotel_data)
        return all_hotel_data
