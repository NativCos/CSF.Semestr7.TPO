from ipaddress import IPv4Address


def is_valid_ipaddress(q):
    try:
        IPv4Address(q)
        return True
    except '':
        return False


def is_valid_mask(q):
    try:
        IPv4Address(q)
        return True
    except '':
        return False


def is_valid_marks(m_list):
    if len(m_list) > 10:
        return False
    for m in m_list:
        if len(m) > 16:
            return False
    return True


def is_valid_text(q):
    if len(q) > 10000:
        return False
    return True
