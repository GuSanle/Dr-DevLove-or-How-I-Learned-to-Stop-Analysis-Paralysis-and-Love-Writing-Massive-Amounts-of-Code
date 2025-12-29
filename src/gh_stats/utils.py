import datetime
import re

def parse_relative_date(date_str):
    """
    Parse relative dates like 'today-2days', 'now-1week', '3days'.
    Returns a datetime.date object.
    """
    today = datetime.date.today()
    if date_str == 'today' or date_str == 'now':
        return today
    
    # Simple N[days|weeks|months|years] (e.g. "3days" -> 3 days ago)
    simple_match = re.match(r'^(\d+)(day|week|month|year)s?$', date_str)
    if simple_match:
        num = int(simple_match.group(1))
        unit = simple_match.group(2)
        if unit == 'day': delta = datetime.timedelta(days=num)
        elif unit == 'week': delta = datetime.timedelta(weeks=num)
        elif unit == 'month': delta = datetime.timedelta(days=num*30) # approx
        elif unit == 'year': delta = datetime.timedelta(days=num*365) # approx
        return today - delta

    # yt-dlp style: (today|now)-N[unit]
    match = re.match(r'^(today|now)([-+])(\d+)(day|week|month|year)s?$', date_str)
    if match:
        op = match.group(2)
        num = int(match.group(3))
        unit = match.group(4)
        
        if unit == 'day': delta = datetime.timedelta(days=num)
        elif unit == 'week': delta = datetime.timedelta(weeks=num)
        elif unit == 'month': delta = datetime.timedelta(days=num*30)
        elif unit == 'year': delta = datetime.timedelta(days=num*365)
        
        if op == '-': return today - delta
        else: return today + delta
        
    raise ValueError(f"Unknown date format: {date_str}")

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
    
    # Try parsing as relative date (e.g. "3days")
    try:
        start = parse_relative_date(range_str)
        return start, today
    except ValueError:
        pass
        
    raise ValueError(f"Unknown range: {range_str}")
