import sys, os
import keras
import cv2
import traceback

from src.keras_utils 			import load_model
from glob 						import glob
from os.path 					import splitext, basename
from src.utils 					import im2single
from src.keras_utils 			import load_model, detect_lp
from src.label 					import Shape, writeShapes


def adjust_pts(pts,lroi):
	return pts*lroi.wh().reshape((2,1)) + lroi.tl().reshape((2,1))


if __name__ == '__main__':

	try:
		vehicle_on = False
		if vehicle_on == False:
			input_dir  = 'img'
		else:
			input_dir = 'detected_cars'
		output_dir = 'img_out'

		lp_threshold = .7

		wpod_net_path = "data/lp-detector/wpod-net_update1.h5"
		wpod_net = load_model(wpod_net_path)

		imgs_paths = glob('%s/*' % input_dir)

		print 'Searching for license plates using WPOD-NET'

		for i,img_path in enumerate(imgs_paths):

			print '\t Processing %s' % img_path

			bname = splitext(basename(img_path))[0]
			Ivehicle = cv2.imread(img_path)

			ratio = float(max(Ivehicle.shape[:2]))/min(Ivehicle.shape[:2])
			side  = int(ratio*288.)
			bound_dim = min(side + (side%(2**4)),608)
			print "\t\tBound dim: %d, ratio: %f" % (bound_dim,ratio)

			Llp,LlpImgs,_ = detect_lp(wpod_net,im2single(Ivehicle),bound_dim,2**4,(240,80),lp_threshold)	
			for i,lpt in enumerate(LlpImgs):
				#cv2.imwrite('a%s/%s_lp.png' % (output_dir,bname),lpt)
				if len(LlpImgs):
					Ilp = lpt
					Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
					Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)

					s = Shape(Llp[i].pts)

					cv2.imwrite('%s/%s%d_lp.png' % (output_dir,bname,i),Ilp*255.)
					writeShapes('%s/%s%d_lp.txt' % ('points',bname,i),[s])

	except:
		traceback.print_exc()
		sys.exit(1)

	sys.exit(0)


