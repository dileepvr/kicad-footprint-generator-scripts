#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math

# sizes in old library:
standard_diameters = [2.5, 2.7, 3.0, 3.5, 3.7, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5]

# ISO metric screw thread (https://en.wikipedia.org/wiki/ISO_metric_screw_thread)
metric_sizes = {
	"M2": 2.2,
	"M2.5": 2.7,
	"M3": 3.2,
	"M4": 4.3,
	"M5": 5.3,
	"M6": 6.4,
	"M8": 8.4
}

# screw sizes (radii)
DIN965 = {
	"M2": 1.9,
	"M2.5": 2.35,
	"M3": 2.8,
	"M4": 3.75,
	"M5": 4.6,
	"M6": 5.5,
}

ISO14580 = {
	"M2": 1.9,
	"M2.5": 2.25,
	"M3": 2.75,
	"M4": 3.5,
	"M5": 4.25,
	"M6": 5,
}

ISO7380 = {
	"M2": 1.75,
	"M2.5": 2.25,
	"M3": 2.85,
	"M4": 3.8,
	"M5": 4.75,
	"M6": 5.25,
}

crtyd_width = 0.05
crtyd_spacing = 0.5

def crtyd_round(value, direction):
	if direction > 0:
		return math.ceil(value/0.05)*0.05
	else:
		return math.floor(value/0.05)*0.05

# Drill diameter, pad diameter, screw diameter, tags
mounting_holes = []

for drill_diameter in standard_diameters:
	mounting_holes.append([drill_diameter, None, None, []])

	pad_diameter = 2.0*drill_diameter
	mounting_holes.append([drill_diameter, pad_diameter, None, []])

for name, drill_diameter in metric_sizes.items():
	mounting_holes.append([drill_diameter, None, None, [name]])

	pad_diameter = 2.0*drill_diameter
	mounting_holes.append([drill_diameter, pad_diameter, None, [name]])

for name, screw_radius in DIN965.items():
	drill_diameter = metric_sizes[name]
	mounting_holes.append([drill_diameter, None, 2.0*screw_radius, [name, "DIN965"]])

	mounting_holes.append([drill_diameter, 2.0*screw_radius, 2.0*screw_radius, [name, "DIN965"]])

for name, screw_radius in ISO14580.items():
	drill_diameter = metric_sizes[name]
	mounting_holes.append([drill_diameter, None, 2.0*screw_radius, [name, "ISO14580"]])

	mounting_holes.append([drill_diameter, 2.0*screw_radius, 2.0*screw_radius, [name, "ISO14580"]])

for name, screw_radius in ISO7380.items():
	drill_diameter = metric_sizes[name]
	mounting_holes.append([drill_diameter, None, 2.0*screw_radius, [name, "ISO7380"]])

	mounting_holes.append([drill_diameter, 2.0*screw_radius, 2.0*screw_radius, [name, "ISO7380"]])

def name(drill_diameter, pad_diameter, labels):
	name = "MountingHole"

	name += ("_%.3gmm" % (drill_diameter)).replace(".","-")

	for label in labels:
		name += "_%s" % (label.replace(".","-"))

	if pad_diameter:
		name += "_Pad"

	return name

def description(drill_diameter, pad_diameter, labels):
	res = "Mounting Hole %.3gmm" % (drill_diameter)

	if pad_diameter == None:
		res += ", no annular"

	for label in labels:
		res += ", %s" % (label)

	return res

def tags(drill_diameter, pad_diameter, labels):
	res = "mounting hole %.3gmm" % (drill_diameter)

	if pad_diameter == None:
		res += " no annular"

	for label in labels:
		res += " %s" % (label.lower())

	return res

