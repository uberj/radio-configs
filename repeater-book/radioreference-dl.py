import sys

import requests
import pdb
from pyquery import PyQuery as pq

from station import RadioRefernceStation
from kenwood import KenwoodChannelLine, UnknownBandError

state_codes = {
    "OR": 41
}

state_dl_link = "https://www.repeaterbook.com/repeaters/keyResult.php?" \
    "keyword={city}&state_id={state_code}"

def get_stations(city, dl_link):
    d = pq(url=dl_link)
    all_data = d('table.rrtable').find('td')
    i = -1
    rows = []
    while True:
        i = i + 1
        if i == 0:  # Header
            continue
        next_row = all_data[i * 8: (i + 1) * 8]
        if not next_row:  # must be done
            break
        rows.append(next_row)
    return filter(None, [parse_station_info(city, row) for row in rows])

def parse_frequency(raw_frequency):
    return raw_frequency.replace(".", "")

def parse_station_info(city, row):

    #example [u'299.200000', u'', u'Multnomah', u'OR', u'Air Traffic Control', u'Approach/Dep', u'Approach/Departure - North', u'Aircraft']
    raw_frequency, in_freq, county, state, category, alpha_tag, description, service_tag = [
        td.text_content().strip() for td in row
    ]

    frequency = parse_frequency(raw_frequency)
    return RadioRefernceStation(
        frequency=frequency,
        input_freq=in_freq,
        city=city,
        county=county,
        state=state,
        system_category=category,
        alpha_tag=alpha_tag,
        description=description,
        service_tag=service_tag,
    )

def main(mem_chan, city, pages, ignore_service_tags):
    for page in pages:
        stations = get_stations(city, page)
        for station in sorted(stations, key=lambda station: station.service_tag):
            if station.service_tag in ignore_service_tags:
                continue
            mem_chan = mem_chan + 1
            channel = KenwoodChannelLine.from_radio_reference_station(mem_chan, station)
            print(channel.channelline)



def get_city_repeater_info(city, state_code):
    dl_link = state_dl_link.format(city=city, state_code=state_code)
    d = pq(url=dl_link)
    trs = d.find('.sortable > tr')
    return filter(None, [parse_station_info(city, tr) for tr in trs])


if __name__ == "__main__":
    #main(sys.argv[1])
    main(119, "Portland", [
        "http://www.radioreference.com/apps/db/?tab=reports&mid=44&rpt=1&os=0&s=tag",
        "http://www.radioreference.com/apps/db/?tab=reports&mid=44&rpt=1&os=200&s=tag",
        "http://www.radioreference.com/apps/db/?tab=reports&mid=44&rpt=1&os=400&s=tag"
        ], [
            "TRS",
            "Media"
            ])
