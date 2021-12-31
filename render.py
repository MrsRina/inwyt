from OpenGL import GL as GL11;

import math;
import pygame;

def lerp(a, b, t):
	if t >= 1 or t < 0:
		return b;

	return a + (b - a) * t;

def texture_id(i):
	return GL11.glGenTextures(i);

def matrix():
	GL11.glPushMatrix();

def refresh():
	GL11.glPopMatrix();

def color(r, g, b, a):
	GL11.glColor(r / 255.0, g / 255.0, b / 255.0, a / 255.0);

def scale(s, s1):
	GL11.glScale(s, s1, 0);

def draw_immediate_rect(vertex, z_level, mode, camera_x, camera_y):
	GL11.glBegin(mode);
	GL11.glVertex(vertex[0].x + camera_x, vertex[0].y + camera_y, z_level);
	GL11.glVertex(vertex[1].x + camera_x, vertex[1].y + camera_y, z_level);
	GL11.glVertex(vertex[2].x + camera_x, vertex[2].y + camera_y, z_level);
	GL11.glVertex(vertex[3].x + camera_x, vertex[3].y + camera_y, z_level);
	GL11.glEnd();

def draw_immediate_texture(x, y, w, h, texture_id, z_level):
	GL11.glEnable(GL11.GL_TEXTURE_2D);
	GL11.glBindTexture(GL11.GL_TEXTURE_2D, texture_id);

	GL11.glBegin(GL11.GL_QUADS);
	GL11.glTexCoord(0, 0);
	GL11.glVertex(x, y, z_level);
	GL11.glTexCoord(0, 1);
	GL11.glVertex(x, y + h, z_level);
	GL11.glTexCoord(1, 1);
	GL11.glVertex(x + w, y + h, z_level);
	GL11.glTexCoord(1, 0);
	GL11.glVertex(x + w, y, z_level);
	GL11.glEnd();

	GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
	GL11.glDisable(GL11.GL_TEXTURE_2D);

def to_texture_id(texture, texture_id):
	data = pygame.image.tostring(texture, "RGBA");

	GL11.glEnable(GL11.GL_TEXTURE_2D);
	GL11.glBindTexture(GL11.GL_TEXTURE_2D, texture_id);

	GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_NEAREST);
	GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_NEAREST);

	GL11.glTexImage2D(GL11.GL_TEXTURE_2D, 0, GL11.GL_RGBA, texture.get_width(), texture.get_height(), 0, GL11.GL_RGBA, GL11.GL_UNSIGNED_BYTE, data);

	GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
	GL11.glDisable(GL11.GL_TEXTURE_2D);

	return texture_id;

def enable_blend():
	GL11.glEnable(GL11.GL_BLEND);
	GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);

def draw_immediate_arc(x, y, r):
	GL11.glBegin(GL11.GL_TRIANGLES);

	for i in range(40 // (360 // 2) + 1, 40 // (360 // 360)):
		previousAngle =  (2 * math.pi * (i - 1) / 40);
		angle = (2 * math.pi * i / 40);

		GL11.glVertex(x, y);
		GL11.glVertex((x + math.cos(angle) * r), (y + math.sin(angle) * r));
		GL11.glVertex((x + math.cos(previousAngle) * r), (y + math.sin(previousAngle) * r));

	GL11.glEnd();