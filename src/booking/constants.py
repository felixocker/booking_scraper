#!/usr/bin/env python3
"""constants for booking.com bot"""

# setup
BASE_URL = "https://www.booking.com"
CHROME_DRIVER_PATH = r"/home/felix/Documents/coding/python/web_scraping/chromedriver_linux64/"
HEADLESS = True

# trip details
CURRENCY = "USD"
PLACE = "New York"
START_DATE = "2022-02-20"
END_DATE = "2022-02-28"
ADULTS = 2
# for children, provide a list with their ages
CHILDREN = [8, 13]
ROOMS = 2
# provide a list of desired hotel star ratings
STARS = [3, 4]

# weightings for optimization in the form [weight, best, worst]
LIMIT = 5
WEIGHTS = {
    "average review": [1, 10.0, 0.0],
    "price": [1, 0.0, 5000.0],
    "distance [km]": [1, 0.0, 3.0],
}
