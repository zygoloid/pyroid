#! /usr/bin/env python2.5
import sys
import os
import random
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pymunk-0.8.1.egg'))
import pymunk

import pyglet
from pyglet.window import key
from pyglet import gl

from groups import *

class CollisionTypes:
	redShip = 1
	redEnemy = 2
	blueShip = 3
	blueEnemy = 4

def addCircle(batch, group, color, npoints=20):
	points = [(0.5 * math.sin(theta), 0.5 * math.cos(theta))
		  for k in range(0, npoints) for theta in [k * 2 * math.pi / npoints]]
	return batch.add(npoints, pyglet.gl.GL_POLYGON, group,
			 ('v2f/static', sum(points, ())),
			 ('c3B/static', npoints * color))

def rectanglePoints(a, b):
	return [a, (a[0],b[1]), b, (b[0],a[1])]

def addRectangle(batch, group, a, b, color):
	return batch.add(4, pyglet.gl.GL_QUADS, group,
	                 ('v2f/static', sum(rectanglePoints(a, b), ())),
	                 ('c3B/static', 4 * color))

def addStar(batch, group, color):
	points = [(r * math.sin(theta), r * math.cos(theta))
	          for k in range(0, 10) for theta in [k * 2 * math.pi / 10.0]
	          for r in [(k%2) * 0.25 + 0.25]]
	return batch.add(10, pyglet.gl.GL_POLYGON, group,
	                 ('v2f/static', sum(points, ())),
	                 ('c3B/static', 10 * color))

class Object(object):
	def __init__(self, parent, color, collisionType, x, y, shape = addCircle, **kw):
		super(Object, self).__init__(**kw)
		self.parent = parent
		self.color = color
		self.body = pymunk.Body(1.0, 1.0)
		self.shape = pymunk.Circle(self.body, 0.5, (0,0))
		self.shape.elasticity = 1.0
		self.shape.friction = 0.5
		self.shape.owner = self
		self.body.position = (x, y)
		self.body.angular_velocity = random.uniform(-3,3)
		self.shape.collision_type = collisionType
		self.parent.space.add(self.body, self.shape)
		self.group = PositionedGroup(self._getX, self._getY, self._getAngle, parent=self.parent.foreground)
		self.prim = shape(self.parent.batch, self.group, self.color)
	
	def _getX(self): return self.body.position[0]
	def _getY(self): return self.body.position[1]
	def _getAngle(self): return self.body.angle
	x = property(_getX, lambda self, v: self.body.position.__setitem__(0, v))
	y = property(_getY, lambda self, v: self.body.position.__setitem__(1, v))

	def key_pressed(self, key): return self.parent.key_pressed(key)
	def update(self, dt): pass
	def destroy(self):
		self.parent.space.remove(self.body, self.shape)
		self.prim.delete()
		self.parent.objects.remove(self)

	def resetForce(self):
		self.body.reset_forces()
		vx, vy = self.body.velocity
		f = -1
		self.body.apply_force((vx*f, vy*f), (0,0))
	def setForce(self, ax, ay):
		a = 10
		m = mod(ax, ay)
		if m:
			ax *= a / m
			ay *= a / m
		self.body.apply_force((ax,ay), (0,0))

class Ship(Object):
	def __init__(self, controls, **kw):
		super(Ship, self).__init__(**kw)
		self.controls = controls

	def update(self, dt):
		accel = { (False, False): 0, (False, True): 1, (True, False): -1, (True, True): 0 }
		ay = accel[self.key_pressed(self.controls[1]), self.key_pressed(self.controls[0])]
		ax = accel[self.key_pressed(self.controls[2]), self.key_pressed(self.controls[3])]
		self.resetForce()
		self.setForce(ax, ay)

class Enemy(Object):
	pass

class Hunter(Enemy):
	def __init__(self, target, enemy, **kw):
		super(Hunter, self).__init__(**kw)
		self.target = target

	def update(self, dt):
		self.resetForce()
		self.setForce(self.target.x - self.x, self.target.y - self.y)

class Dodger(Enemy):
	def __init__(self, target, enemy, **kw):
		super(Dodger, self).__init__(shape=addStar, **kw)
		self.target = target
		self.enemy = enemy

	def update(self, dt):
		self.resetForce()
		tx, ty = self.target.x - self.x, self.target.y - self.y
		ex, ey = self.enemy.x - self.x, self.enemy.y - self.y
		dt = mod(tx, ty)
		de = mod(ex, ey)
		self.setForce(tx / (dt ** 5) - ex / (de ** 5),
		              ty / (dt ** 5) - ey / (de ** 5))

class Wall(object):
	def __init__(self, parent, body, a, b):
		shape = pymunk.Poly(body, rectanglePoints(a, b), (0,0))
		shape.friction = 1.0
		parent.space.add_static(shape)
		addRectangle(parent.batch, parent.foreground, a, b, (255,255,255))
	def update(self, dt): pass

class Message(object):
	def __init__(self, parent, message):
		self.parent = parent
		self.label = pyglet.text.Label(text=message, x=10, y=10, font_size=72, batch=parent.batch, group=parent.overlay)
	def update(self, dt): pass
	def destroy(self):
		self.label.delete()
		self.parent.objects.remove(self)

class Scene(pyglet.event.EventDispatcher):
	def __init__(self, window):
		self.window = window

	def key_pressed(self, key):
		return self.window.keys[key]

	def update(self, dt):
		pass

red = (255,0,0)
blue = (0,0,255)

darkRed = (128,0,0)
darkBlue = (0,0,128)

def mod(x,y): return math.sqrt(x*x+y*y)
def collides(a, b): return mod(a.x - b.x, a.y - b.y) < 1
