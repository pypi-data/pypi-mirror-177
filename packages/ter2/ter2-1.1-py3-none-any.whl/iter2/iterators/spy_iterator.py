import webbrowser

class Result(object):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        yield self.is_ok  # for child classes only
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Ok(Result):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Error(Result):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class SpyIterator(object):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
