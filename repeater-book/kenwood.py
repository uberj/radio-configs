import itertools

import attr

from band import (
    is_70_cm_freq, is_2_meter_freq, UnknownBandError,
    cacl_tx_offset, is_6_meter_freq, is_33_cm_freq
)
from ctss_freqs import CTSS_OFFSET_LOOKUP

@attr.s
class KenwoodChannelLine(object):
        # NR    FREQ        STEP 0/+/- REV  PL/T PL/R DCS PL/T  PL/R DCS    OFFSET      MODE L/O            NAME
    nr_0 = attr.ib()
    freq_repr_1 = attr.ib()
    step_2 = attr.ib()
    offset_11 = attr.ib()
    offset_direction_3 = attr.ib()
    pl_t_8 = attr.ib()
    pl_r_9 = attr.ib()
    dcs_freq_10 = attr.ib()
    name_14 = attr.ib()
    pl_t_xmit_5 = attr.ib()
    dcs_xmit_7 = attr.ib(default=0)
    pl_r_xmit_6 = attr.ib(default=0)
    mode_12 = attr.ib(default=0)
    l_o_13 = attr.ib(default=0)
    rev_4 = attr.ib(default=0)

    @property
    def channelline(self):
        # 002	00440400000	8	 1	   0	1	 0	  0	  18	08	 000	005000000	0	 0				IRLP NEP
        return \
        "{nr_0}	" \
        "{freq_repr_1}	" \
        "{step_2}	" \
        "{offset_direction_3}	" \
        "{rev_4}	" \
        "{pl_t_xmit_5}	" \
        "{pl_r_xmit_6}	" \
        "{dcs_xmit_7}	" \
        "{pl_t_8}	" \
        "{pl_r_9}	" \
        "{dcs_freq_10}	" \
        "{offset_11}	" \
        "{mode_12}	" \
        "{l_o_13}               " \
        "{name_14}".format(**vars(self))

    @staticmethod
    def from_station(mem_chan, station):
        # NR    FREQ        STEP 0/+/- REV  PL/T PL/R DCS PL/T  PL/R DCS    OFFSET      MODE L/O            NAME
        # 002	00440400000	8	 1	   0	1	 0	  0	  18	08	 000	005000000	0	 0				IRLP NEP
        # frequency = attr.ib()
        # offset = attr.ib()
        # offset_direction = attr.ib()
        # tone = attr.ib()
        # location = attr.ib()
        # ST_PR = attr.ib()
        # county = attr.ib()
        # call = attr.ib()
        # use = attr.ib()
        freq_repr_1 = (station.frequency + "00").zfill(11)
        freq_hz = int(freq_repr_1)
        offset_direction = calc_offset_direction(station.offset_direction)
        return KenwoodChannelLine(
            nr_0=str(mem_chan).zfill(3),
            freq_repr_1=freq_repr_1,
            step_2=calc_step(freq_hz),
            offset_direction_3=offset_direction,
            pl_t_xmit_5=1 if offset_direction > 0 else 0,
            pl_r_9="08",
            pl_t_8=CTSS_OFFSET_LOOKUP.get(station.tone, "08"),
            dcs_freq_10="000",
            offset_11=str(cacl_tx_offset(freq_hz)).zfill(9),
            name_14=calc_name(station),
        )

def calc_step(hz):
    if is_70_cm_freq(hz):
        return '8'
    elif is_2_meter_freq(hz):
        return '0'
    elif is_6_meter_freq(hz):
        return '0'  # TODO, what is 6 meter step?
    elif is_33_cm_freq(hz):
        return '0'  # TODO, what is 33 cm step?
    else:
        raise UnknownBandError(hz)

def calc_offset_direction(direction):
    if not direction or direction.lower() == "n/a" or direction == "s":
        return 0
    elif direction == "+":
        return 1
    elif direction == "-":
        return 2
    else:
        raise ValueError("Unknown direction " + direction)

def calc_name(station):
    # TODO, shorted to 8 chars
    name = station.location.replace(",", "").strip()
    no_city_name = name.replace(station.city, "").strip()
    if no_city_name == "":
        return station.call
    return remove_vouls(no_city_name, 10)

VOULS = [
    "a", "e", "i", "o", "u"
]
def remove_vouls(name, max_size):
    if len(name) <= max_size:
        return name

    name = name.replace(" ", "")

    if len(name) <= max_size:
        return name

    while True:
        name_size = len(name)
        for voul in itertools.chain(VOULS, [v.upper() for v in VOULS]):
            name = name.replace(voul, "", 1)
            if len(name) <= max_size:
                return name
        if len(name) == name_size:
            raise Exception("Couldn't simplify name " + name)

