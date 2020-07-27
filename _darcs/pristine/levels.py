from level import *

@level(32, 24)
def level1(scene):
	scene.addEnemy(2, 12, blue)
	scene.addEnemy(30, 12, red)
	yield message('Hello!')
	yield start()

@level(32, 24)
def level2(scene):
	scene.addEnemy(2, 12, red)
	scene.addEnemy(30, 12, blue)
	yield start()

@level(32, 24)
def level3(scene):
	for y in 6,8,10,12,14,16,18:
		scene.addEnemy(2, y, blue)
		scene.addEnemy(30, y, red)
	scene.addWall((10,6), (11,18))
	scene.addWall((21,6), (22,18))
	yield start()

@level(32, 24)
def level4(scene):
	for y in 6,8,10,12,14,16,18:
		scene.addEnemy(2, y, red)
		scene.addEnemy(30, y, blue)
	scene.addWall((10,6), (11,18))
	scene.addWall((21,6), (22,18))
	yield start()

@level(32, 24)
def level5(scene):
	for n, y in enumerate((6,8,10,12,14,16,18)):
		scene.addEnemy(2, y, (n%2) and blue or red)
		scene.addEnemy(30, y, (n%2) and red or blue)
	scene.addWall((10,6), (11,18))
	scene.addWall((21,6), (22,18))
	yield start()

@level(32, 24)
def level5a(scene):
	scene.addEnemy(2, 12, blue, type=Dodger)
	scene.addEnemy(30, 12, red, type=Dodger)
	yield start()

@level(26, 12)
def level6(scene):
	for x in range(2,25,6):
		scene.addWall((x,0), (x+1,10))
	for x in range(5,25,6):
		scene.addWall((x,2), (x+1,12))
	scene.addEnemy(0.5, 0.5, red)
	scene.addEnemy(25.5, 11.5, blue)
	scene.redShip.x = 12.5
	scene.blueShip.x = 13.5
	yield start()

@level(26, 12)
def level7(scene):
	for x in range(2,25,6):
		scene.addWall((x,0), (x+1,10))
	for x in range(5,25,6):
		scene.addWall((x,2), (x+1,12))
	for y in range(1,10):
		scene.addEnemy(0.5, y+0.5, red)
		scene.addEnemy(25.5, y+0.5, blue)
	scene.redShip.x = 12.5
	scene.blueShip.x = 13.5
	yield start()

@level(26, 12)
def level8(scene):
	for x in range(2,25,6):
		scene.addWall((x,0), (x+1,10))
	for x in range(5,25,6):
		scene.addWall((x,2), (x+1,12))
	for y in range(1,10):
		if y % 2:
			scene.addEnemy(0.5, y+0.5, red)
			scene.addEnemy(25.5, y+0.5, blue)
		else:
			scene.addEnemy(0.5, y+0.5, blue)
			scene.addEnemy(25.5, y+0.5, red)
	scene.redShip.x = 12.5
	scene.blueShip.x = 13.5
	yield start()

@level(32, 24)
def level9(scene):
	for x in range(1,10):
		for y in range(1,10):
			if x < 5 and y < 5:
				scene.addEnemy(x+0.5, y+0.5, blue)
				scene.addEnemy(31.5-x, 23.5-y, red)
			elif x < 6 and y < 6:
				pass
			elif x < 9 and y < 9:
				scene.addEnemy(x+0.5, y+0.5, red)
				scene.addEnemy(31.5-x, 23.5-y, blue)
	scene.addWall((5,1), (6,6))
	scene.addWall((1,5), (5,6))
	scene.addWall((9,1), (10,10))
	scene.addWall((1,9), (9,10))

	scene.addWall((26,18), (27,23))
	scene.addWall((27,18), (31,19))
	scene.addWall((22,14), (23,23))
	scene.addWall((23,14), (31,15))

	yield start()

@level (40, 40)
def level10(scene):
	scene.addWall((4,4), (5,16))
	scene.addWall((4,4), (16,5))
	
	scene.addWall((4,24), (5,36))
	scene.addWall((4,35), (16,36))

	scene.addWall((24,4), (36,5))
	scene.addWall((35,4), (36,16))
	
	scene.addWall((36,36), (35,24))
	scene.addWall((24,35), (36,36))

	scene.addWall((8,8), (14,14))
	scene.addWall((20,8), (26,14))
	scene.addWall((8,20), (14,26))

	scene.addWall((16,18), (17,32))
	scene.addWall((31,18), (32,32))
	scene.addWall((16,31), (30,32))
	scene.addWall((16,16), (30,17))


	scene.addEnemy(2,2,red)
	scene.addEnemy(2,3,red)
	scene.addEnemy(3,2,red)
	scene.addEnemy(3,3,red)

	scene.addEnemy(38,38,blue)
	scene.addEnemy(38,39,blue)
	scene.addEnemy(39,38,blue)
	scene.addEnemy(39,39,blue)

	scene.addEnemy(2,38,red)
	scene.addEnemy(2,39,red)
	scene.addEnemy(3,38,red)
	scene.addEnemy(3,39,red)

	scene.addEnemy(38,2,blue)
	scene.addEnemy(39,3,blue)
	scene.addEnemy(39,2,blue)
	scene.addEnemy(38,3,blue)

	yield start()


