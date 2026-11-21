# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Executing functions."""
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import pandas
from ._types import TimeTableData
from typing import overload

__all__ = [
    'load_timetable',
]


@overload
def load_timetable() -> pandas.DataFrame:
    return pandas.DataFrame({
        'course': ['[33]'],
        'day': [0],
        'hour': [5],
        'minute': [11],
    })


@overload
def load_timetable(
    start_url: str,
    stop_code: str
) -> pandas.DataFrame:
    return pandas.DataFrame({
        'course': ['[33]'],
        'day': [0],
        'hour': [5],
        'minute': [11],
    })


def load_timetable(
    start_url: str = 'https://busnavi.keihanbus.jp/pc/diagram',
    stop_code: str = '0957-2'
) -> pandas.DataFrame:
    """Loads the time table of the Keihan Bus.

    Parameters
    ----------
    start_url : valid URL string, optional
        The home page URL.
    stop_code : str, optional
        The bus stop code string.

    Returns
    -------
    df : DataFrame
        The ``DataFrame`` object
        which represents the serialized time table data.
    """
    data: TimeTableData = {
        'course': [],
        'day': [],
        'hour': [],
        'minute': [],
    }
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    driver = Edge(options)
    driver.get(start_url)
    driver.implicitly_wait(2.)
    search_input = driver.find_element(By.XPATH, '/html/body/div/div[4]/div/form/div[2]/div[2]/div/div[1]/div/p[1]/input[1]')
    wait = WebDriverWait(driver, timeout=30.)
    wait.until(lambda _: search_input.send_keys(stop_code) or True)
    wait.until(lambda _: search_input.send_keys(Keys.ENTER) or True)
    driver.implicitly_wait(2.)
    for day in range(3):
        selections_list = driver.find_elements(By.XPATH, '//*[@id="mov-wrap"]/div[4]/div/div[2]/div[2]/ul[2]/li')
        selection = selections_list[day]
        wait.until(lambda _: selection.click() or True)
        driver.implicitly_wait(5.)
        courses: list[str] = []
        for course in driver.find_elements(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/ul[3]/li/div[2]/div[2]/table/thead/tr/th/p[1]/span'):
            courses.append(course.text)
        if len(courses) < 1:
            raise Exception("Couldn't load the selections.")
        table_body = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/ul[3]/li/div[2]/div[2]/table/tbody')
        for tr in table_body.find_elements(By.TAG_NAME, 'tr'):
            hour = int(tr.find_element(By.TAG_NAME, 'td').text)
            print('Number of hits:', len(tr.find_elements(By.CSS_SELECTOR, 'td:nth-of-type(n+2)')))
            for csn, td in enumerate(tr.find_elements(By.CSS_SELECTOR, 'td:nth-of-type(n+2)')):
                print(csn)
                if csn >= len(courses):
                    raise IndexError(f'Too large number of hits. `{csn}` is too large.')
                cs = courses[csn]
                for minute_span in td.find_elements(By.CSS_SELECTOR, 'ul > li > span:last-of-type'):
                    minute = int(minute_span.text)
                    data['hour'].append(hour)
                    data['day'].append(day)
                    data['course'].append(cs)
                    data['minute'].append(minute)
    df = pandas.DataFrame(data)
    return df
