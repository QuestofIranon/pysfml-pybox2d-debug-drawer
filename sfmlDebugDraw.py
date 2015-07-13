# pySFML Debug Draw for pyBox2d
#
# Copyright (C) 2015 "questofiranon" / https://github.com/QuestofIranon
# Box2D C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Box2D Python version Copyright (c) 2008 kne / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#  
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.


from math import floor
import sfml as sf
import Box2D
from Box2D import b2Draw, b2DrawExtended

class sfDebugDraw(b2Draw):

	def __init__(self, window, scale, **kwargs):
		
		super(sfDebugDraw, self).__init__()
		self.window = window
		self.scale = scale

	def StartDraw(self):
		self.window.clear(sf.Color.BLACK)

	def EndDraw(self):
		self.window.display()

	def DrawAABB(self, aabb, color):
		sfAABB = VertexArray(sf.graphics.PrimitiveType.LINES, 4)

		sfAABB[0] = sf.Vertex(self.B2VectoSFVec(aabb.lowerBound.x, aabb.lowerBound.y), self.ColorToSFML(color))
		sfAABB[1] = sf.Vertex(self.B2VectoSFVec(aabb.upperBound.x, aabb.lowerBound.y), self.ColorToSFML(color))
		sfAABB[2] = sf.Vertex(self.B2VectoSFVec(aabb.upperBound.x, aabb.upperBound.y), self.ColorToSFML(color))
		sfAABB[3] = sf.Vertex(self.B2VectoSFVec(aabb.lowerBound.x, aabb.upperBound.y), self.ColorToSFML(color))

		self.window.draw(sfAABB)

	def DrawPoint(self, p, size, color):

		point = sf.CircleShape((size/2) * self.scale)
		point.origin = ((size/2) * self.scale, (size/2) * self.scale)
		point.position = self.B2VectoSFVec(p)
		point.fill_color = self.ColorToSFML(color)
		
		self.window.draw(point)

	def DrawPolygon(self, vertices, color):
		
		polygon = sf.ConvexShape()

		polygon.point_count = len(vertices)

		point_index = 0
		for vertex in vertices:
			trans_vector = self.B2VectoSFVec(vertex)

			polygon.set_point(point_index, (floor(trans_vector.x), floor(trans_vector.y)))
			point_index = point_index + 1

		polygon.outline_thickness = 1.0
		polygon.fill_color = sf.Color.TRANSPARENT
		polygon.outline_color = self.ColorToSFML(color)

		self.window.draw(polygon)

	def DrawSolidPolygon(self, vertices, color):
		
		polygon = sf.ConvexShape()
		
		polygon.point_count = len(vertices)
		
		point_index = 0
		for vertex in vertices:
			trans_vector = self.B2VectoSFVec(vertex)

			polygon.set_point(point_index, (floor(trans_vector.x), floor(trans_vector.y)))
			point_index = point_index + 1

		polygon.outline_thickness = 1.0
		polygon.fill_color = self.ColorToSFML(color, 60)
		polygon.outline_color = self.ColorToSFML(color)

		self.window.draw(polygon)

	def DrawCircle(self, center, radius, color, drawwidth=1):

		circle = sf.CircleShape(radius * self.scale)
		circle.origin = radius * self.scale, radius * SCALE
		circle.position = self.B2VectoSFVec(center)
		circle.fill_color = sf.COLOR.TRANSPARENT
		circle.outline_thickness = drawwidth
		circle.outline_color = self.ColorToSFML(color)

		self.window.draw(circle)

	def DrawSolidCircle(self, center, radius, axis, color):

		circle = sf.CircleShape(radius * self.scale)
		circle.origin = radius * self.scale, radius * self.scale
		circle.position = self.B2VectoSFVec(center)
		circle.fill_color = self.ColorToSFML(color, 60)
		circle.outline_thickness = 1.0
		circle.outline_color = self.ColorToSFML(color)

		end_point = center + radius * axis

		line = sf.VertexArray(sf.graphics.PrimitiveType.LINES, 2)
		line[0] = sf.Vertex(self.B2VectoSFVec(center), self.ColorToSFML(color))
		line[1] = sf.Vertex(self.B2VectoSFVec(end_point), self.ColorToSFML(color))

		self.window.draw(circle)
		self.window.draw(line)

	def DrawSegment(self, p1, p2, color):

		line = sf.VertexArray(sf.graphics.PrimitiveType.LINES, 2)
		line[0] = sf.Vertex(self.B2VectoSFVec(p1), self.ColorToSFML(color))
		line[1] = sf.Vertex(self.B2VectoSFVec(p2), self.ColorToSFML(color))

		self.window.draw(line)

	def DrawTransform(self, xf):

		line_length = 0.4

		xAxis = xf.position + line_length * xf.R.Col1
		yAxis = xf.position + line_length * xf.R.Col2

		red_line = sf.VertexArray(sf.graphics.PrimitiveType.LINES, 2)
		red_line[0] = sf.Vertex(self.B2VectoSFVec(xf.position), sf.Color.RED)
		red_line[1] = sf.Vertex(self.B2VectoSFVec(xAxis), sf.Color.RED)

		green_line = sf.VertexArray(sf.graphics.PrimitiveType.LINES, 2)
		green_line[0] = sf.Vertex(self.B2VectoSFVec(xf.position), sf.Color.GREEN)
		green_line[1] = sf.Vertex(self.B2VectoSFVec(yAxis), sf.Color.GREEN)

		self.window.draw(red_line)
		self.window.draw(green_line)

	def ColorToSFML(self, color, alpha=255):
		return sf.Color((color.r * 255), (color.g * 255), (color.b * 255), alpha)

	def B2VectoSFVec(self, vector, scale_to_pixels=True):
		return sf.Vector2(vector[0] * (self.scale if scale_to_pixels else 1), (vector[1] * (self.scale if scale_to_pixels else 1)))

