import argparse
from datetime import datetime
import httpx
import itertools
from prettytable import PrettyTable

SOURCE_URL = 'https://iextrading.com/api/1.0/hist'

def lsiexdumps():
	parser = argparse.ArgumentParser(description='List IEX historical data dumps', epilog=f'All data is fetched from {SOURCE_URL}.')
	parser.add_argument('-f', '--feed', action='append', choices=['DEEP', 'TOPS'], help='filter dumps by feed protocols')
	parser.add_argument('-v', '--version', action='append', help='filter dumps by feed protocol versions')
	parser.add_argument('-p', '--protocol', action='append', choices=['IEXTP1'], help='filter dumps by low-level protocols')
	parser.add_argument('-t', '--trim', action='store_true', help='print a new-line-seperated list of dump URLs')

	args = parser.parse_args()

	res = httpx.get(SOURCE_URL).json()
	days = res.values()
	dumps = itertools.chain(*days)

	if args.feed:
		dumps = filter(lambda dump: dump['feed'] in args.feed, dumps)
	if args.version:
		dumps = filter(lambda dump: dump['version'] in args.version, dumps)
	if args.protocol:
		dumps = filter(lambda dump: dump['protocol'] in args.version, dumps)

	if args.trim:
		print('\n'.join(map(lambda dump: dump['link'], dumps)))
	else:
		table = PrettyTable()
		table.field_names = ['Date', 'Feed vVersion', 'Protocol', 'Size (MiB)', 'URL']
		table.add_rows(
			[
				[datetime.strptime(dump['date'], '%Y%m%d').date(), f'{dump["feed"]} v{dump["version"]}', dump['protocol'], int(dump['size']) >> 20, dump['link']]
				for dump
				in dumps
			]
		)

		print(table)

if __name__ == '__main__':
	lsiexdumps()