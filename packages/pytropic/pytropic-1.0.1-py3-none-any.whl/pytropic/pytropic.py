# -*- coding: utf-8 -*-
import collections
import math
import warnings
import json

"""Main module."""


def sliding(string, n):
    for i in range(len(string) - n + 1):
        yield string[i : i + n]


class Model(object):
    """A counter for ngrams"""

    def __init__(self, size=2.0, name=None):
        self.size = size
        self.default_count = 0.5  # make a parameter?
        self.counter = collections.Counter()
        self.total = 0
        self.name = name

    def __repr__(self):
        return "<Model {}>".format(self.name)

    def update(self, string, muliplier=1):
        """
        Public: update a counter with a string, and a multiplier

        Examples

        counter = NGramCounter(2)
        counter.update_with_multiplier('01234', 1)

        string: The String to update with
        multiplier: The Integer describing how much weight (will often be 1)
        """
        for substr in sliding(string, self.size):
            self.counter[substr] += muliplier
            self.total += muliplier

    def count(self, ngram):
        """
        Public: get count for string, with default

         Examples

         counter = NGramCounter.new(2)
         counter.update('01234')
         counter.count('01')
         #=> 1
         counter.count('bob')
         #=> 0.5

         ngram: The String to check

        """
        return self.counter.get(ngram, self.default_count)

    def log_prob(self, key):
        if self.total == 0 or not key:
            return -math.inf
        count = self.count(key)
        return math.log(count, 2.0) - math.log(self.total, 2.0)

    def dump(self, io):
        for key, value in self.counter.items():
            io.write("{}\t{}\t{}\n".format(self.size, key, value))

    def dump_json(self, io):
        for key, value in self.counter.items():
            io.write(
                json.dumps(
                    {
                        "model_name": self.name,
                        "ngram_size": self.size,
                        "ngram": key,
                        "count": value,
                    }
                )
                + "\n"
            )

    def predict(self, string):
        n_ngrams = 0
        log_prob_total = 0.0
        for ngram in sliding(string, self.size):
            n_ngrams += 1
            log_prob_total += self.log_prob(ngram)
        log_prob_average = log_prob_total / n_ngrams
        return {
            "log_prob_total": log_prob_total,
            "log_prob_average": log_prob_average,
            "size": int(n_ngrams),
        }

    def entropy(self, string):
        return -self.predict(string)["log_prob_average"]

    def read(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                _, ngram, count = line.strip().split("\t")
                count = float(count)
                self.counter[ngram] += count
                self.total += count
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))

    def read_json(self, io, count_key="count", ngram_key="ngram"):
        n = 0
        for line in io:
            n += 1
            data = json.loads(line.strip())
            count = data[count_key]
            ngram = data[ngram_key]
            self.counter[ngram] += count
            self.total += count

    def read_from_string(self, string):
        n = 0
        for line in string.split("\n"):
            n += 1
            _, ngram, count = line.strip().split("\t")
            count = float(count)
            self.counter[ngram] += count
            self.total += count

    def train(self, io):
        for line in io:
            self.update(line.strip())

    def train_with_multiplier(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                text, count = line.strip().split("\t")
                count = float(count)
                self.update(text, count)
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))


def read_models_from_json(
    io,
    count_key="count",
    ngram_key="ngram",
    model_name_key="model_name",
    ngram_size_key="ngram_size",
    ngram_size=None,
):
    models = {}
    for line in io:
        data = json.load(line.strip())
        ngram = data[ngram_key]
        count = data[count_key]
        model_name = data[model_name_key]
        ngram_size = data[ngram_size_key]
        if model_name not in models:
            models[model_name] = Model(size=ngram_size, name=model_name)
        model = models[model_name]
        model.update(ngram, count)
    return models
