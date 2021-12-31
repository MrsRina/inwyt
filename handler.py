# Current packet list.
PACKET_SEND_LIST = [];
PACKET_RECEIVE_LIST = [];

# RP: Receive Packet; SP: Send Packet;
RP_SPAWN_ENTITY = 0;
SP_SPAWN_ENTITY = 1;

def listen_channel(k):
	p = -1;

	if len(k) != 0:
		p = k[0];

	return p;

def refresh_channel(k):
	if len(k) != 0:
		del k[0];

def send_packet(packet):
	PACKET_SEND_LIST.append(packet);

def receive_packet(packet):
	PACKET_RECEIVE_LIST.append(packet);

def packet(data):
	return data;

def packet_decoder(inwyt, channel_open = False):
	packet = listen_channel(PACKET_SEND_LIST);

	if not channel_open or packet == -1:
		return;

	if packet[0] == SP_SPAWN_ENTITY:
		receive_packet([RP_SPAWN_ENTITY, packet[1], packet[2], packet[3]]);
		refresh_channel(PACKET_SEND_LIST);

def ingame_packet_processor(inwyt):
	packet = listen_channel(PACKET_RECEIVE_LIST);
	world = inwyt.world;

	if world is not None and packet != -1:
		if packet[0] == RP_SPAWN_ENTITY:
			entity = world.get_entity(packet[1]);

			if entity is not None:
				entity.set_position(packet[2], packet[3]);
				entity.rect.update();

			refresh_channel(PACKET_RECEIVE_LIST);