import webbrowser

class EndSceneEarlyException(Exception):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class RerunSceneException(Exception):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class MultiAnimationOverrideException(Exception):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
