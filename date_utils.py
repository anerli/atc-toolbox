from datetime import datetime, timedelta
import pandas_market_calendars as mcal

'''
Return a range of dates from date_from to date_to,
with a 1-day interval.
cal_restrict: MarketCalendar object to restrict range
to valid_days of.
'''
def date_range(
	start_date: datetime, 
	end_date: datetime, 
	cal_restrict: mcal.MarketCalendar=None
	):
	restrict = False
	if cal_restrict:
		restrict = True
		valid_days = cal_restrict.valid_days(start_date, end_date)
	print(valid_days)
	days = (end_date - start_date).days
	dates = []
	for n in range(days):
		date = start_date + timedelta(days=n)
		# FIXME: Potential problem if date has time attributes, wont equal any valid days.
		if not restrict or date in valid_days:
			dates.append(date)
	return dates


if __name__ == '__main__':
	print(date_range(datetime(2010, 1, 1), datetime(2010, 2, 1), mcal.get_calendar('NYSE')))