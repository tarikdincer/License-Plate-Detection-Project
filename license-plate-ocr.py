import sys
import cv2
import numpy as np
import traceback

import darknet.python.darknet as dn

from os.path 				import splitext, basename
from glob					import glob
from darknet.python.darknet import detect
from src.label				import dknet_label_conversion
from src.utils 				import nms


if __name__ == '__main__':

	try:
	
		input_dir  = 'img_out'
		output_dir = 'license_plates'
		tr_plates = True
		ocr_threshold = .1

		ocr_weights = 'data/ocr/ocr-net.weights'
		ocr_netcfg  = 'data/ocr/ocr-net.cfg'
		ocr_dataset = 'data/ocr/ocr-net.data'

		ocr_net  = dn.load_net(ocr_netcfg, ocr_weights, 0)
		ocr_meta = dn.load_meta(ocr_dataset)

		imgs_paths = sorted(glob('%s/*' % input_dir)) 


		print 'Performing OCR...'

		for i,img_path in enumerate(imgs_paths):
			print '\tScanning %s' % img_path

			bname = basename(splitext(img_path)[0])

			R,(width,height) = detect(ocr_net, ocr_meta, img_path ,thresh=ocr_threshold, nms=None)

			if len(R):
				L = dknet_label_conversion(R,width,height)
				L = nms(L,.45)		

				L.sort(key=lambda x: x[0].tl()[0])

				if len(L)>=7 and tr_plates == True:# or len(L)==8:
					for i in L[0]:
						if i.cl()=='I':
							i.set_class('1')
						elif i.cl()=='Z':
							i.set_class('2')
						elif i.cl()=='S':
							i.set_class('5')
						elif chr(i.cl()).isalpha():
							L[0].remove(i)
				
					for i in L[1]:
						if i.cl()=='I':
							i.set_class('1')
						elif i.cl()=='Z':
							i.set_class('2')
						elif i.cl()=='S':
							i.set_class('5')
						elif chr(i.cl()).isalpha():
							L[1].remove(i)

					for i in L[2]:
						if i.cl()=='1':
							i.set_class('I')
						elif i.cl()=='2':
							i.set_class('Z')
						elif i.cl()=='7':
							i.set_class('Z')
						elif i.cl()=='5':
							i.set_class('S')
						elif i.cl()=='0':
							i.set_class('O')
						elif chr(i.cl()).isdigit():
							L[2].remove(i)

					for i in L[3]:
						if i.cl()=='1':
							i.set_class('I')
						elif i.cl()=='2':
							i.set_class('Z')
						elif i.cl()=='7':
							i.set_class('Z')
						elif i.cl()=='5':
							i.set_class('S')
						elif i.cl()=='0':
							i.set_class('O')
						elif chr(i.cl()).isdigit():
							L[3].remove(i)

					for i in L[5]:
						if i.cl()=='I':
							i.set_class('1')
						elif i.cl()=='Z':
							i.set_class('2')
						elif i.cl()=='S':
							i.set_class('5')
						elif chr(i.cl()).isalpha():
							L[5].remove(i)

					for i in L[6]:
						if i.cl()=='I':
							i.set_class('1')
						elif i.cl()=='Z':
							i.set_class('2')
						elif i.cl()=='S':
							i.set_class('5')
						elif chr(i.cl()).isalpha():
							L[6].remove(i)

					if len(L)>7:
						for i in L[7]:
							if i.cl()=='I':
								i.set_class('1')
							elif i.cl()=='Z':
								i.set_class('2')
							elif i.cl()=='S':
								i.set_class('5')
							elif chr(i.cl()).isalpha():
								L[7].remove(i)
				
				
				#lp_str = ''.join([chr(l[0].cl()) for l in L])
				lp_str = ''
				for possible_chars in L:
					if len(possible_chars) == 1:
						lp_str = lp_str+'\t'+chr(possible_chars[0].cl())+': %'+str(int(100*possible_chars[0].prob()))+'\n '
					else:
						lp_str = lp_str + '\t'
						for i,ch in enumerate(possible_chars):
							if i != (len(possible_chars)-1):
								lp_str = lp_str+chr(ch.cl())+': %'+str(int(100*ch.prob()))+','
							else:
						 		lp_str = lp_str+chr(ch.cl())+': %'+str(int(100*ch.prob()))
						lp_str = lp_str + '\n '
				lp_most = ''
				if len(L) > 5:

					for lp in L:
						if len(lp) > 0:
							lp_most = lp_most + chr(lp[0].cl())
						else:
							lp_most = lp_most + '-'

					with open('%s/%s_str.txt' % (output_dir,bname),'w') as f:
						f.write('Muhtemel Plaka: '+lp_most + '\n'+'Ihtimal Degerler: '+lp_str)

					print '\n\tEn Yuksek Ihtimalli Plaka: %s' % lp_most +'\n'
					print '\tPlaka Muhtemel Harf Listesi:\n %s' % lp_str
					

			else:

				print 'Hicbir karakter bulunamadi'

	except:
		traceback.print_exc()
		sys.exit(1)

	sys.exit(0)
