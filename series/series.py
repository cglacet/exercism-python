def slices(series, length):
    if not (0 < length <= len(series)):
        raise ValueError("Length needs to be in [1,{}], you asked for {} which lies outside this range.".format(len(series), length))
    return [ series[i:i+length] for i in range(1+len(series)-length) ]
