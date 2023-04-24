import spacy 
import numpy as np

from spacy.matcher import Matcher


class info_extractor():
  def __init__(self):
    self.nlp = spacy.load("en_core_web_sm")
    self.sentence_structure = {}
    self.sentence_structure["prefix"] = []
    self.sentence_structure["suffix"] = []
    self.sentence_structure["conj_suffix"] = []
    self.sentence_structure["verb_relation"] = []
    self.sentence_structure["verb_conj_relation"] = []

  def purge_sentence_structure(self):
    self.sentence_structure["prefix"] = []
    self.sentence_structure["suffix"] = []
    self.sentence_structure["conj_suffix"] = []
    self.sentence_structure["verb_relation"] = []
    self.sentence_structure["verb_conj_relation"] = []

  def entity_matcher(self):
    matcher = Matcher(self.nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    pattern = [{"LOWER": "is"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    matcher.add("HelloWorld", [pattern])

    doc = self.nlp("Hello , is world! Hello world!")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = self.nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)

  def construct_triples(self,texts):
    doc = self.nlp(texts)

    for tok in doc:
      if tok.dep_.endswith("ROOT") == True:
        root = tok

    self.recursive_dependency(root)

  def right_conj_suffix_recur(self, token):
    verb_text = []
    verb_text.append(token.text)
    for subtok in token.lefts:
      if not subtok.dep_ == "cc" and not subtok.dep_ == "punct":
        if list(subtok.children) == []:
          if subtok.dep_ == "aux":
            verb_text.insert(0,subtok.text)
    self.sentence_structure["verb_conj_relation"].append(verb_text)
    for subtok in token.rights:
      if not subtok.dep_ == "cc" and not subtok.dep_ == "punct":
        if subtok.dep_ == "conj":
          self.right_conj_suffix_recur(subtok)
        else:
          self.sentence_structure["conj_suffix"].append(list(subtok.subtree))


  def recursive_dependency(self,root):

    verb_text = []
    verb_text.append(root.text)
    for tok in root.lefts:
      if not tok.dep_ == "cc" and not tok.dep_ == "punct":
        if list(tok.children) == []:
          if not tok.dep_.endswith("subj") and not tok.dep_.endswith("obj") and not tok.dep_.endswith("subjpass"):
            verb_text.insert(0,tok.text)
          else:
            subtrees = list(tok.subtree)
            self.sentence_structure["prefix"].append(subtrees)
        else:
          subtrees = list(tok.subtree)
          self.sentence_structure["prefix"].append(subtrees)
    #verb_text.append("root")
    self.sentence_structure["verb_relation"].append(verb_text)
    verb_text = []
    for tok in root.rights:
      if not tok.dep_ == "cc" and not tok.dep_ == "punct":
        if tok.dep_.endswith("conj"):
          self.right_conj_suffix_recur(tok)
        else:
          print(tok.text)
          self.sentence_structure["suffix"].append(list(tok.subtree))

    if not verb_text == []:
      #verb_text.append("conj")
      self.sentence_structure["verb_relation"].append(verb_text)
      verb_text = []




