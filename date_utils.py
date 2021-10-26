from datetime import datetime, timedelta
import pandas_market_calendars as mcal

'''
Return a range of dates from date_from to date_to,
with a 1-day interval.
cal_restrict: MarketCalendar object to restrict range
to valid_days of.

Inclusive of start_date AND end_date.
'''
def date_range(
	start_date: datetime, 
	end_date: datetime, 
	cal_restrict: mcal.MarketCalendar=None
	):
	start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
	end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
	assert start_date < end_date
	restrict = False
	if cal_restrict:
		restrict = True
		valid_days = cal_restrict.valid_days(start_date, end_date)
	#print(valid_days)
	days = (end_date - start_date).days + 1
	dates = []
	for n in range(days):
		date = start_date + timedelta(days=n)
		# The equality check inside the "in" is fine since we 
		# made sure to 0 the time fields of start and end dates
		if not restrict or date in valid_days:
			dates.append(date)
	return dates


# Example usage
if __name__ == '__main__':
	print(date_range(datetime(2010, 1, 1), datetime(2010, 2, 1), mcal.get_calendar('NYSE')))