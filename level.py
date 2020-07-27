from game import red, blue, Hunter, Dodger

def setScene(s):
	global scene
	scene = s

class Level(object):
	def __init__(self, width, height, fn):
		self.width = width
		self.height = height
		self.fn = fn
	
	def run(self, scene):
		iter = self.fn(scene)
		v = None
		while True:
			setScene(scene)
			v = yield iter.send(v)

def level(width, height): return lambda fn: Level(width, height, fn)

class Action(object):
	def begin(self, scene): pass
	def end(self, scene): pass
	def done(self, result=None):
		scene.actionNext(result)

class WaitAction(Action):
	def begin(self, scene):
		self.wasRunning = scene.running
		scene.running = False
		self.key_press_handler = lambda a,b: self.done()
		scene.window.push_handlers(on_key_press=self.key_press_handler)
	def end(self, scene):
		scene.running = self.wasRunning
		scene.window.remove_handlers(on_key_press=self.key_press_handler)

class StartAction(Action):
	def begin(self, scene):
		scene.running = True
		scene.push_handlers(on_level_end=self.done)

class MessageAction(WaitAction):
	def __init__(self, message):
		self.message = message
	def begin(self, scene):
		WaitAction.begin(self, scene)
		self.txt = scene.addMessage(self.message)
	def end(self, scene):
		self.txt.destroy()
		WaitAction.end(self, scene)

class ChainActions(Action):
	def __init__(self, *a):
		self.actions = a
		self.pos = 0
	def begin(self, scene):
		self.scene = scene
		self.beginInner()
	def beginInner(self):
		self.actions[self.pos].done = self.next
		self.actions[self.pos].begin(self.scene)
	def endInner(self):
		self.actions[self.pos].end(self.scene)
	def next(self):
		self.endInner()
		self.pos += 1
		if self.pos < len(self.actions):
			self.beginInner()
		else:
			self.done()

wait = WaitAction
def start(): return ChainActions(WaitAction(), StartAction())
message = MessageAction
