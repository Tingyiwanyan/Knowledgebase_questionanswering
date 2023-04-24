from utility.infor_extraction import info_extractor
from spacy import displacy


if __name__ == '__main__':
	info_ext = info_extractor()
	text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 
	text2 = "Tableau was recently acquired by Salesforce." 
	text3 = "AnalyticsVidhya is the largest community of data scientists and will provides best resources for understanding data and analytics."
	text4 = "James is the leader who is nice"
	text5 = "James plays in his room"
	text6 = "james and lucy are friends"
	text7 = "moved by james, lucy went out"
	text8 = "The accident happened as the night was falling"
	#info_ext.entity_matcher()