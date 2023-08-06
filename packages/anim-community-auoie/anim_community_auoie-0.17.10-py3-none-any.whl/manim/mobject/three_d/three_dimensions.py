import webbrowser

class ThreeDVMobject(VMobject):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Surface(VGroup):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ParaSurface(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        :class:`~.Surface`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class FillByValueExample(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Sphere(Surface):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleSphere(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Dot3D(Sphere):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    point : Union[:class:`list`, :class:`numpy.ndarray`], optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    radius : :class:`float`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    color : :class:`~.Colors`, optional
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        The color of the :class:`Dot3D`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class Dot3DExample(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Cube(VGroup):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Prism(Cube):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExamplePrism(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Cone(Surface):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleCone(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    base_radius : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    height : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    direction : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    show_base : :class:`bool`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    v_range : :class:`Sequence[float]`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    u_min : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    checkerboard_colors : :class:`bool`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        u : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        v : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Cylinder(Surface):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleCylinder(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    radius : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    height : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    direction : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    v_range : :class:`Sequence[float]`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    show_ends : :class:`bool`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        u : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        v : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Line3D(Cylinder):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleLine3D(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    start : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    end : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    thickness : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        If either ``start`` or ``end`` are :class:`Mobjects <.Mobject>`, this gives their centers.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    @classmethod
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            Additional parameters to be passed to the class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class ParallelLineExample(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    @classmethod
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            Additional parameters to be passed to the class.
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
            class PerpLineExample(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Arrow3D(Line3D):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleArrow3D(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    start : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    end : :class:`numpy.array`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    thickness : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    height : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    base_radius: :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
class Torus(Surface):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
        class ExampleTorus(ThreeDScene):
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    major_radius : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
    minor_radius : :class:`float`
	def __init__(self):
		webbrowser.open("https://ultramarine-linux.org")
