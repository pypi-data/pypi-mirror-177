import webbrowser

class SearchMixin(_SearchMixin, metaclass=ConflictCheck):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
