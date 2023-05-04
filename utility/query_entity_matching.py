import spacy 
import numpy as np
from utility.infor_extraction import info_extractor
from pyspark.sql import functions as F

class query_matching(info_extractor):
	def __init__(self):
		info_extractor.__init__(self)

	def query_analyze(self,query_text):
		doc = self.nlp(query_text)
		query_entity = []
		for tok in doc:
			print(tok.head.text,"-->",tok.text,"-->",tok.dep_,"-->",tok.pos_)
			if not tok.pos_ == "PRON" and not tok.pos_ == "DET" and not tok.pos_ == "AUX" and not tok.pos_ == "VERB" and not tok.pos_ == "ADV" and not tok.pos_ == "PUNCT" and not tok.pos_ == "ADV":
				query_entity.append(tok.text)
		print(query_entity)
		self.query_entity = query_entity


	def extract_entities(self, dataframe):

		answer_tables = []
		for entity in self.query_entity:
			answer_df = dataframe.filter(F.col("target").contains(entity)|F.col("source").contains(entity))
			answer_tables.append(answer_df)
		if not len(answer_tables) == 1:
			join_table = answer_tables[0]
			for i in range(len(answer_tables)):
				join_table = join_table.union(answer_tables[i]).dropDuplicates()
			self.answer_table = join_table
		else:
			self.answer_table = answer_tables[0]

	def return_triple_sentences(self):
		df = self.answer_table.toPandas()
		sources = df['source']
		relation = df['relation']
		target = df['target']
		sentences = ''
		for i in range(len(sources)):
			text = sources[i] + ' ' + relation[i] + ' '+ target[i]
			sentences = sentences + text + '. '

		self.returned_sentences = sentences
		#return sentences

	def keyword_entity_extraction(self, query_text, dataframe):
		self.query_analyze(query_text)
		self.extract_entities(dataframe)
		self.return_triple_sentences()
		if sentences == '':
			print("There is no information related to the query:")
			for i in self.query_entity:
				print(i)
		else:
			return self.sentences

			






