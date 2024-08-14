
class Validate:
	def __init__(self):
		pass

	@classmethod
	def isSet(cls, value):
		data = False	
		try:
			if value is None:
				data = False	
			else:
				data = True	
		except ValueError:
			raise ValueError('invalid value provided')	
		except Exception as e:
			raise e
		finally:
			return data
	
	@classmethod
	def isEmpty(cls, value):
		data = True 
		try:
			if value is None:
				data = True
			else:
				data = not bool(float(value))
		except ValueError:
			raise ValueError("invalid value provided")
		except Exception as e:
			raise e
		finally:
			return data
	
	@classmethod
	def isDigit(self, value, min_allowed = 1):
		try:
			value = int(value)
			if value is None or value=="" or value < min_allowed:
				raise ValueError("invalid value provided")

		except ValueError:
			raise ValueError("invalid value provided")

		except Exception as e:
			raise e

	@classmethod
	def isValidString(self, value):
		try:
			value = str(value)
			value = value.strip()
			if bool(value) is False:
				raise ValueError("invalid value provided")

		except ValueError:
			raise ValueError("invalid value provided")

		except Exception as e:
			raise e
