#-*- coding:utf-8 -*-
import sys, getopt, time
import requests, socket
import station_code, seat_code
import mail
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s  %(levelname)s %(message)s',
                datefmt='%Y %b %d %H:%M:%S',
                filename='12306.log',
                filemode='a')

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

url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(query_date,from_station,to_station)

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
	
	query_begin_time = time.time()

	# 获取数据
	try:
		result = requests.get(url, verify=False, timeout=600)   # 不用验证证书
	except socket.timeout:
		mail.email('服务停止，12306返回超时')
		logging.error('timeout')
		break
	except requests.exceptions.ReadTimeout:
		mail.email('服务停止，12306返回超时')
		logging.error('timeout')
		break

	# 转换json格式
	try:
		info = result.json()
	except ValueError:
		mail.email('服务停止，12306返回了奇怪的结果, json无法解析:' + str(result))
		logging.error('ValueError: No JSON object could be decoded, value=' + str(result))
		break  

	# 日志
	query_end_time = time.time()
	try_times = try_times + 1
	logging.info(str(try_times) + ' times trying, take time: ' + str(query_end_time - query_begin_time) + 's')

	if info['status'] and 'data' in info.keys():
		ticket_result = has_ticket(info['data'])
		if ticket_result:
			logging.info('Get it!')
			logging.info(ticket_result)
			mail.email(ticket_result)
			break;

	else:
		logging.error('Error!!' + info)
		break;

