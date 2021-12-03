#!/usr/bin/env python3
"""bot for interacting with booking.com"""

import time
from src.booking.booking import Booking
from src.booking import constants as const


def main() -> None:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(const.CURRENCY)
        bot.select_place(const.PLACE)
        bot.select_date(startdate=const.START_DATE, enddate=const.END_DATE)
        bot.specify_booking(adults=const.ADULTS, children=const.CHILDREN, rooms=const.ROOMS)
        bot.search()
        bot.apply_filter(star_values=const.STARS)
        bot.extract_data()
        bot.optimize()
        bot.report_results(print_to_console=True)


if __name__ == "__main__":
    main()
