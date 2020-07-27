#! /usr/bin/env python2.5
import pyglet
from pyglet import gl

from object import *

class Rect(object):
       def __init__(self, a, b):
               self.a, self.b = a, b
       def sort(self):
               return Rect((min(self.a[0], self.b[0]), min(self.a[1], self.b[1])),
                           (max(self.a[0], self.b[0]), max(self.a[1], self.b[1])))
       def shrink(self, k):
               return Rect((self.a[0] + k, self.a[1] + k),
                           (self.b[0] - k, self.b[1] - k))
       def expand(self, k): return self.shrink(-k)
       def width(self): return self.b[0] - self.a[0]
       def height(self): return self.b[1] - self.a[1]
       def fixAspect(self, w, h):
               if h * self.width() > w * self.height():
                       # not high enough
                       o = h * self.width() / w - self.height()
                       self.a = (self.a[0], self.a[1] - o/2)
                       self.b = (self.b[0], self.b[1] + o/2)
               else:
                       # not wide enough
                       o = w * self.height() / h - self.width()
                       self.a = (self.a[0] - o/2, self.a[1])
                       self.b = (self.b[0] + o/2, self.b[1])
       def __repr__(self):
               return "Rect(%s, %s)" % (self.a, self.b)

def intersection(r1, r2):
       return Rect((max(r1.a[0],r2.a[0]), max(r1.a[1], r2.a[1])),
                   (min(r1.b[0],r2.b[0]), min(r1.b[1], r2.b[1])))

def union(r1, r2):
       return Rect((min(r1.a[0],r2.a[0]), min(r1.a[1], r2.a[1])),
                   (max(r1.b[0],r2.b[0]), max(r1.b[1], r2.b[1])))


class Camera(object):
	def __init__(self, parent, group, tracked):
		self.parent = parent
		self.group = group
		self.tracked = tracked
		self.prev = self.group.rect
		self.group.rect.fixAspect(self.parent.window.width, self.parent.window.height)
	def update(self, dt):
		v = 6.0 # Max camera speed
		k = 5 # Border around tracked things
		shrunk = self.prev.shrink(dt * v)
		self.prev = reduce(union, [Rect((t.x-k,t.y-k),(t.x+k,t.y+k)) for t in self.tracked], shrunk)
		#self.group.rect = intersection(target, self.group.rect.expand(dt * v))
		self.group.rect = Rect(self.prev.a, self.prev.b)
		self.group.rect.fixAspect(self.parent.window.width, self.parent.window.height)

class ForegroundGroup(pyglet.graphics.Group):
	def __init__(self, rect, *a, **kw):
		pyglet.graphics.Group.__init__(self, *a, **kw)
		self.rect = rect
	def set_state(self):
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glPushMatrix()
		gl.glLoadIdentity()
		# left, right, bottom, top
		gl.gluOrtho2D(self.rect.a[0], self.rect.b[0],
		              self.rect.a[1], self.rect.b[1])
	def unset_state(self):
		gl.glPopMatrix()

class PositionedGroup(pyglet.graphics.Group):
	def __init__(self, getX, getY, getAngle, *a, **kw):
		pyglet.graphics.Group.__init__(self, *a, **kw)
		self.getX, self.getY, self.getAngle = getX, getY, getAngle
	def set_state(self):
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glPushMatrix()
		gl.glTranslatef(self.getX(), self.getY(), 0)
		gl.glRotatef(self.getAngle() * 360 / 6.283184, 0, 0, 1)
	def unset_state(self):
		gl.glPopMatrix()
