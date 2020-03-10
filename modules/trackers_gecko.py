from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, JavascriptException,
                                        InvalidArgumentException
from itertools import product
from urllib.parse import urlparse
from re import compile, IGNORECASE
from requests import get
from requests.exceptions import ConnectionError, ReadTimeout
from time import sleep
from json import loads, load


with open('tracker_set.json') as j:
    tracker_set = load(j)


def is_valid_url(url):
    """Valide URLs Only. From only Django Source
    May update: https://github.com/django/django/blob/master/django/core/validators.py#L74"""
    regex = compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', IGNORECASE)
    return url is not None and regex.search(url)


def clean_url(url):
    """Ensure hostname is affixed to URL"""
    parse = urlparse(url)
    if parse[1] == '':
        url = 'https://' + parse[2]
    elif parse[0] not in ['https', 'http']:
        url = 'https://' + parse[1]
    return url


def get_calls(driver):
    """Get Network calls from browser.
    Stringify required to prevent cyclical error present in gecko driver """
    try:
        resources = driver.execute_script("return window.performance.getEntries();")
        print('NON_STRINGIFY')
        return [resource['name'] for resource in resources]
    except JavascriptException:
        resources = driver.execute_script("return JSON.stringify(window.performance.getEntries());")
        print('stringify')
        return [resource['name'] for resource in loads(resources)]


def get_network_dat(url, sleep_time):
    """Construct list of sites called through external network calls"""
    path_to_driver = '/home/ubuntu/track_proj/geckodriver'
    path_to_log = '/home/ubuntu/track_proj/geckodriver.log'
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=path_to_driver, service_log_path=path_to_log)
    driver.set_page_load_timeout(100)
    try:
        driver.get(url)
        sleep(sleep_time + 3)
        calls = get_calls(driver)
        driver.quit()
        out = [i for i in calls]
        return get_network_trackers(out)
    except (TimeoutException, UnboundLocalError, WebDriverException, InvalidArgumentException):
        driver.quit()
        return {"Connection Error"}


def get_network_trackers(traff_urls):
    """Test network calls against list of known trackers.
    Return positive trackers found"""
    trackers = set()
    if len(traff_urls) > 0:
        for key, sites in tracker_set.items():
            for site, traff in product(sites, traff_urls):
                if traff.find(site) != -1:
                    trackers.add(key)
    return trackers


def get_raw_trackers(url):
    """Scan raw HTML for trackers"""
    raw_trackers = set()
    try:
        r = get(url, timeout=30)
        html = r.text
        for key, sites in tracker_set.items():
            for site in sites:
                if html.find(site) != -1:
                    raw_trackers.add(key)
        return raw_trackers
    except (ConnectionError, ReadTimeout):
        return {'Connection Error'}


def track_light(url, sleep_time):
    """Performs site analysis
        status == 0 Connection Error
        Status == 1 Trackers
        Status == 2 No Trackers
        Status == 3 Trouble Obtaining Network Data
        Status == 4 No Raw"""
    cleaned_url = clean_url(url)
    if is_valid_url(cleaned_url):
        net_traffic = get_network_dat(cleaned_url, sleep_time)
        raw_traffic = get_raw_trackers(cleaned_url)
        out = net_traffic.union(raw_traffic)
        if 'Connection Error' in out:
            if raw_traffic == {'Connection Error'} and net_traffic != {'Connection Error'}:
                if not net_traffic:
                    return [{'No Trackers'}, 2]
                else:
                    return [sorted(net_traffic), 4]
            elif net_traffic == {'Connection Error'} and raw_traffic != {'Connection Error'}:
                return [sorted(raw_traffic), 3]
            else:
                return [out, 0]
        elif out == set():
            return [{'No Trackers'}, 2]
        else:
            return [sorted(out), 1]
    else:
        return ['Bad URL', 5]
