def safe_list_get(l_, idx=0, default=None):
    try:
        return l_[idx]
    except IndexError:
        return default
