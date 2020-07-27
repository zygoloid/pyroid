#! /usr/bin/env python2.5
import sys
import os
import random
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pymunk-0.8.1.egg'))
import pymunk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyglet-1.1.2.egg'))
import pyglet
from pyglet.window import key
from pyglet import gl

from object import *
from groups import *

class Scripted(pyglet.event.EventDispatcher):
	def __init__(self, script):
		self.script = script
		self.action = None
		self.actionNext()

	def actionNext(self, result=None):
		if self.action: self.action.end(self)
		try:
			self.action = self.script.send(result)
		except StopIteration:
			self.dispatch_event('on_done')
			return
		self.action.begin(self)

class GameScene(Scene, Scripted):
	def __init__(self, level, **kw):
		Scene.__init__(self, **kw)
		self.level = level
		self.space = pymunk.Space()
		self.space.add_collisionpair_func(CollisionTypes.redShip, CollisionTypes.redEnemy, self.enemyHit)
		self.space.add_collisionpair_func(CollisionTypes.blueShip, CollisionTypes.blueEnemy, self.enemyHit)
		self.space.add_collisionpair_func(CollisionTypes.redShip, CollisionTypes.blueEnemy, self.shipHit)
		self.space.add_collisionpair_func(CollisionTypes.blueShip, CollisionTypes.redEnemy, self.shipHit)
		self.space.add_collisionpair_func(CollisionTypes.redShip, CollisionTypes.blueShip, self.shipShipHit)
		self.batch = pyglet.graphics.Batch()
		self.foreground = ForegroundGroup(Rect((0,0), (self.level.width,self.level.height)).expand(5))
		self.overlay = pyglet.graphics.Group()
		w, h = level.width, level.height
		self.redShip = Ship(parent=self, color=red, x=w/2.0+1, y=h/2.0,
		                    collisionType=CollisionTypes.redShip,
		                    controls=(key.UP, key.DOWN, key.LEFT, key.RIGHT))
		self.blueShip = Ship(parent=self, color=blue, x=w/2.0-1, y=h/2.0,
		                     collisionType=CollisionTypes.blueShip,
		                     controls=(key.W, key.S, key.A, key.D))
		self.objects = [self.redShip, self.blueShip]
		self.camera = Camera(self, self.foreground, self.objects[:])
		self.objects.append(self.camera)
		self.running = False
		self.walls = pymunk.Body(pymunk.inf, pymunk.inf)
		pts = [(-0.5,-0.5), (-0.5,h+0.5), (w+0.5,h+0.5), (w+0.5,-0.5)]
		for a, b in zip(pts, pts[1:] + [pts[0]]):
			rect = Rect(a, b).sort().expand(0.5)
			self.addWall(rect.a, rect.b)
			self.space.add_static(pymunk.Segment(self.walls, a, b, 0.0))
		self.soundShipHit = pyglet.resource.media('low parrp.wav', streaming=False)
		self.soundEnemyHit = pyglet.resource.media('beep.wav', streaming=False)
		self.soundShipShipHit = pyglet.resource.media('collision.wav', streaming=False)
		Scripted.__init__(self, level.run(self))

	def addWall(self, a, b):
		self.objects.append(Wall(parent=self, body=self.walls, a=a, b=b))

	def addEnemy(self, x, y, c, type=Hunter):
		color, target, enemy, collisionType = {
		  red: (darkRed, self.blueShip, self.redShip, CollisionTypes.redEnemy),
		  blue: (darkBlue, self.redShip, self.blueShip, CollisionTypes.blueEnemy)
		}[c]
		self.objects.append(type(parent=self, color=color, x=x, y=y,
		                         target=target, enemy=enemy,
		                         collisionType=collisionType))

	def addMessage(self, message):
		txt = Message(parent=self, message=message)
		self.objects.append(txt)
		return txt

	def update(self, dt):
		if not self.running:
			self.camera.update(dt)
			return
		if self.key_pressed(key.G):
			self.space.gravity = (random.uniform(-5,5), random.uniform(-5,5))
		for o in self.objects: o.update(dt)
		self.destroyed = set()
		self.space.step(dt)
		for d in self.destroyed:
			d.destroy()
		for o in self.objects:
			if isinstance(o, Enemy): break
		else:
			self.dispatch_event('on_level_end')
	
	def shipHit(self, ship, enemy, contacts, normal, data):
		self.soundShipHit.play()
		self.dispatch_event('on_dead')
		return False

	def shipShipHit(self, red, blue, contacts, normal, data):
		#self.soundShipShipHit.play()
		return True

	def enemyHit(self, ship, enemy, contacts, normal, data):
		self.soundEnemyHit.play()
		self.destroyed.add(enemy.owner)
		return False

	def render(self):
		self.batch.draw()

GameScene.register_event_type('on_level_end')
GameScene.register_event_type('on_dead')
GameScene.register_event_type('on_done')

class ApplicationWindow(pyglet.window.Window):
	def __init__(self):
		super(ApplicationWindow, self).__init__(fullscreen=True)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		self.set_mouse_visible(False)
		pyglet.clock.schedule_interval(self.update, 1/60.)
		pyglet.resource.path = ['sounds']
		pyglet.resource.reindex()
		self.music = pyglet.resource.media('music 1.wav', streaming=False)
		self.musicPlayer = pyglet.media.Player()
		self.musicPlayer.queue(self.music)
		self.musicPlayer.eos_action = pyglet.media.Player.EOS_LOOP
		self.musicPlayer.play()
		self.startLevel(1)

	def startLevel(self, level):
		self.level = level
		import levels
		self.scene = GameScene(window=self, level=levels.levels[self.level-1])
		self.scene.set_handlers(on_done=lambda: self.startLevel(level+1),
                                        on_dead=lambda: self.startLevel(level))

	def update(self, dt):
		if self.keys[key.ESCAPE]:
			pyglet.app.exit()
		self.scene.update(dt)

	def on_key_press(self, symbol, mods):
		if symbol == key.F:
			self.set_fullscreen(not self.fullscreen)
			return True
		if symbol == key.L:
			self.startLevel(self.level + 1)
			return True

	def on_draw(self):
		self.clear()
		self.scene.render()

def main(args):
	pymunk.init_pymunk()
	window = ApplicationWindow()
	pyglet.app.run()

if __name__ == '__main__':
	sys.exit(main(sys.argv))
