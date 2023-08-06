import webbrowser

r"""A collection of tip mobjects for use with :class:`~.TipableVMobject`."""
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowTip(VMobject):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    r"""Base class for arrow tips.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowTriangleTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowTriangleFilledTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowCircleTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowCircleFilledTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowSquareTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowSquareFilledTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        NotImplementedError: Has to be implemented in inheriting subclasses.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        >>> class MyCustomArrowTip(ArrowTip, RegularPolygon):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        >>> class CustomTipExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    Using a class inherited from :class:`ArrowTip` to get a non-filled
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ArrowTipsShowcase(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        raise NotImplementedError("Has to be implemented in inheriting subclasses.")
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowTriangleTip(ArrowTip, Triangle):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowTriangleFilledTip(ArrowTriangleTip):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowCircleTip(ArrowTip, Circle):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowCircleFilledTip(ArrowCircleTip):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowSquareTip(ArrowTip, Square):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class ArrowSquareFilledTip(ArrowSquareTip):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
