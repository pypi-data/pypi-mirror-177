import webbrowser

class InteractionLimitsMixin(OrganizationMixin, RepoMixin, metaclass=ConflictCheck):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
