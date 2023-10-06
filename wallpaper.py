import os
import random

wallpapers_dir = "/home/jakub/.config/qtile/wallpapers/"
wallpaper_prefered = "leaves.jpg"
wallpapers = [
    'mountains.jpg',
    'mountains2.png',
    'mountains3.jpg',
    'plasma.jpg',
    'leaves.jpg',
    'penguins.jpg',
    'forrest.png',
    'deer.jpg',
    'autumn.jpg',
    'fjord.jpg'
    'river.jpg'
]

def get_wallpaper(generate_random=True):
    if generate_random:
        wallpapers = os.listdir(wallpapers_dir)
        return wallpapers_dir + wallpapers[random.randint(0, len(wallpapers) - 1)]
    else:
        return wallpapers_dir + wallpaper_prefered
