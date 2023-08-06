import webbrowser

class Line(TipableVMobject):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class LineExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class DashedLine(Line):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    """A dashed :class:`Line`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Arguments to be passed to :class:`Line`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dash_length : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dashed_ratio : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`Line`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`~.DashedVMobject`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class DashedLineExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class TangentLine(Line):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    """Constructs a line tangent to a :class:`~.VMobject` at a specific point.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    vmob : :class:`~.VMobject`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    alpha : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    length : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    d_alpha: :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`Line`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class TangentLineExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Elbow(VMobject):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    width : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    angle : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`~.VMobject`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`RightAngle`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ElbowExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Arrow(Line):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Arguments to be passed to :class:`Line`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    stroke_width : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    buff : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    max_tip_length_to_length_ratio : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    max_stroke_width_to_length_ratio : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`Line`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`ArrowTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`CurvedArrow`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ArrowExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ArrowExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Vector(Arrow):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    direction : Union[:class:`list`, :class:`numpy.ndarray`]
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    buff : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`Arrow`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class VectorExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            Additional arguments to be passed to :class:`~.Matrix`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`~.Matrix`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class VectorCoordinateLabel(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class DoubleArrow(Arrow):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Arguments to be passed to :class:`Arrow`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Additional arguments to be passed to :class:`Arrow`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`.~ArrowTip`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`.~CurvedDoubleArrow`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class DoubleArrowExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class DoubleArrowExample2(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Angle(VMobject):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        The radius of the :class:`Arc`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    quadrant : Sequence[:class:`int`]
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        A sequence of two :class:`int` numbers determining which of the 4 quadrants should be used.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dot : :class:`bool`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Allows for a :class:`Dot` in the arc. Mainly used as an convention to indicate a right angle.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dot_radius : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        The radius of the :class:`Dot`. If not specified otherwise, this radius will be 1/10 of the arc radius.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dot_distance : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    dot_color : :class:`~.Colors`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        The color of the :class:`Dot`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    elbow : :class:`bool`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Produces an elbow-type mobject indicating a right angle, see :class:`RightAngle` for more information
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Further keyword arguments that are passed to the constructor of :class:`Arc` or :class:`Elbow`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class RightArcAngleExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class AngleExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class FilledAngle(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        """Get the lines forming an angle of the :class:`Angle` class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`~.VGroup`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            A :class:`~.VGroup` containing the lines that form the angle of the :class:`Angle` class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        """Get the value of an angle of the :class:`Angle` class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            The value in degrees/radians of an angle of the :class:`Angle` class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class GetValueExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            Further keyword arguments are passed to :class:`.Angle`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class AngleFromThreePointsExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class RightAngle(Angle):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        Further keyword arguments that are passed to the constructor of :class:`Angle`.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class RightAngleExample(Scene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
