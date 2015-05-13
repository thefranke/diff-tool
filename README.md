# diff-tool

This tool is used to visualize the difference of two input images. To do this, the squared differnce of the luminance of each pixel is amplified by a user-supplied factor (the default is 1). The output shows positive and negative differences as a heatmap.

# Usage

This is a sample input

    $ diff.py -i render.png -g groundtruth.png -x 4

In this case the generated output is called "render_diff.png". It will show the squared difference times four.

    Usage: diff.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -g FILE_GROUNDTRUTH, --groundtruth=FILE_GROUNDTRUTH
                            The image of the ground truth.
      -i FILE_IMAGE, --image=FILE_IMAGE
                            The image of the new method.
      -m FILE_MASK, --mask=FILE_MASK
                            An optional binary mask.
      -x MULTIPLIER, --multiplier=MULTIPLIER
                            Multiply difference by this amount
      -o, --output-mse      Prints  mean square error

# Troubleshooting

If you are running the script on Windows you can look here for additional libraries:
http://www.lfd.uci.edu/~gohlke/pythonlibs/
