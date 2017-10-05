#!/usr/bin/env python
# blender python
import argparse
import sys

parser = argparse.ArgumentParser(description='mandelmesh - produce meshes from fractals')
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])

import bpy
import math

def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name + ' Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True

    # Link object to scene
    bpy.context.scene.objects.link(ob)

    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)

    # Update mesh with new data
    me.update(calc_edges=True)
    
    return ob

def _frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def frange(x, y, jump):
    return list(_frange(x, y, jump))

# scale from
def sclfrm(center, value, off):
    return (value - center) * off + center


"""

"""
def mand_data(zoom=1, miter=20, scale=1.0, zscale=1.0, xv=(-1, 1, .01), yv=(-1, 1, .01)):
    x_coords = frange(*xv)
    y_coords = frange(*yv)

    cx = (xv[0]+xv[1])/2.0
    cy = (yv[0]+yv[1])/2.0

    mverts = [(None, None, None)] * (len(x_coords) * len(y_coords))
    
    px = 0
    for x in x_coords:
        py = 0        
        for y in y_coords:
            c = x + y * 1j
            z = c + 0
            ci = 0
            for k in range(0, miter):
                if abs(z) > 2 ** 4:
                    break
                ci += 1
                z = z ** 2 + c
            if abs(z) <= 1:
                z = 2.0
            
            fri = 2 + ci - math.log(math.log(abs(z))) / math.log(2.0)

            if fri > miter:
                fri = miter
            if fri < 0:
                fri = 0

            if fri == 0:
                fri = 0
            else:
                fri = miter * (1 - 1 / (1.213 ** fri))
            
            #fri = math.log(fri / miter)
            fri = float(fri)
            mverts[px + len(x_coords) * py] = (sclfrm(cx, x, scale), sclfrm(cy, y, scale), zscale * (fri / miter))
            py += 1

        px += 1

    print ("generating faces")
    mfaces = []
    for i in range(0, len(x_coords)-2):
        for j in range(0, len(y_coords)):
            idx = i + len(x_coords) * j
            if idx + len(x_coords) + 2 < len(x_coords) * len(y_coords):
                mfaces += [(idx, idx + len(x_coords) + 1, idx + 1)]
                mfaces += [(idx + len(x_coords) + 1, idx + 1, idx + len(x_coords) + 2)]


    return mverts, mfaces

            
def run(origin):
    # center, zoom, slices
    vv = lambda c, z, s: (c - 1.0 / z, c + 1.0 / z, 2.0 / (z * s))
    verts0, faces0 = mand_data(scale=1, miter=250, zscale=1, xv=vv(-.5, .5, 100), yv=vv(0, .5, 100), zoom=10)
    ob1 = createMesh('MANDELBROT', origin, verts0, [], faces0)
    return

if __name__ == "__main__":
    run((0,0,0))
