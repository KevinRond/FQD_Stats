import requests
import numpy as np
import statistics as stat
import itertools
import time
from urllib.error import HTTPError
from Classes.stats import Stats

# years = [str(year) for year in range(2011, 2025)]
# genders = ['m', "f"]
# types = ['pl', 'bp']
# divisions = ['cl', 'eq']
# ac = ['sj', 'j', 'o', 'm1', 'm2', 'm3', 'm4']
male_wc = ['-53kg', '-59kg', '-66kg', '-74kg', '-83kg', '-93kg', '-105kg', '-120kg', '+120kg']
female_wc = ['-43kg', '-47kg', '-52kg', '-57kg', '-63kg', '-69kg', '-76kg', '-84kg', '+84kg']

years = [str(year) for year in range(2024, 2025)]
ac = ['sj', 'j', 'o']

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

def get_ranking_url(year='all', type='pl', division='cl', gender='m', ac='all', wc='all'):
    base_url = 'https://sheltered-inlet-15640.herokuapp.com/api/rankings'
    endpoint_url = f'{base_url}?year={year}&type={type}&division={division}&gender={gender}&ac={ac}&wc={wc}'
    return endpoint_url

def get_desc_stats(data):
    return {
        'mean': stat.mean(data),
        'median': stat.median(data),
        'mode': stat.mode(data),
        'std': stat.stdev(data),
        'var': stat.variance(data),
        'min': np.min(data),
        'max': np.max(data)
    }

def get_stats(year='2024', type='pl', division='cl', gender='m', ac='all', wc='all'):
    url = get_ranking_url(year, type, division, gender, ac, wc)

    # Retry logic
    retries = 3
    for attempt in range(retries):
        try:
            r = requests.get(url)
            data = r.json()

            if len(data) < 2:
                print(f"Skipping {year}, {gender}, {ac}, {wc}, {type}, {division} - Not enough data (less than 2 athletes).")
                return  # Skip processing this combination

            if type == 'pl':
                stats_data = {
                    'GL': [],
                    'Total': [],
                    'Squat': [],
                    'Bench': [],
                    'Deadlift': []
                }
            else:
                stats_data = {
                    'GL': [],
                    'Total': [],
                    'Bench': []
                }

            for athlete in data:
                total = athlete.get('total')
                if total > 0:
                    if type == 'pl':
                        stats_data['Total'].append(total)
                        stats_data['GL'].append(athlete.get('gl'))
                        stats_data['Squat'].append(float(athlete.get('squat')))
                        stats_data['Bench'].append(float(athlete.get('bench')))
                        stats_data['Deadlift'].append(float(athlete.get('deadlift')))
                    else:
                        stats_data['Total'].append(total)
                        stats_data['GL'].append(athlete.get('gl'))
                        stats_data['Bench'].append(float(athlete.get('bench')))

            stats_objects = {key: Stats(key, value, year, type, division, gender, ac, wc) for key, value in stats_data.items()}
            for stat_obj in stats_objects.values():
                stat_obj.print_stats()
                stat_obj.plot_histogram(save_dir=f"histograms/{year}/{type}/{division}/{gender}/{ac}/{wc.replace('-', '')}")

            break
        except HTTPError as e:
            if e.code == 429:  # Too many requests
                print(f"Rate limit exceeded, retrying after delay... (Attempt {attempt + 1}/{retries})")
                time.sleep(2 ** attempt)  # Exponential backoff (2^attempt seconds)
            else:
                print(f"HTTP error occurred: {e}")
                break  # Break out if it's not a rate limit error
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break  # Break out on other request errors



def get_weight_classes_for_gender(gender):
    if gender == 'm':
        return male_wc
    elif gender == 'f':
        return female_wc
    else:
        return []

def get_all_stats():
    for year, age_category in itertools.product(years, ac):
        for wc in male_wc:
            print(f"Fetching stats for {year}, males, {age_category}, {wc}")
            get_stats(year, type='pl', division='cl', gender='m', ac=age_category, wc=wc,)
            time.sleep(1)



if __name__ == '__main__':
    get_all_stats()
