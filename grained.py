import numpy as np
from PIL import Image

import random
import argparse

parser = argparse.ArgumentParser(description='Run grain filter on a image')
parser.add_argument('file', type=str, help="The image to process")
parser.add_argument('--invert', action="store_true", default=False, help="Whether to invert the image")
parser.add_argument('--tilesize', type=int, default=3, help="The tile size (tiles are square).")
args = parser.parse_args()
# print(args)
# exit()

def pil_grid(images, max_horiz=np.iinfo(int).max):
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * ((n_images // n_horiz) + (1 if n_images % n_horiz > 0 else 0))
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('L', (h_sizes[-1], v_sizes[-1]), color='Black')
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid

import pathlib

if not pathlib.Path(args.file).exists():
    print("The specified file does not exist!")
    exit()

img = Image.open(args.file)
gimg = img.convert('L')
im = (np.array(gimg)/255.)
if args.invert: im = 1 - im
print(im.shape)
#img.histogram()
M = args.tilesize
N = M
tiles = [im[x:x+M,y:y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
print(tiles[0].shape)
brights = [tile.mean() for tile in tiles]
# print(brights[23])
# print(max(brights))
# print(min(brights))
ntiles = []
for bright in brights:
    ntile = np.random.rand(M, N)
    ntile = ntile < bright
    ntile = ntile.astype(float)
    ntile = (ntile*255).astype(int)
    ntiles.append(Image.fromarray(ntile))

xtiles = np.ceil(im.shape[1] / M).astype(int)

print(xtiles)

#print(ntiles)

total = pil_grid(ntiles, xtiles)

total.save("out.png")
print("done")