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
		self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()

		self.spark.sql("CREATE DATABASE IF NOT EXISTS graph_database")

	def download_pdf(self, url, filepath):
		response = urllib.request.urlopen(url)
		file = open(filepath, "wb")
		file.write(response.read())
		file.close()
		#response = request.get(url, stream=True)

		#try:
		#	with open(filepath, 'wb') as fd:
		#		for chunk in response.iter_content(chunk_size=123):
		#			fd.write(chunk)
		#except:
		#	pass


	def read_pdf(self, filepath):
		self.reader = PdfReader(filepath)
		page = self.reader.pages[0]
		self.text = page.extract_text()

	def text_clean(self):
		self.text = self.text.replace("\n", " ")
		self.text = self.text.replace("\x03", ".")

	def import_text(self, text):
		self.text = text

	def triple_construction(self):
		data = request.get_json() # get the json from the post request object
		source = data['source']
		relation = data['relation']
		#relation_user = data['relationuser']
		target = data['target']
		#id_ = data['id']
		#time = data['time']
		columns = ["source","relation","target"]
		data = [(source,relation,target)]
		df_temp = spark.sparkContext.parallelize(data).toDF(columns)
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