@level (40, 40)
def level11(scene):

	scene.addWall((4,4), (5,16))
	scene.addWall((4,4), (16,5))
	
	scene.addWall((4,24), (5,36))
	scene.addWall((4,35), (16,36))

	scene.addWall((24,4), (36,5))
	scene.addWall((35,4), (36,16))
	
	scene.addWall((36,36), (35,24))
	scene.addWall((24,35), (36,36))

	scene.addWall((8,8), (14,14))
	scene.addWall((20,8), (26,14))
	scene.addWall((8,20), (14,26))

	scene.addWall((16,18), (17,32))
	scene.addWall((31,18), (32,32))
	scene.addWall((16,31), (30,32))
	scene.addWall((16,16), (30,17))

	scene.addEnemy(2,2,red)
	scene.addEnemy(2,3,blue)
	scene.addEnemy(3,2,red)
	scene.addEnemy(3,3,blue)

	scene.addEnemy(38,38,red)
	scene.addEnemy(38,39,blue)
	scene.addEnemy(39,38,red)
	scene.addEnemy(39,39,blue)

	scene.addEnemy(2,38,red)
	scene.addEnemy(2,39,blue)
	scene.addEnemy(3,38,red)
	scene.addEnemy(3,39,blue)

	scene.addEnemy(38,2,red)
	scene.addEnemy(39,3,blue)
	scene.addEnemy(39,2,red)
	scene.addEnemy(38,3,blue)

	yield start()

@level (40, 40)
def level12(scene):

	scene.addWall((4,4), (5,16))
	scene.addWall((4,4), (16,5))
	


	scene.addWall((4,24), (5,36))
	scene.addWall((4,35), (16,36))

	scene.addWall((19,0), (21,0))	
	scene.addWall((19,40), (21,40))
	scene.addWall((0,19), (0,21))
	scene.addWall((40,19), (40,21))

	scene.addWall((24,4), (36,5))
	scene.addWall((35,4), (36,16))
	
	scene.addWall((36,36), (35,24))
	scene.addWall((24,35), (36,36))

	scene.addWall((8,8), (14,14))
	scene.addWall((20,8), (26,14))
	scene.addWall((8,20), (14,26))

	scene.addWall((16,18), (17,32))
	scene.addWall((31,18), (32,32))
	scene.addWall((16,31), (30,32))
	scene.addWall((16,16), (30,17))

	scene.addEnemy(2,2,red)
	scene.addEnemy(2,3,blue)
	scene.addEnemy(3,2,red)
	scene.addEnemy(3,3,blue)

	scene.addEnemy(38,38,red)
	scene.addEnemy(38,39,blue)
	scene.addEnemy(39,38,red)
	scene.addEnemy(39,39,blue)

	scene.addEnemy(2,38,red)
	scene.addEnemy(2,39,blue)
	scene.addEnemy(3,38,red)
	scene.addEnemy(3,39,blue)

	scene.addEnemy(38,2,red)
	scene.addEnemy(39,3,blue)
	scene.addEnemy(39,2,red)
	scene.addEnemy(38,3,blue)

	yield start()

@level(30,20)
def level14(scene):

	scene.addWall((10,4), (11,16))
	scene.addWall((20,4), (21,16))

	scene.addWall((5,0), (6,6))
	scene.addWall((5,14), (6,20))

	scene.addWall((15,0), (16,6))
	scene.addWall((15,14), (16,20))

	scene.addWall((25,0), (26,6))
	scene.addWall((25,14), (26,20))

	for x in range(1,4):
		for y in range(1,4):
			scene.addEnemy(x, y, blue)
			scene.addEnemy(x, y+15, blue)
			scene.addEnemy(x+25, y, red)
			scene.addEnemy(x+25, y+15, red)

	yield start()		

@level(30,20)
def level15(scene):

	scene.addWall((10,4), (11,16))
	scene.addWall((20,4), (21,16))

	scene.addWall((5,0), (6,6))
	scene.addWall((5,14), (6,20))

	scene.addWall((15,0), (16,6))
	scene.addWall((15,14), (16,20))

	scene.addWall((25,0), (26,6))
	scene.addWall((25,14), (26,20))

	for x in range(1,4):
		for y in range(1,4):
			scene.addEnemy(x, y, blue)
			scene.addEnemy(x, y+15, red)
			scene.addEnemy(x+25, y, red)
			scene.addEnemy(x+25, y+15, blue)

	yield start()	

