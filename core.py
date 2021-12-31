import render;
import pygame;
import math;

from OpenGL import GL as GL11;

RECT = 0;
CIRCLE = 1;

KEYUP = 2;
KEYDOWN = 3;

class TextureManager:
	def __init__(self, inwyt):
		self.inwyt = inwyt;
		self.textures = {};

	def init(self):
		self.add("data/terrain.png", "terrain");

	def add(self, path, tag):
		if self.textures.__contains__(tag) is False:
			image = None;

			try:
				image = pygame.image.load(path).convert_alpha();
			except IOError as exc:
				pass;

			if image is not None:
				id = render.texture_id(0);

				self.textures[tag] = render.to_texture_id(image, render.texture_id(1));

	def get(self, tag):
		if self.textures.__contains__(tag):
			return self.textures[tag];

		return None;

class Input:
	def convert_state_to_bool(boolean, state):
		if state is KEYDOWN:
			boolean = False;

		if state is KEYUP:
			boolean = True;

	def __init__(self, inwyt):
		self.inwyt = inwyt;
		self.object_in = None;

		self.up = False;
		self.down = False;
		self.left = False;
		self.right = False;

	def set_controll(self, obj):
		self.object_in = obj;

	def unset_control(self):
		self.object_in = None;

	def keyboard_listener(self, key, state):
		if self.object_in is None:
			return;

		if key == pygame.K_w:
			convert_state_to_bool(self.up, state);

		if key == pygame.K_d:
			convert_state_to_bool(self.right, state);

		if key == pygame.K_a:
			convert_state_to_bool(self.left, state);

		if key == pygame.K_s:
			convert_state_to_bool(self.down, state);

	def update(self):
		if self.object_in is None:
			return;

		if self.up:
			self.object_in.move(Vec(0, -10));

		if self.right:
			self.object_in.move(Vec(10, 0));

		if self.left:
			self.object_in.move(Vec(-10, 0));

		if self.down:
			self.object_in.move(Vec(0, 10));

class Math:
	def clamp(i, n, m):
		return n if i <= n else (m if i >= m else i);

class Timing:
	def get_ticks():
		return pygame.time.get_ticks();

	def __init__(self):
		self.ms = -1;

	def reset(self):
		self.ms = pygame.time.get_ticks();

	def current_ms(self):
		return pygame.time.get_ticks() - self.ms;

	def is_passed(self, ms):
		return pygame.time.get_ticks() - self.ms >= ms;

	def count(self, ms_div):
		return (pygame.time.get_ticks() - self.ms) / ms_div;

class Vec:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def length(self):
		x = self.x * self.x;
		y = self.y * self.y;

		return math.sqrt(x + y);

	def dot(self, v):
		return (self.x * v.x + self.y * v.y);

	def cross(self, v):
		return (self.x * v.y - self.y * v.x);

	def rotate(self, v, a):
		rx = 0;
		ry = 0;

		x = self.x - v.x;
		y = self.y - v.y;

		rx = x * math.cos(a) - y * math.sin(a);
		ry = x * math.sin(a) + y * math.cos(a);

		rx += v.x;
		ry += v.y;

		return Vec(rx, ry);

	def normalize(self):
		l = self.length();

		if l > 0:
			l = 1 / l;

		return Vec(self.x * l, self.y * l);

	def distance(self, v):
		dx = self.x - v.x;
		dy = self.y - v.y;

		diff = dx * dx + dy * dy;

		return math.sqrt(diff);

	def __add__(self, i):
		x = i;
		y = i;

		if type(i) is Vec:
			x = i.x;
			y = i.y;

		return Vec(self.x + x, self.y + y);

	def __sub__(self, i):
		x = i;
		y = i;

		if type(i) is Vec:
			x = i.x;
			y = i.y;

		return Vec(self.x - x, self.y - y);

	def __mul__(self, i):
		return Vec(self.x * i, self.y * i);

	def __div__(self, i):
		x = i;
		y = i;

		if type(i) is Vec:
			x = i.x;
			y = i.y;

		return Vec(self.x / x, self.y / y);

