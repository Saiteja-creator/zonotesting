from datetime import datetime,timedelta

current_date = datetime.now()


last_month_date = current_date - timedelta(days=current_date.day)


formatted_last_month_date = last_month_date.replace(day=current_date.day, hour=0, minute=0, second=0).strftime("%Y-%m-%d")


formatted_date = datetime.now().strftime("%Y-%m-%d")

