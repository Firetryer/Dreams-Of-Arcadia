import pygame



def world_to_screen(x, y):
	w, h = pygame.display.get_surface().get_size()
	return (int(x * (w / 1920)), int(y * (h / 1080)))

def screen_to_world(x, y):
	w, h = pygame.display.get_surface().get_size()
	return (int(x / (w / 1920)), int(y / ( h / 1080)))	

def size_to_screen(x):
	w, h = pygame.display.get_surface().get_size()
	offset = w / 1920
	return int(x * offset)