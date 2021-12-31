import pygame;
import sys;

from OpenGL import GL as GL11;

# Core from InWYT;
from   core import Math, Timing, Input, Rect, TextureManager;
import core

import world;
import render;
import handler;

# Just start pygame stuff.
pygame.init();
pygame.mixer.quit();

class InWYT:
	def __init__(self):
		self.update_display();
		self.prepare_init();

	def update_display(self):
		self.window = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL); pygame.display.set_caption("It's not what you think");

	def prepare_init(self):
		# Managers & stuffs.
		self.the_input = Input(self);
		self.texture_manager = TextureManager(self);

		self.texture_manager.init();

		# Shits.
		self.running = True;
		self.timer = 60;

		# Ticks stuff.
		self.previous_ticks = 0;
		self.elapsed_ticks = 0;
		self.running_ticks = 0;
		self.partial_ticks = 0;

		# Objects.
		self.concurrent_object_list = [];
		self.background_color = [0, 190, 190];

		self.player = world.EntityPlayer("Rina", 99);

		self.world = world.World(self);
		self.world.init();
		self.world.camera_drag = True;
		self.world.add_entity(self.player);
		self.world.request_spawn();

		self.screen_width = 0;
		self.screen_height = 0;

		self.mouse_x = 0;
		self.mouse_y = 0;

	def update(self):
		handler.ingame_packet_processor(self);
		handler.packet_decoder(self, channel_open = True);

		self.the_input.update();

		if self.world is not None:
			self.world.update();

			if self.world.surface.w != self.screen_width or self.world.surface.h != self.screen_height:
				self.world.surface.w = self.screen_width;
				self.world.surface.h = self.screen_height;

				self.world.surface.update();

	def render(self):
		if self.world is not None:
			self.world.render(self.partial_ticks);

	def loop(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False;

					sys.exit();

					break;

				if event.type == pygame.KEYDOWN:
					self.the_input.keyboard_listener(event.key, core.KEYDOWN);

				if event.type == pygame.KEYUP:
					self.the_input.keyboard_listener(event.key, core.KEYUP);

				if event.type == pygame.MOUSEBUTTONUP:
					if self.world is not None:
						self.world.mouse_listener(event.pos[0], event.pos[1], event.button, core.KEYUP);

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.world is not None:
						self.world.mouse_listener(event.pos[0], event.pos[1], event.button, core.KEYDOWN);

			self.running_ticks += Timing.get_ticks() - self.previous_ticks;
			self.previous_ticks = Timing.get_ticks();

			self.partial_ticks = 0.1 + (self.running_ticks * 0.001);

			while (self.running_ticks >= self.timer):
				self.update();

				self.running_ticks -= self.timer;

			self.screen_width, self.screen_height = pygame.display.get_surface().get_size();
			self.mouse_x, self.mouse_y = pygame.mouse.get_pos();

			GL11.glClearColor(self.background_color[0] / 255.0, self.background_color[1] / 255.0, self.background_color[2] / 255.0, 1);
			GL11.glClear(GL11.GL_DEPTH_BUFFER_BIT | GL11.GL_COLOR_BUFFER_BIT);

			GL11.glMatrixMode(GL11.GL_PROJECTION);
			GL11.glLoadIdentity();
			GL11.glOrtho(0, self.screen_width, self.screen_height, 0, -1, 1);

			GL11.glMatrixMode(GL11.GL_MODELVIEW);
			GL11.glDepthFunc(GL11.GL_NEVER);

			self.render();

			pygame.display.flip();

if "__main__" == "__main__":
	game = InWYT();
	game.loop();