def pad(name, type_ = 'thru_hole', shape = 'circle', at = None, size = None, drill_size = None, layers = None):
	res = "  (pad";

	# add name
	res += " %s" % (name)

	# add type
	res += " %s" % (type_)

	# add shape
	res += " %s" % (shape)

	if at:
		res += " (at %.3g %.3g)" % (at[0], at[1])

	res += " (size %.3g %.3g)" % (size[0], size[1])

	if drill_size:
		res += " (drill %.3g)" % (drill_size)

	if layers == None:
		if type_ == 'thru_hole' or type_ == 'np_thru_hole':
			layers = "*.Cu *.Mask F.SilkS"
		elif type_ == 'smd' or type_ == 'connect':
			layers = "F.Cu F.Paste F.Mask"
		else:
			raise("Type '%s' not supported" % type_)

	res += " (layers%s%s)" % (" " if layers != "" else "", layers)

	res += ")\n"

	return res

for mounting_hole in mounting_holes:
	drill_diameter, pad_diameter, screw_diameter, labels = mounting_hole

	screw_diameter = 2.0*drill_diameter if screw_diameter == None else screw_diameter

	print(drill_diameter, pad_diameter, screw_diameter)

	module_name = name(drill_diameter, pad_diameter, labels)

	filename = "%s.kicad_mod" % (module_name)

	with open(filename, 'w') as output:
		output.write("(module %s (layer F.Cu) (tedit %X)\n" % (module_name, int(time.time())))
		output.write("  (at 0 0)\n")

		# description
		output.write("  (descr \"%s\")\n" % (description(drill_diameter, pad_diameter, labels)))

		# tags
		output.write("  (tags \"%s\")\n" % (tags(drill_diameter, pad_diameter, labels)))

		text_size = 1
		text_offset = screw_diameter/2.0 + text_size

		# reference
		output.write("  (fp_text reference REF** (at %.3g %.3g) (layer F.SilkS)\n" % (0,-text_offset))
		output.write("    (effects (font (size %.3g %.3g) (thickness 0.15)))\n" % (text_size, text_size))
		output.write("  )\n")

		# value
		output.write("  (fp_text value %s (at %.3g %.3g) (layer F.Fab)\n" % (module_name, 0,text_offset))
		output.write("    (effects (font (size %.3g %.3g) (thickness 0.15)))\n" % (text_size, text_size))
		output.write("  )\n")

		# screw size
		output.write("  (fp_circle (center %.3g %.3g) (end %.3g %.3g) (layer Cmts.User) (width 0.15))\n" %
			(0, 0, screw_diameter/2.0, 0))

		# courtyard
		crtyd_diameter = crtyd_round(max(screw_diameter, pad_diameter if pad_diameter else drill_diameter) + crtyd_spacing,1)
		output.write("  (fp_circle (center %.3g %.3g) (end %.3g %.3g) (layer F.CrtYd) (width %.3g))\n" %
			(0, 0, crtyd_diameter/2.0, 0, crtyd_width))

		output.write(pad(
			name = 1,
			type_ = "thru_hole",
			shape = "circle",
			at = [0, 0],
			size = [pad_diameter, pad_diameter] if pad_diameter else [drill_diameter, drill_diameter],
			drill_size = drill_diameter,
			layers = "*.Cu *.Mask F.SilkS" if pad_diameter else ""))

		output.write(")\n")
		output.close()


# 		if not shield:
# 			crtyd_x_lines = [
# 				crtyd_round(x_lines[0] - crtyd_spacing, -1),
# 				crtyd_round(x_lines[-1] + crtyd_spacing, 1)]
# 		else:
# 			crtyd_x_lines = [
# 				crtyd_round(x_origin - C(number_of_positions)/2.0 - pth_ring/2.0 - crtyd_spacing, -1),
# 				crtyd_round(x_origin + C(number_of_positions)/2.0 + pth_ring/2.0 + crtyd_spacing, 1)]

# 		crtyd_y_lines = [
# 			crtyd_round(y_lines[0] - crtyd_spacing, -1),
# 			crtyd_round(y_lines[-1] + crtyd_spacing, 1)]

# 		for y in crtyd_y_lines:
# 			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
# 				crtyd_x_lines[0],
# 				y,
# 				crtyd_x_lines[-1],
# 				y,
# 				crtyd_width))

# 		for x in crtyd_x_lines:
# 			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
# 				x,
# 				crtyd_y_lines[0],
# 				x,
# 				crtyd_y_lines[-1],
# 				crtyd_width
# 				))


