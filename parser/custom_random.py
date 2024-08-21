from random import randint, normalvariate
from statistics import NormalDist
from math import sqrt, ceil
from typing import List
import json
import os


class RandomGenerator:
    def __init__(self, kappa=None, use_karmic=False, karmic_die_size=None):
        self.kappa = kappa or 0.999
        self.sigma = sqrt(1 / (1 - self.kappa ** 2))
        self.use_karmic = use_karmic
        self.karmic_die_size = karmic_die_size
        self.latent_score = normalvariate(0, self.sigma)

    @property
    def karmic_score(self) -> float:
        self.latent_score = -self.kappa * self.latent_score + normalvariate(0, 1)
        return self.latent_score

    def karmic_dice(self, n) -> int:
        dist = NormalDist(sigma=self.sigma)
        return ceil(n * dist.cdf(self.karmic_score))

    @staticmethod
    def original_dice(n) -> int:
        return randint(1, n)

    def roll(self, die_size, times=1) -> int | List[int]:
        if self.use_karmic and (self.karmic_die_size is None or die_size in self.karmic_die_size):
            func = self.karmic_dice
        else:
            func = self.original_dice
        rolls = [func(die_size) for i in range(times)]
        if times == 1:
            return rolls[0]
        return rolls


use_karmic = os.environ.get('USE_KARMIC') == 'True'
kappa = float(os.environ.get('KAPPA'))
karmic_die_size = json.loads(os.environ.get('KARMIC_DICE'))

rangen = RandomGenerator(use_karmic=use_karmic, kappa=kappa, karmic_die_size=karmic_die_size)
rangen_orig = RandomGenerator()

if __name__ == '__main__':
    rolls1 = rangen_orig.roll(20, times=100)
    rolls2 = rangen.roll(20, times=100)
    rangen0999 = RandomGenerator(use_karmic=True, kappa=0.999)
    rangen08 = RandomGenerator(use_karmic=True, kappa=0.8)
    rolls = rangen0999.roll(20, times=100)
    rolls08 = rangen08.roll(20, times=100)

    from collections import Counter
    c1 = Counter(rolls)
    c2 = Counter(rolls08)
    c3 = Counter(rolls2)
    c4 = Counter(rolls1)

    def discrepancy(c):
        v = c.values()
        return (max(v) - min(v)) / sum(v)

    print(discrepancy(c1), len(c1)/20)
    print(discrepancy(c2), len(c2)/20)
    print(discrepancy(c3), len(c3)/20)
    print(discrepancy(c4), len(c4)/20)
