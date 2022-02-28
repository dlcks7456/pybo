# import locale
# locale.setlocale(locale.LC_ALL, '')

def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)

# from datetime import datetime
# print(format_datetime(datetime.now()))