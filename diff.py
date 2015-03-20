#!/usr/bin/env python

# Diff-tool
# Copyright (c) 2013 Tobias Alexander Franke
# http://www.tobias-franke.eu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pylab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
import numpy as np
import sys
import optparse

# helper to create new colormap
def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def create_error_image(file_groundtruth, file_image, file_mask, file_out, multiplier):
	# define custom colormap
	c = mcolors.ColorConverter().to_rgb
	rvb = make_colormap([ c('yellow'), c('red'), 0.25, c('red'), c('black'), 0.5, c('black'), c('blue'), 0.75, c('blue'), c('white') ])

	# load images
	groundtruth = mpimg.imread(file_groundtruth)
	image = mpimg.imread(file_image)

	if file_mask != None:
	    img_mask = mpimg.imread(file_mask)[:,:,0]

	# convert to luminance images
	lum1 = groundtruth[:,:,0]*0.2126 	+ groundtruth[:,:,1]*0.7152 	+ groundtruth[:,:,2]*0.0722
	lum2 = image[:,:,0]*0.2126 			+ image[:,:,1]*0.7152 			+ image[:,:,2]*0.0722

	# error per component [-1, 1]
	difference = np.subtract(lum2, lum1)

	# error squared
	abs_error_squared = np.square(np.fabs(difference)+1.0)-1.0

	# back to [-1, 1] range
	abs_error_squared = np.multiply(abs_error_squared, np.sign(difference))

	# upper and lower clip bound
	error = abs_error_squared * multiplier

	if file_mask != None:
	    error = np.multiply(error, img_mask)

	# find maximum value
	max_scale = np.max(np.fabs(error))
	max_scale = 1

	# render the plot
	imgplot = plt.imshow(error)

	# choose a color palette
	imgplot.set_cmap(rvb)
	imgplot.set_clim(-max_scale, max_scale)

	# make layout tighter
	plt.axis('off')
	from mpl_toolkits.axes_grid1 import make_axes_locatable
	divider = make_axes_locatable(plt.gca())
	cax = divider.append_axes("right", "5%", pad="1%")
	plt.colorbar(imgplot, cax=cax)
	plt.tight_layout()

	F = pylab.gcf()
	the_dpi = 192
	width  = len(image[0])/the_dpi + 8
	height = len(image)/the_dpi + 5
	#F.set_size_inches(width, height)
	F.savefig(file_out, dpi=the_dpi, bbox_inches='tight', pad_inches=0)


parser = optparse.OptionParser()
parser.add_option("-g", "--groundtruth", dest="file_groundtruth", help="The image of the ground truth.")
parser.add_option("-i", "--image", dest="file_image", help="The image of the new method.")
parser.add_option("-m", "--mask", dest="file_mask", help="An optional binary mask.", default=None)
parser.add_option("-x", "--multiplier", type="int", dest="multiplier", help="Multiply difference by this amount", default=8)

(options, args) = parser.parse_args()

if options.file_groundtruth and options.file_image:

	if len(args) == 0:
		options.file_output = options.file_image[:-4] + "_diff.png"
	else:
		options.file_output = args[0]

	create_error_image(options.file_groundtruth, options.file_image, options.file_mask, options.file_output, options.multiplier)
else:
	parser.print_help()