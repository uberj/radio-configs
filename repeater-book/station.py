import attr

@attr.s
class Station(object):
    frequency = attr.ib()
    offset = attr.ib()
    offset_direction = attr.ib()
    tone = attr.ib()
    location = attr.ib()
    ST_PR = attr.ib()
    county = attr.ib()
    call = attr.ib()
    use = attr.ib()
