# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class BaldorCadItem(Item):
	ids = Field()
	catalog_number = Field()
	description = Field()
	pdf_2d = Field()
	dxf_2d = Field()
	dxf_3d = Field()


class BaldorImgItem(Item):
	ids = Field()
	catalog_number = Field()
	description = Field()
	main_image = Field()
	ship_weight = Field()


class BearCadItem(Item):
	ids = Field()
	catalog_number = Field()
	cad = Field()


class BearImgItem(Item):
	ids = Field()
	catalog_number = Field()
	main_image = Field()
	additional_descriptions = Field()


class DixonItem(Item):
	ids = Field()
	name = Field()
	url = Field()


class DixonImgItem(Item):
	ids = Field()
	catalog_number = Field()
	description = Field()
	main_image = Field()
	response_url = Field()


class GatesItem(Item):
	ids = Field()
	catalog_number = Field()
	cad = Field()


class HubellItem(Item):
	ids = Field()
	catalog_number = Field()
	url_page = Field()
	Product_Drawing_PDF = Field()
	Product_Drawing_DWG = Field()
	Installation_Instructions = Field()


class McrsafetyItem(Item):
	ids = Field()
	catalog_number = Field()
	image = Field()
	document_name = Field()
	document_url = Field()
	additional_description = Field()
	features = Field()
	specs = Field() 
	industry_application = Field()


class MetropacItem(Item):
	catalog_number = Field()
	retail = Field()
	your_price = Field()


class MotionItem(Item):
	# ids = Field()
	# catalog_number = Field()
	# description = Field()
	# main_image = Field()
	# response_url = Field()
	code = Field()
	mi_item = Field()


class RegalItem(Item):
	ids = Field()
	catalog_number = Field()
	cad = Field()
	# main_image = Field()
	# ship_weight = Field()


class RexnordItem(Item):
	ids = Field()
	catalog_number = Field()
	attributes = Field()


class RexnordCadItem(Item):
	ids = Field()
	catalog_number = Field()
	cadid = Field()


class RingspanncorpItem(Item):
	ids = Field()
	catalog_number = Field()
	description = Field()
	main_image = Field()
	key = Field()
	name_datasheet = Field()
	url_datasheet = Field()
	response_url = Field()


class RingspanncorpCadItem(Item):
	ids = Field()
	catalog_number = Field()
	cad_url = Field()


class SkfItem(Item):
	ids = Field()
	catalog_number = Field()
	file_urls = Field()
	files = Field()


class StatesItem(Item):
	ids = Field()
	catalog_number = Field()
	description = Field()


class TecoItem(Item):
	ids = Field()
	catalog_number = Field()
	attributes = Field()


class TecoDocsItem(Item):
	ids = Field()
	catalog_number = Field()
	name = Field()
	document = Field()