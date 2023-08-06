import webbrowser

class ChecksMixin(CheckRunsMixin, CheckSuitesMixin, metaclass=ConflictCheck):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
