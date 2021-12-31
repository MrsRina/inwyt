import handler;
import render;
import core;
import json;
import os;

TILE_SIZE = 32;

def load_map(the_map, data):
	#the_map.id = data["id"];
	texture_data = data["textures"];
	#the_map.background_color = data["color"];

	#the_map.loaded_image_list.clear();
	#the_map.loaded_entity_list.clear();

	for textures in texture_data:
		the_map.inwyt.texture_manager.add("data/" + os.path.basename(textures["path"]), textures["tag"]);

	image_data = data["images"];

	for images in image_data:
		tag = images["tag"];
		name = images["name"];
		mode = images["mode"];
		id = images["id"];

		alpha = images["alpha"];
		static = images["static"];
		tile = images["tile"];
		visibility = images["visibility"];

		x = images["x"];
		y = images["y"];
		w = images["w"];
		h = images["h"];

		the_map.data[(x, y)] = [w, h, name]

class EntityPlayer:
	def __init__(self, tag, id):
		self.tag = tag;
		self.id = id;
		self.rect = core.Rect(core.Vec(0, 0), 32, 32 + 32, 0);
		self.z_level = 0;

	def set_position(self, x, y):
		self.rect.c.x = x;
		self.rect.c.y = y;

		self.rect.update();

	def update(self):
		pass;

class World:
	def __init__(self, inwyt):
		self.inwyt = inwyt;
		self.data = {};

		self.entity_list = {};
		self.loaded_entity_list = {};

		# Packets list to do shit.
		self.packets = {};

		# Surface shit.
		self.surface = core.Rect(core.Vec(0, 0), 20, 20);

		# Camera shit.
		self.camera_x = 0;
		self.camera_y = 0;

		self.camera_focus_on_player = False;
		self.camera_dragging = False;
		self.camera_drag = False;

		self.camera_drag_x = 0;
		self.camera_drag_y = 0;

		self.camera_tick_pos_x = 0;
		self.camera_tick_pos_y = 0;

		self.camera_zoom = 0;

	def init(self):
		self.read_data_from_file("data/level_1.json");

	def request_spawn(self):
		for i in self.data:
			tile = self.data[i];

			if tile[2] == "player_spawn":
				handler.send_packet([handler.SP_SPAWN_ENTITY, self.inwyt.player.id, i[0], i[1]]);

	def read_data_from_file(self, path):
		with open(path, 'r') as file:
			data = json.load(file);

			load_map(self, data);
			file.close();

	def get_entity(self, id):
		if self.loaded_entity_list.__contains__(id):
			return self.loaded_entity_list[id];

		return None;

	def add_entity(self, entity):
		if self.loaded_entity_list.__contains__(entity.id) is False:
			self.loaded_entity_list[entity.id] = entity;

		return entity;

	def remove_entity(self, id):
		if self.loaded_entity_list.__contains__(id):
			del self.loaded_entity_list[id];

	def mouse_listener(self, mx, my, button, state):
		if self.camera_drag:
			if state == core.KEYDOWN and button == 5:
				self.camera_zoom += 1;

			if state == core.KEYDOWN and button == 4:
				self.camera_zoom -= 1;

			if state == core.KEYDOWN and button == 2:
				self.camera_drag_x = mx - self.camera_x;
				self.camera_drag_y = my - self.camera_y;

				self.camera_dragging = True;

		if state == core.KEYUP:
			self.camera_dragging = False;

	def update(self):
		for entities_id in self.loaded_entity_list:
			entity = self.loaded_entity_list[entities_id];
			entity.update();

		if self.camera_dragging:
			self.camera_tick_pos_x = self.inwyt.mouse_x - self.camera_drag_x;
			self.camera_tick_pos_y = self.inwyt.mouse_y - self.camera_drag_y;

	def render(self, partial_ticks):
		self.camera_x = render.lerp(self.camera_x, self.camera_tick_pos_x, partial_ticks);
		self.camera_y = render.lerp(self.camera_y, self.camera_tick_pos_y, partial_ticks);

		for i in self.data:
			tile = self.data[i];

			render.matrix();
			render.enable_blend();
			render.color(255, 255, 255, 255);
			render.draw_immediate_texture(i[0] + self.camera_x, i[1] + self.camera_y, tile[0], tile[1], self.inwyt.texture_manager.get(tile[2]), -1);
			render.refresh();

		for entities_id in self.loaded_entity_list:
			entity = self.loaded_entity_list[entities_id];

			render.matrix();
			render.enable_blend();
			render.color(255, 255, 255, 100);
			render.draw_immediate_rect(entity.rect.vertex, entity.z_level, render.GL11.GL_QUADS, self.camera_x, self.camera_y);
			render.refresh();