# -*- coding: UTF-8 -*-
import sys, getopt, pymysql
import config, station_code, seat_code

def print_usage():
    print('格式：python add_queriers.py -f 福州 -t 杭州 -d 2017-01-20')
    print('或：python add_queriers.py -f 福州 -t 杭州 -d 2017-01-20 -n D3343,G366')
    print('或：python add_queriers.py -f 福州 -t 杭州 -d 2017-01-20 -n D3343,G366 -s 一等座,无座')

# 获取参数
try:
    options,args = getopt.getopt(sys.argv[1:],"hf:t:d:n:s:",["help","from=", "to=", "date=", "number=", "seat="])
except getopt.GetoptError:
    print_usage()
    sys.exit()

# 参数获取
from_station = None
to_station = None
query_date = None
valid_trips = None
valid_seats = None

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
        valid_trips = arg
    if option in ("-s", "seat"):
        valid_seats = arg.split(',')
        for num in range(len(valid_seats)):
            valid_seats[num] = seat_code.code_map[valid_seats[num]]
        valid_seats = ','.join(valid_seats)

#将con设定为全局连接
db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_table_name);
with db:
    #获取连接的cursor，只有获取了cursor，我们才能进行各种操作
    cursor = db.cursor()
    cursor.execute("INSERT INTO trainquery.querylist (`from`, `to`, `date`, `number`, `seat`, `status`) VALUES (%s, %s, %s, %s, %s, DEFAULT)", [from_station, to_station, query_date, valid_trips, valid_seats])