class Rect:
	def __init__(self, c, w, h, fix = False):
		self.c = c;
		self.a = 0;
		self.the_type = RECT;

		self.w = w;
		self.h = h;

		self.fix = fix;

		self.vertex = [None, None, None, None];
		self.faces = [None, None, None, None];

		self.vertex[0] = Vec(self.c.x - self.w / 2, self.c.y - self.h / 2);
		self.vertex[1] = Vec(self.c.x + self.w / 2, self.c.y - self.h / 2);
		self.vertex[2] = Vec(self.c.x + self.w / 2, self.c.y + self.h / 2);
		self.vertex[3] = Vec(self.c.x - self.w / 2, self.c.y + self.h / 2);

		self.faces[0] = self.vertex[1] - self.vertex[2];
		self.faces[0] = self.faces[0].normalize();
		self.faces[1] = self.vertex[2] - self.vertex[3];
		self.faces[1] = self.faces[1].normalize();
		self.faces[2] = self.vertex[3] - self.vertex[0];
		self.faces[2] = self.faces[2].normalize();
		self.faces[3] = self.vertex[0] - self.vertex[1];
		self.faces[3] = self.faces[3].normalize();

	def update(self):
		self.vertex[0] = Vec(self.c.x - self.w / 2, self.c.y - self.h / 2);
		self.vertex[1] = Vec(self.c.x + self.w / 2, self.c.y - self.h / 2);
		self.vertex[2] = Vec(self.c.x + self.w / 2, self.c.y + self.h / 2);
		self.vertex[3] = Vec(self.c.x - self.w / 2, self.c.y + self.h / 2);

		self.faces[0] = self.vertex[1] - self.vertex[2];
		self.faces[0] = self.faces[0].normalize();
		self.faces[1] = self.vertex[2] - self.vertex[3];
		self.faces[1] = self.faces[1].normalize();
		self.faces[2] = self.vertex[3] - self.vertex[0];
		self.faces[2] = self.faces[2].normalize();
		self.faces[3] = self.vertex[0] - self.vertex[1];
		self.faces[3] = self.faces[3].normalize();

	def move(self, v):
		for l, k in enumerate(self.vertex):
			self.vertex[l] = self.vertex[i] + v;

		self.c = self.c + v;

		return self;

	def rotate(self, angle):
		for i, k in enumerate(self.vertex):
			self.vertex[i] = self.vertex[i].rotate(self.c, angle);

		self.faces[0] = self.vertex[1] - self.vertex[2];
		self.faces[0] = self.faces[0].normalize();
		self.faces[1] = self.vertex[2] - self.vertex[3];
		self.faces[1] = self.faces[1].normalize();
		self.faces[2] = self.vertex[3] - self.vertex[0];
		self.faces[2] = self.faces[2].normalize();
		self.faces[3] = self.vertex[0] - self.vertex[1];
		self.faces[3] = self.faces[3].normalize();

		return self;

	def collide_with_mouse(self, x, y):
		return (x >= self.vertex[0].x and y >= self.vertex[0].y) and (x >= self.vertex[1].x and y >= self.vertex[1].y) and (x <= self.vertex[2].x and y <= self.vertex[2].y) and (x <= self.vertex[3].x and y <= self.vertex[3].y);

	def get_type(self):
		return self.the_type;

class Circle:
	def __init__(self, c, r):
		self.c = c;
		self.r = r;
		self.a = 0;

		self.the_type = CIRCLE;
		self.point = Vec(self.c.x, self.c.y - r);

	def move(self, v):
		self.point = self.point + v;
		self.c = self.c + v;

		return self;

	def rotate(self, angle):
		self.a += angle;
		self.point = self.point.rotate(self.c, self.a);

		return self;

	def get_type(self):
		return self.the_type;

	def collide_bounce_with_circle(self, circle):
		diff = self.c - circle.c;
		dist = diff.length();

		radiu = self.r + circle.r;

		if dist > radiu:
			return False;

		return True;

	def collide_with_circle(self, circle):
		diff = self.c - circle.c;
		dist = diff.length();

		radiu = self.r + circle.r;

		if dist > math.sqrt(radiu * radiu):
			return False;

		if dist != 0:
			diff_normal = (diff * -1).normalize();
			diff_radiu = (diff_normal * circle.r);

			circle.c + diff_radiu;

		return True;