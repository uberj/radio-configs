import attr

@attr.s
class Station(object):
    frequency = attr.ib()
    offset = attr.ib()
    offset_direction = attr.ib()
    tone = attr.ib()
    location = attr.ib()
    city = attr.ib()
    ST_PR = attr.ib()
    county = attr.ib()
    call = attr.ib()
    use = attr.ib()

@attr.s
class RadioRefernceStation(object):
    frequency = attr.ib()
    input_freq = attr.ib()
    city = attr.ib()
    county = attr.ib()
    state = attr.ib()
    system_category = attr.ib()
    alpha_tag = attr.ib()
    description = attr.ib()
    service_tag = attr.ib()
