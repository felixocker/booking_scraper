#!/usr/bin/env python3
"""optimize with simple objective function"""

import copy
from selenium.webdriver.remote.webdriver import WebDriver
import src.booking.constants as const


class Optimizer:
    def __init__(self, driver: WebDriver, quantity: int) -> None:
        self.options = copy.deepcopy(driver.data)
        self.quantity = quantity
        self.weights = const.WEIGHTS

    def check_validity(self, option) -> bool:
        valid = True
        for k in self.weights:
            lower = min(self.weights[k][1], self.weights[k][2])
            higher = max(self.weights[k][1], self.weights[k][2])
            if not option[k] or not lower <= option[k] <= higher:
                valid = False
                break
        return valid

    def calc_ind_score(self, value, scoretype: str) -> float:
        score = (value - self.weights[scoretype][2]) / (self.weights[scoretype][1] - self.weights[scoretype][2])
        return score

    def calc_score(self, option):
        score = sum(self.calc_ind_score(option[k], k) * self.weights[k][0] for k in self.weights) /\
                sum(self.weights[k][0] for k in self.weights)
        return round(score, 2)

    def optimize(self):
        valid_options = [opt for opt in self.options if self.check_validity(opt)]
        for opt in valid_options:
            opt["score"] = self.calc_score(opt)
        ranked = sorted(valid_options, key=lambda d: d["score"], reverse=True)
        return ranked[:self.quantity]
