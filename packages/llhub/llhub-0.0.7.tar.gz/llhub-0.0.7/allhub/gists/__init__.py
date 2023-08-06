import webbrowser

class GistMixin(_GistMixin, GistCommentsMixin):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
