def format_number(num):
    """
    Convert numeric values to abbreviated forms (e.g., 1000 to 1k).
    """
    if num < 0:
        return '-' + format_number(-num)
    elif num < 1000:
        return str(num)
    elif num < 1e6:
        return '{:.1f}k'.format(num / 1e3)
    elif num < 1e9:
        return '{:.1f}M'.format(num / 1e6)
    elif num < 1e12:
        return '{:.1f}B'.format(num / 1e9)
    elif num < 1e15:
        return '{:.1f}T'.format(num / 1e12)
    else:
        return '{:.1e}'.format(num)
