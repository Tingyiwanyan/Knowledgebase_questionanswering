from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
import pandas as pd
from utility.infor_extraction import info_extractor
from PyPDF2 import PdfReader
import requests
import urllib
import re


class kg_construct(info_extractor):
	def __init__(self):
		info_extractor.__init__(self)
		self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()

		self.spark.sql("CREATE DATABASE IF NOT EXISTS graph_database")


	def download_pdf(self, url, filepath):
		response = urllib.request.urlopen(url)
		file = open(filepath, "wb")
		file.write(response.read())
		file.close()
	
	def core(self, filepath):
		self.read_pdf(filepath)
		self.text_clean()
		self.sentence_divider()
		valid_sentence = 1
		for texts in self.sentences:
			self.construct_triples(texts)
			if self.sentence_structure['prefix'] == []:
				valid_sentence = 0
			if self.sentence_structure['suffix'] == []:
				valid_sentence = 0
			if self.sentence_structure['verb_relation'] == []:
				valid_sentence = 0
			if not valid_sentence == 0:
				self.triple_construction(texts)
			valid_sentence = 1

	def read_pdf(self, filepath):
		self.reader = PdfReader(filepath)
		page = self.reader.pages[0]
		self.text = page.extract_text()
		self.text_origin = self.text

	def text_clean(self):
		self.text = self.text.replace("\n", " ")
		self.text = self.text.replace("\x03", ".")

	def import_text(self, text):
		self.text = text

	def convert_to_text(self,list_text):
		l = []
		for x in list_text:
			l = l + x
		m_string = ''
		for x in l:
			m_string += ' ' + str(x)

		return m_string


	def triple_construction(self,texts):
		#data = request.get_json() # get the json from the post request object

		source  = self.sentence_structure['prefix']
		source = self.convert_to_text(source)
		self.check_source = source
		#source = data['source']
		relation = self.sentence_structure['verb_relation']
		relation = self.convert_to_text(relation)
		self.check_relation = relation
		#relation_user = data['relationuser']
		target = self.sentence_structure['suffix']
		target = self.convert_to_text(target)
		self.check_target = target
		#id_ = data['id']
		#time = data['time']
		columns = ["source","relation","target"]
		data = [(source,relation,target)]
		df_temp = self.spark.sparkContext.parallelize(data).toDF(columns)
		tables = self.spark.catalog.listTables("graph_database")
		if "triple_relation" in [table.name for table in tables]:
			df_temp.write.mode('append').saveAsTable("graph_database.triple_relation")
		else:
			df_temp.write.mode('overwrite').saveAsTable("graph_database.triple_relation")


	def sentence_divider(self):
		"""
		generate each individual sentence from paragraph
		"""
		self.sentences = [x for x in re.split("[//.|//!|//?|\n]", self.text) if x!=""]





