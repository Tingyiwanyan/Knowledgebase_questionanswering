from utility.infor_extraction import info_extractor


if __name__ == '__main__':
	info_ext = info_extractor()
	text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 
	info_ext.subtree_matcher(text)