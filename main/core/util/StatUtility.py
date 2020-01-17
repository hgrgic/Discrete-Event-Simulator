from scipy.stats import norm
from scipy.stats import gamma
import numpy as np
import pandas as pd


# center is the parameter which represents the center of the normal distribution
def get_norm_dist(_size, center=10):
    return norm.rvs(size=_size, loc=center, scale=1)


def get_gamma_dist(_size, _a):
    return gamma.rvs(a=_a, size=_size)


def get_binomial_dist(_size, probability, options=1):
    return np.random.binomial(options, probability, _size)


def get_poisson_dist(_size, _center):
    return np.random.poisson(_center, _size)


def generate_settings_per_hour_df(events_per_hour, distribution_per_hour, load_times_per_hour):
    settings_per_hour = pd.DataFrame([events_per_hour, distribution_per_hour, load_times_per_hour])
    settings_per_hour = settings_per_hour.transpose()
    settings_per_hour.columns = ["n_events", "distribution", "load_times"]
    return (settings_per_hour)


def generate_intervals_hour(n_events, distribution):
    intervals = []
    time = 0
    if distribution == "exponential":
        while time < 1:
            new_interval = np.random.exponential(1 / n_events)
            time = time + new_interval
            intervals.append(time)
        return np.array(intervals[:-1])
    if distribution == "gamma":
        while time < 1:
            new_interval = np.random.gamma(1 / n_events)
            time = time + new_interval
            intervals.append(time)
        return np.array(intervals[:-1])


def generate_intervals_day(events_per_hour, distribution_per_hour):
    hour = 0
    interval_list = []
    for i in range(len(events_per_hour)):
        interval_list.append(list(generate_intervals_hour(events_per_hour[i], distribution_per_hour[i]) + hour))
        hour += 1
    return interval_list


def generate_load_times_day(interval_list, load_times_per_hour):
    load_times_list = []
    for e, i in enumerate(interval_list):
        n = len(i)
        load_times_list.append(np.random.exponential(load_times_per_hour[e], n))
    return load_times_list


def generate_intervals_load_times_and_names(events_per_hour, distribution_per_hour, load_times_per_hour):
    intervals_day = generate_intervals_day(events_per_hour, distribution_per_hour)
    load_times_day = generate_load_times_day(intervals_day, load_times_per_hour)
    flat_intervals_day = [item for sublist in intervals_day for item in sublist]
    flat_load_times_day = [item for sublist in load_times_day for item in sublist]
    names_day = list(range(1, len(flat_intervals_day) + 1))
    return flat_intervals_day, flat_load_times_day, names_day


