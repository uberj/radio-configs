def is_2_meter_freq(freq):
    return freq >= 114100000 and freq <= 148000000

def is_6_meter_freq(freq):
    return freq >= 50000000 and freq <= 54000000

def is_70_cm_freq(freq):
    return freq >= 420000000 and freq <= 450000000

def is_33_cm_freq(freq):
    return freq >= 902000000 and freq <= 928000000

def cacl_tx_offset(freq):
    if is_70_cm_freq(freq):
        return 5000000
    elif is_33_cm_freq(freq):
        return 0 # TODO, what is 33 cm offset?
    elif is_2_meter_freq(freq):
        return 600000
    elif is_6_meter_freq(freq):
        return 0 # TODO, what is 6 meter offset?
    else:
        raise UnknownBandError("unkown band for frequency: " + str(freq))

class UnknownBandError(ValueError):
    pass
