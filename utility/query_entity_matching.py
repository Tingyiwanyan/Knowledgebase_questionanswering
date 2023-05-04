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


	def extract_entities(self, dataframe, obj):
		self.answer_df = df.filter(F.col("target").contains(obj)|F.col("source").contains(obj))
