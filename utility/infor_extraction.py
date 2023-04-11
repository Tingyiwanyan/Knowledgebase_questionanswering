import spacy 
import numpy as np

from spacy.matcher import Matcher


nlp = spacy.load("en_core_web_sm")

text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 

# create a spaCy object 
doc = nlp(text)

for tok in doc: 
  print(tok.text, "-->",tok.dep_,"-->", tok.pos_)