@level(30,20)
def level16(scene):

	scene.addWall((10,4), (11,16))
	scene.addWall((20,4), (21,16))

	scene.addWall((5,0), (6,6))
	scene.addWall((5,14), (6,20))

	scene.addWall((15,0), (16,6))
	scene.addWall((15,14), (16,20))

	scene.addWall((25,0), (26,6))
	scene.addWall((25,14), (26,20))

	for x in range(1,4):
		for y in range(1,4):
			if x == 1 or x == 3:
				if y == 1 or y == 3:
					scene.addEnemy(x, y, blue)
					scene.addEnemy(x, y+15, blue)
					scene.addEnemy(x+25, y, blue)
					scene.addEnemy(x+25, y+15, blue)
				else:
					scene.addEnemy(x, y, red)
					scene.addEnemy(x, y+15, red)
					scene.addEnemy(x+25, y, red)
					scene.addEnemy(x+25, y+15, red)	
			else:
				if y == 1 or y == 3:
					scene.addEnemy(x, y, red)
					scene.addEnemy(x, y+15, red)
					scene.addEnemy(x+25, y, red)
					scene.addEnemy(x+25, y+15, red)
				else:
					scene.addEnemy(x, y, blue)
					scene.addEnemy(x, y+15, blue)
					scene.addEnemy(x+25, y, blue)
					scene.addEnemy(x+25, y+15, blue)

	yield start()	


@level(30,20)
def level17(scene):

	scene.addWall((10,2), (11,19))
	scene.addWall((20,2), (21,19))

	scene.addWall((5,0), (5,8))
	scene.addWall((5,12), (6,20))

	scene.addWall((15,0), (16,8))
	scene.addWall((15,12), (16,20))

	scene.addWall((25,0), (26,8))
	scene.addWall((25,12), (26,20))

	for x in range(1,4):
		for y in range(1,4):
			if x == 1 or x == 3:
				if y == 1 or y == 3:
					scene.addEnemy(x, y, blue)
					scene.addEnemy(x, y+15, blue)
					scene.addEnemy(x+25, y, blue)
					scene.addEnemy(x+25, y+15, blue)
				else:
					scene.addEnemy(x, y, red)
					scene.addEnemy(x, y+15, red)
					scene.addEnemy(x+25, y, red)
					scene.addEnemy(x+25, y+15, red)	
			else:
				if y == 1 or y == 3:
					scene.addEnemy(x, y, red)
					scene.addEnemy(x, y+15, red)
					scene.addEnemy(x+25, y, red)
					scene.addEnemy(x+25, y+15, red)
				else:
					scene.addEnemy(x, y, blue)
					scene.addEnemy(x, y+15, blue)
					scene.addEnemy(x+25, y, blue)
					scene.addEnemy(x+25, y+15, blue)
				

	yield start()

@level(30,30)
def level18(scene):
	scene.redShip.x = 3
	scene.redShip.y = 15
	scene.blueShip.x = 27
	scene.blueShip.y = 15

	scene.addWall((0,20), (10,21))
	scene.addWall((0,10), (10,11))

	scene.addWall((20,20), (30,21))
	scene.addWall((20,10), (30,11))

	for x in range(1,4):
		for y in range(1,4):
			scene.addEnemy(x+20,y+13,red)
			scene.addEnemy(x+10,y+13,blue)
			scene.addEnemy(x+3,y+3,red)
			scene.addEnemy(x+3,y+23,blue)
			scene.addEnemy(x+23,y+3,red)
			scene.addEnemy(x+23,y+23,blue)
	yield start()

@level(3, 2)
def win(scene):
	yield message('You win!')
	import sys
	sys.exit(0)

levels = [level1, level2, level3, level4, level5, level5a, level6, level7, level8, level9, level10, level11, level12, level14, level15, level16, level17, level18, win]

#		self.enemies = [Enemy(parent=self, color=(k/10) and darkRed or darkBlue,
#		                      x=16 + random.randint(9, 15) * math.sin(theta),
#		                      y=12 + random.randint(9, 10) * math.cos(theta),
#		                      target=(k/10) and self.blueShip or self.redShip,
#		                      collisionType=(k/10) and CollisionTypes.redEnemy or CollisionTypes.blueEnemy)
#		                for k in range(20) for theta in [k * 2 * math.pi / 20]]

#		self.wall1 = Wall(self, walls, (12,5), (13,19))
#		self.wall2 = Wall(self, walls, (19,5), (20,19))
