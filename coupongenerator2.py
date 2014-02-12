import random
import os
import base64
from ConfigParser import SafeConfigParser


class CouponGenerator( object ):
	"""A factory class which creates a CouponList object, based on the specifications
	   defined in the configuration file. This configuration file is specified as a
	   parameter (filename).		

	"""
	def __init__( self , filename ):
		"""Initializes factory whith settings from specified config file"""
		self.config = {}
		parser = SafeConfigParser()
		found = parser.read(filename)
		if not found:
			raise ValueError('Configuration file not found!')
		for section in parser.sections():
			for key, value in parser.items(section):
				self.config[key] = value

	def newList( self ):
		"""Factory object creation method"""
		if self.config['algorithm'] == "simple":
			strategy = SimpleCouponList()
		else:		
			strategy = SecureCouponList()
		
		return CouponList(strategy, self.config["quantity"] , self.config["length"])

class CouponList( object ):
	"""A base class that holds the coupon list as well as a methods for generating the list and for printing it out to standard output"""
	def __init__( self, strategy , quantity , length ):
		self.strategy = strategy
		self.quantity = int(quantity)
		self.length = int(length)
		self.list = None

	def generateList( self ):
		self.list = self.strategy.generateList( self.quantity, self.length )
		self.printCouponList()

	def printCouponList( self ):
		for coupon in self.list:
			print(coupon)

class CouponStrategy ( object ):
	"""Superclass that defines the generateList method that all its subclasses must override."""
	def generateList( self ):
		raise NotImplementedError

class SimpleCouponList( CouponStrategy ):
	"""Simple coupon list generation strategy class."""
	def generateList( self, quantity , length):		
		coupons = []		
		chars = "0123456789abcdefghijklmnopqrst"
		while len(coupons) < quantity:
			coupon = ""
			for i in range(0,length):
				slice_start = random.randint(0, len(chars) - 1)
				coupon += chars[slice_start: slice_start +1]
				
			if coupon not in coupons:
				coupons.append(coupon)

		return coupons

class SecureCouponList ( CouponStrategy ):
	"""A more secure strategy for coupon list generation."""
	def generateList( self, quantity , length):
		coupons = []
		while len(coupons) < quantity:
			token = os.urandom(length)		
			coupon = base64.b64encode(token)

			if coupon not in coupons:
				coupons.append(coupon)
		return coupons

if __name__ == '__main__':
	generator = CouponGenerator("config.ini")
	generator.newList().generateList()
	

	
	