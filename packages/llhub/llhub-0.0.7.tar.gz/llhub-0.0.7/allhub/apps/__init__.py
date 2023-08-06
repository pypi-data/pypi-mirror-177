import webbrowser

class AppsMixin(AppMixin, InstallationMixin, metaclass=ConflictCheck):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
