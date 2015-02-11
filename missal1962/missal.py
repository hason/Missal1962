from datetime import date, datetime, timedelta
from dateutil.easter import easter
import sys
from constants import *


def get_index_of_date(empty_year, date_):
    for ii, day in enumerate(empty_year):
        if day[0] == date_:
            return ii


def build_empty_year(year):
    empty_year = list()
    day = date(year, 1, 1)

    while day.year == year:
        empty_year.append([day, []])
        day += timedelta(days=1)

    return empty_year


def calc_varday__dom_ressurectionis(year):
    """ Ressurection (Easter) Sunday
    """
    return easter(year)


def calc_varday__dom_sanctae_familiae(year):
    """ Dominica Sanctae Familiae Jesu Mariae Joseph
    First Sunday after Epiphany (06 January)
    """
    epiphany = date(year, 1, 6)
    wd = epiphany.weekday() 
    delta = 6 - wd if wd < 6 else 7
    return epiphany + timedelta(days=delta)


def calc_varday__dom_septuagesima(year):
    """ Dominica in Septuagesima
    First day of a Ressurection Sunday related block.
    It's 63 days before Ressurection.
    """
    return calc_varday__dom_ressurectionis(year) - timedelta(days=63)


def calc_varday__dom_adventus(year):
    """ Dominica I Adventus
    Nov 27 (if it's Sunday) or closest Sunday
    """
    advent = date(year, 11, 27)
    wd = advent.weekday()
    if wd != 6:
        advent += timedelta(days=6-wd)
    return advent


if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year
    empty_year = build_empty_year(year)

    blocks = (
        # Post Epiphany
        (calc_varday__dom_sanctae_familiae, vardays__post_epiphania),
        # Pascha related days
        (calc_varday__dom_septuagesima, vardays__pascha),
        # Advent
        (calc_varday__dom_adventus, vardays__advent)
    )

    for calc_varday_func, dataset in blocks:
        index = get_index_of_date(empty_year, calc_varday_func(year))
        for ii, day in enumerate(dataset):
            empty_year[index + ii][1] = [day]

    # Fixed days
    for date_, contents in empty_year:
        date_id = date_.strftime("%m-%d")
        days = list(set([ii for ii in fixdays if ii.startswith(date_id)]))
        contents.extend(days)

    for ii in empty_year:
        print ii[0].strftime('%A'), ii