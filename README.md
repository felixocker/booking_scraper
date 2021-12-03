# booking_scraper
bot for scraping hotel data from [booking.com](https://www.booking.com/) \
I was loosely following this [FCC tutorial](https://www.youtube.com/watch?v=j7VZsCCnptM&list=WL&index=9&t=49s&ab_channel=freeCodeCamp.org), their [code](https://github.com/jimdevops19/SeleniumSeries) is also available on GitHub

## setup
Note that the Chrome driver must match your Chrome version
* check Chrome version via [settings](chrome://version/)
* get Chrome driver
  * download respective driver version from [Google download site](https://chromedriver.chromium.org/downloads)
  * specify the path to the Chrome driver in the config file

## use
1. specify your desired travel parameters in the *config.py* file
2. indicate your personal preferences via the objective function's parameters (WEIGHTS) in the *config.py* file
3. run ```python booking_scraper.py```
4. check search results, either in your terminal or in the *report.txt* file
