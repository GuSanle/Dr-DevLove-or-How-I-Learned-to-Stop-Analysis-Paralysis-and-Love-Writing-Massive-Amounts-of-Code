import datetime

def parse_date_range(range_str):
    today = datetime.date.today()
    if range_str == 'today':
        return today, today
    elif range_str == 'week':
        start = today - datetime.timedelta(days=today.weekday())
        return start, today
    elif range_str == 'month':
        return today.replace(day=1), today
    elif range_str == 'quarter':
        quarter_month = ((today.month - 1) // 3) * 3 + 1
        return today.replace(month=quarter_month, day=1), today
    elif range_str == 'year':
        return today.replace(month=1, day=1), today
    else:
        raise ValueError(f"Unknown range: {range_str}")
