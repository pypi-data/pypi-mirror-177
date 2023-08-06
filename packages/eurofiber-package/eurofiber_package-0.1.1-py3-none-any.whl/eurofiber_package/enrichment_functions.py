import numpy as np

def segment(fte:float) -> str or float:
    """ this function returns the segment based on the number of fte """
    if np.isnan(fte):
        return np.nan
    else:
        if fte >= 250:
            return 'LE'
        elif 50 <= fte < 250:
            return 'SME Large'
        elif 10 <= fte < 50:
            return 'SME Small'
        else:
            return 'SOHO' 


# def sales_channel():


# def company_size():
