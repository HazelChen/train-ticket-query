#-*- coding:utf-8 -*-
import sys, time, pymysql
import config

class QueryDB:
	connection = None

	def connect(self):
		self.connection = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_table_name);

	def execute(self, sql, arguments):
		try:
			cursor = self.connection.cursor()
			cursor.execute(sql, arguments)
			self.connection.commit()
			cursor.close()
		except pymysql.err.OperationalError:
			self.connect()
			cursor = self.connection.cursor()
			cursor.execute(sql, arguments)
			self.connection.commit()
			cursor.close()

	def query(self, sql):
		try:
			cursor = self.connection.cursor()
			cursor.execute(sql)
			return cursor
		except pymysql.err.OperationalError:
			self.connect()
			cursor = self.connection.cursor()
			cursor.execute(sql)
			return cursor

	def close(self):
		self.connection.close()

	