import webbrowser

class ReversibleLayer(base.Layer):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ReversibleSwap(ReversibleLayer, cb.Swap):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ReversibleSerial(ReversibleLayer, cb.Serial):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
