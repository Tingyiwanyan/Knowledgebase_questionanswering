from utility.infor_extraction import info_extractor
from spacy import displacy


if __name__ == '__main__':
	info_ext = info_extractor()
	text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 
	text2 = "Tableau was recently acquired by Salesforce." 
	text3 = "AnalyticsVidhya is the largest community of data scientists and provides best resources for understanding data and analytics."
	x,y,z = info_ext.subtree_matcher(text)