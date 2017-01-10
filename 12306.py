#-*- coding:utf-8 -*-
import sys, getopt
import requests, socket
import station_code, seat_code
import mail

def print_usage():
	print('格式：python 12306.py -f 福州 -t 杭州 -d 2017-01-20')
	print('或：python 12306.py -f 福州 -t 杭州 -d 2017-01-20 -n D3343,G366')
	print('或：python 12306.py -f 福州 -t 杭州 -d 2017-01-20 -n D3343,G366 -s 一等座,无座')

# 获取参数
try:
	options,args = getopt.getopt(sys.argv[1:],"hf:t:d:n:s:",["help","from=", "to=", "date=", "number=", "seat="])
except getopt.GetoptError:
	print_usage()
	sys.exit()

# 参数获取
global from_station
global to_station
global query_date
try_times = 0
valid_trips = []
valid_seats = []

for option, arg in options:
	if option in ("-h", "help"):
		print_usage()
		sys.exit()
	if option in ("-f", "from"):
		from_station = station_code.code_map[arg]
	if option in ("-t", "to"):
		to_station = station_code.code_map[arg]
	if option in ("-d", "date"):
		query_date = arg
	if option in ("-n", "number"):
		valid_trips = arg.split(',')
	if option in ("-s", "seat"):
		valid_seats = arg.split(',')
		for num in range(len(valid_seats)):
			valid_seats[num] = seat_code.code_map[valid_seats[num]]
		print(valid_seats)

url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(query_date,from_station,to_station)
print(url)

def has_ticket(info):
	for number in range(len(info)):
		trip = info[number]['queryLeftNewDTO']
		trip_number = trip['station_train_code']
		# 如果不是想要的车次，那就跳过
		if len(valid_trips) != 0 and (trip_number not in valid_trips):
			continue

		for seat in seat_code.code_map.values():
			# 如果不是想要的座位，就跳过
			if len(valid_seats) != 0 and (seat not in valid_seats):
				continue
			seat_num = trip[seat];
			if seat_num == '有' or (seat_num.isdigit() and int(seat_num) > 0):
				return trip

	return False

while True:
	try_times = try_times + 1
	print('try ' + str(try_times) + ' times')
	try:
		result = requests.get(url,verify=False, timeout=30)   # 不用验证证书
	except socket.timeout:
		print('timeout')
		break
	except requests.exceptions.ReadTimeout:
		print('timeout')
		break

	info = result.json()  # 转换json格式
	if info['status'] and 'data' in info.keys():
		ticket_result = has_ticket(info['data'])
		if ticket_result:
			print('有票啦！车次号：')
			print(ticket_result)
			mail.email(ticket_result)
			break;

	else:
		print(info)
		break;

