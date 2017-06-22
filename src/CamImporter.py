#!/usr/bin/env python
#
# version: v1.0
# author: francesco.pantano@linux.com
#

import os
import sys
import datetime
import logging
import config
from FileHandler import FileHandler
from ImageHandler import ImageHandler as ImageObject
from utils.parser import Parser as Parser
from utils.ConsoleUtils import ANSIColors as colorize


logging.basicConfig(filename='/tmp/exifimporter.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)

cc = colorize()


class CameraImporter(Parser):


	def __init__(self):
		super(CameraImporter, self).__init__(config.parameters_json_file_source)

	def parse(self):
		self.configure = self.raw_json
		print(self.configure['globals'])
		# Build the global attributes
		for key, value in self.configure.get("globals").items():
			setattr(self, key, value)
			LOG.debug("[CameraImporter] Acquiring attribute [%s] with default value [%s]" % (key, str(value)))
	
	def __setattr__(self, key, value):
		self.__dict__[key] = value


	def instlookup(self, name):
		True if name in self.__dict__.keys() else False


	def import_objects(self):
		try:
			f = FileHandler(self.ingress, self.egress, self.deep, self.configure['statistics']['header'])
			for im in f.flist():
				if not f.blacklisted(im):
					LOG.debug("[FileHandler] |/ Analyzing image [%s] " % im)
					cc.s_success("[FileHandler] ", "|/ Analyzing image [%s] " % im)
					next_img = ImageObject(im, f.deep)
					if next_img.reference:
						LOG.debug("[FileHandler] |/ Building [%s] " % (f.egress + next_img.dpath))
						cc.s_success("[FileHandler] ", "|/ Building [%s] " % (f.egress + next_img.dpath))
						f.os_dest_path(next_img.dpath)
						#print("[FileHandler] |/ Processing Image [%s] " % im)
					else:
						LOG.warning("[FileHandler] |x Skipping file [%s] " % im)
						cc.s_warning("[FileHandler] |x Skipping file [%s] " % im)
				else:
					LOG.error("[FileHandler] |x Skipping file [%s] => BLACKLISTED " % im)
					cc.s_error("[FileHandler] |x Skipping file [%s] => BLACKLISTED " % im)
			f.stats()
		except Exception as e:
		#TODO: Raise the correct exception...
			print(e)

if __name__ == "__main__":
	c = CameraImporter()
	c.parse()
	c.import_objects()
