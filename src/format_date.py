from datetime import datetime

def convert_date(date):
    date_object = datetime.strptime(date.strip(),'%m/%d/%Y')
    return date_object.strftime('%m/%Y')