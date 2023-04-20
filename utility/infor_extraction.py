import spacy 
import numpy as np

from spacy.matcher import Matcher


class info_extractor():
  def __init__(self):
    self.nlp = spacy.load("en_core_web_sm")

    #text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 

# create a spaCy object 
  def subtree_matcher(self, text):

    doc = self.nlp(text)

    subjpass = 0

    for i,tok in enumerate(doc):
      # find dependency tag that contains the text "subjpass"    
      if tok.dep_.find("subjpass") == True:
        subjpass = 1

    x = ''
    y = ''
    z = ''
    pre_tok_text = ''
    pre_tok_dep = ''
    suf_tok_text = ''
    suf_tok_dep = ''
    prefix = ''
    suffix = ''
    modifier = ''

    matcher = Matcher(self.nlp.vocab)


    # if subjpass == 1 then sentence is passive
    #if subjpass == 1:
    pattern = [{'DEP':'subj','OP':"?"},
               {'DPE':'ROOT','OP':"?"},
               {'DPE':'obj'}]

    matcher.add("matching_1", None, pattern)
    matcher = matcher(doc)



      """
      for i,tok in enumerate(doc):
        if not tok.dep_ == "punct":
          if tok.dep_.endswith("mod"):
            prefix = prefix + " " + tok.text
          if tok.dep_.find("subjpass") == True:
            y = tok.text

          if tok.dep_.endswith("obj") == True:
            x = tok.text

          if tok.dep_.endswith("ROOT") == True:
            z = tok.text
      """
    
    # if subjpass == 0 then sentence is not passive
    """
    else:
      for i,tok in enumerate(doc):
        if tok.dep_.endswith("subj") == True:
          x = tok.text

        if tok.dep_.endswith("obj") == True:
          y = tok.text

        if tok.dep_.endswith("ROOT") == True:
          z = tok.text
    """
    #return x,y,z
