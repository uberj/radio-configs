import sys
import requests
from station import Station
from pyquery import PyQuery as pq

state_codes = {
    "OR": 41
}

state_dl_link = "https://www.repeaterbook.com/repeaters/keyResult.php?" \
    "keyword={city}&state_id={state_code}"

def main(state):
    if not state in state_codes.keys():
        raise Exception("No state code for state " + state)

    state_code = state_codes[state]

    for city in [city.strip() for city in open(state + "-cities.txt", "r")]:
        stations = get_city_repeater_info(city, state_code)
        for station in stations:
            print(station)

def parse_frequency(raw_frequency):
    offset_direction = raw_frequency[-1]
    frequency = raw_frequency[:-1].replace(".", "")
    # TODO, detect band and set offset
    offset = "n/a"
    return frequency, offset, offset_direction


def parse_station_info(raw_tr):
    print(raw_tr)
    tds = raw_tr.findall('td')
    if not tds:
        return None
    if len(tds) != 8:
        print("more than 8 collumns per row. could they have updated the"
              "website?")
        return None

    raw_frequency, tone, location, ST_PR, county, call, use, _ = [
        td.text_content().strip() for td in tds
    ]
    frequency, offset, offset_direction = parse_frequency(raw_frequency)
    raw_tr.findall('td')[0].text_content()
    return Station(
        frequency=frequency,
        offset=offset,
        offset_direction=offset_direction,
        tone=tone,
        location=location,
        ST_PR=ST_PR,
        county=county,
        call=call,
        use=use
    )

def get_city_repeater_info(city, state_code):
    dl_link = state_dl_link.format(city=city, state_code=state_code)
    d = pq(url=dl_link)
    trs = d.find('.sortable > tr')
    return filter(None, [parse_station_info(tr) for tr in trs])


if __name__ == "__main__":
    main(sys.argv[1])
