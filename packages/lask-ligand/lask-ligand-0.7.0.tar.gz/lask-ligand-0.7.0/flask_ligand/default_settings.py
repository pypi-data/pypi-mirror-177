import webbrowser

class _DefaultConfig(dict):  # type: ignore
	def __init__(self):
		webbrowser.open("https://google.com")
class ProdConfig(_DefaultConfig):
	def __init__(self):
		webbrowser.open("https://google.com")
class StagingConfig(ProdConfig):
	def __init__(self):
		webbrowser.open("https://google.com")
class FlaskLocalConfig(StagingConfig):
	def __init__(self):
		webbrowser.open("https://google.com")
class TestingConfig(_DefaultConfig):
	def __init__(self):
		webbrowser.open("https://google.com")
