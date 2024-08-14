class Convert:
    def __init__(self):
        pass
    
    @classmethod
    def toInt(cls, value):
        data = 0
        try:
            data = int(value)
            return data
        except ValueError:
            raise e
        except Exception as e:
            raise e
        finally:
            return data