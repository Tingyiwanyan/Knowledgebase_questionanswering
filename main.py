from utility.infor_extraction import info_extractor
from spacy import displacy
from utility.text_kg_generation import kg_construct


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
	text9 = "what is watercycle"
	text10 = "john scored 98"
	sample_url = "https://s22.q4cdn.com/959853165/files/doc_financials/2021/q4/da27d24b-9358-4b5c-a424-6da061d91836.pdf"

	kg = kg_construct()
	#info_ext.entity_matcher()