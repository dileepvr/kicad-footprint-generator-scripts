#!/usr/bin/env python
print "(module VHDCI (layer F.Cu) (tedit 5478A913)"
print "  (fp_text reference VHDCI (at 0 -27.94) (layer F.SilkS)"
print "    (effects (font (size 1.5 1.5) (thickness 0.15)))"
print "  )"
print "  (fp_text value VAL** (at 0 20.32) (layer F.SilkS)"
print "    (effects (font (size 1.5 1.5) (thickness 0.15)))"
print "  )"

base_x = -16.175

offsets_x = [
	base_x + 3.175,
	base_x + 2.775+0.8+0.4,
	base_x + 2.775,
	base_x + 2.775+0.8]

base_y = 0
offsets_y = [
	base_y + 1.15,
	base_y,
	base_y - 1.2,
	base_y - 1.2 - 1.15
	]


pins = 68

for pin in xrange(1, pins+1):
	if pin <= pins/2:
		y = 2 if (pin % 2 == 1) else 3
		x = (pin-1) / 2
	else:
		y = 0 if (pin % 2 == 1) else 1
		x = (pin-1-(pins/2))/2

	pos_x = offsets_x[y] + x*1.6
	pos_y = offsets_y[y]

	print "  (pad %u thru_hole circle (at %f %f) (size 1 1) (drill 0.6) (layers *.Cu *.Mask F.SilkS) (clearance 0.1))" % (pin, pos_x, pos_y)

print ")"
