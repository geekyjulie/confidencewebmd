from bs4 import BeautifulSoup
import urllib2
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import codecs
import os

import dp2

connect_words_list=[]

connect_list=open("connecting_words_list.txt",'r')

#This creates a list of connecting words that will be used in searching in the web page content result
for line in connect_list:
	line=line.rstrip()
	if ('\xef\xbb\xbf' in line):
		line=line.strip('\xef\xbb\xbf')
	connect_words_list.append(line)


def scraping(url,mode):

	myList=defaultdict(list)

	print myList
	length=len(url)
	url_array=url
	for i in xrange(0,length):	
		hdr={'User-Agent': 'Mozilla/5.0'}
		urlname=url_array[i]
		req=urllib2.Request(urlname,headers=hdr)
		page=urllib2.urlopen(req)
		soup=BeautifulSoup(page.read(),"html.parser")

		extract=soup.findAll('script')

		for item in extract:
			item.extract()

		text=soup.get_text()
		text=text.encode("utf-8")
		print "Strip off the contents done"

		filename='sample_'+mode+'.txt'
		outf=open(filename, 'a')
		outf.write(text)

	#So this generates words 
	
	word_list=codecs.open(filename,"r",encoding='utf8')

	stops = set(stopwords.words('english'))

	result_file_name='result_file_'+mode+'.txt'
	rfile=open(result_file_name,'w')

	for line in word_list:
		if ('Previous Page' in line ) or ('Next Page' in line):
			pass
		else:
			try:	
				if (len(str(line)) <= 1):
					pass
				tokenarray=nltk.word_tokenize(str(line))
				#print tokenarray

				if(len(tokenarray) != 0):
					
					for conn_word in connect_words_list:
						#print conn_word
						if (conn_word in tokenarray):
							#print "passed"
							#print conn_word
							#print line
							if (line not in myList[conn_word]):
								myList[conn_word].append(line)
							
							rfile.write("Connecting word: " + conn_word + "\n")
							rfile.write(line + "\n")
							
							index=tokenarray.index(conn_word)
							
			except UnicodeError:
				#print "unicode error here"
				pass
	return myList

def fun_main():
	
	webmdurl=["http://www.webmd.com/heart-disease/guide/diseases-cardiovascular",
	 "http://www.webmd.com/heart-disease/guide/diseases-cardiovascular?page=2",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-overview-facts",
 	 "http://www.webmd.com/heart-disease/guide/heart-disease-risk-factors",
	 "http://www.webmd.com/heart-disease/guide/homocysteine-risk",
	 "http://www.webmd.com/heart-disease/guide/metabolic-syndrome",
	 "http://www.webmd.com/heart-disease/guide/metabolic-syndrome?page=2",
	 "http://www.webmd.com/heart-disease/guide/metabolic-syndrome?page=3",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-diagnosis-tests",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-treatment-care",
	 "http://www.webmd.com/heart-disease/guide/cpr",
	 "http://www.webmd.com/heart-disease/guide/understanding-heart-disease-treatment",
	 "http://www.webmd.com/heart-disease/guide/understanding-heart-disease-treatment?page=2",
	 "http://www.webmd.com/heart-disease/guide/understanding-heart-disease-treatment?page=3",
	 "http://www.webmd.com/heart-disease/guide/stents-types-and-uses",
	 "http://www.webmd.com/heart-disease/guide/stents-types-and-uses?page=2",
	 "http://www.webmd.com/heart-disease/guide/stents-types-and-uses?page=3",
	 "http://www.webmd.com/heart-disease/guide/treatment-angioplasty-stents",
	 "http://www.webmd.com/heart-disease/guide/treatment-angioplasty-stents?page=2",
	 "http://www.webmd.com/heart-disease/guide/treatment-angioplasty-stents?page=3",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-bypass-surgery",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-bypass-surgery?page=2",
	 "http://www.webmd.com/heart-disease/guide/valve-disease-treatment",
	 "http://www.webmd.com/heart-disease/guide/valve-disease-treatment?page=2",
	 "http://www.webmd.com/heart-disease/guide/valve-disease-treatment?page=3",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-cardioversion",
	 "http://www.webmd.com/heart-disease/guide/treating-chronic-angina-eecp",
	 "http://www.webmd.com/heart-disease/guide/what-is-cardiac-ablation",
	 "http://www.webmd.com/heart-disease/guide/what-is-cardiac-ablation?page=2",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythyms-pacemaker",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythyms-pacemaker?page=2",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythyms-pacemaker?page=3",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythyms-pacemaker?page=4",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythyms-pacemaker?page=5",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythms-icd",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythms-icd?page=2",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythms-icd?page=3",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythms-icd?page=4",
	 "http://www.webmd.com/heart-disease/guide/abnormal-rhythms-icd?page=5",
	 "http://www.webmd.com/heart-disease/guide/lead-extraction",
	 "http://www.webmd.com/heart-disease/guide/lead-extraction?page=2",
	 "http://www.webmd.com/heart-disease/guide/treating-left-ventricular-device",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment?page=2",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment?page=3",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment?page=4",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment?page=5",
	 "http://www.webmd.com/heart-disease/guide/transplantation-treatment?page=6",
	 "http://www.webmd.com/heart-disease/guide/medicine-ace-inhibitors",
	 "http://www.webmd.com/heart-disease/guide/medicine-ace-inhibitors?page=2",
	 "http://www.webmd.com/heart-disease/guide/medicine-ace-inhibitors?page=3",
	 "http://www.webmd.com/heart-disease/guide/medicine-angiotension-ii",
	 "http://www.webmd.com/heart-disease/guide/medicine-angiotension-ii?page=2",
	 "http://www.webmd.com/heart-disease/guide/medicine-antiarrhythmics",
	 "http://www.webmd.com/heart-disease/guide/medicine-antiarrhythmics",
	 "http://www.webmd.com/heart-disease/guide/antiplatelet-drugs",
	 "http://www.webmd.com/heart-disease/guide/antiplatelet-drugs?page=2",
	 "http://www.webmd.com/heart-disease/guide/aspirin-therapy",
	 "http://www.webmd.com/heart-disease/guide/aspirin-therapy?page=2",
	 "http://www.webmd.com/heart-disease/guide/aspirin-therapy?page=3",
	 "http://www.webmd.com/heart-disease/guide/beta-blocker-therapy",
	 "http://www.webmd.com/heart-disease/guide/beta-blocker-therapy?page=2",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-calcium-channel-blocker-drugs",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-calcium-channel-blocker-drugs?page=2",
	 "http://www.webmd.com/heart-disease/guide/medicine-clot-busters",
	 "http://www.webmd.com/heart-disease/guide/medicine-clot-busters?page=2",
	 "http://www.webmd.com/heart-disease/guide/treatment-digoxin",
	 "http://www.webmd.com/heart-disease/guide/treatment-digoxin?page=2",
	 "http://www.webmd.com/heart-disease/guide/medicine-diuretics",
	 "http://www.webmd.com/heart-disease/guide/medicine-diuretics?page=2",
	 "http://www.webmd.com/heart-disease/guide/medicine-diuretics?page=3",
	 "http://www.webmd.com/heart-disease/guide/warfarin-other-blood-thinners",
	 "http://www.webmd.com/heart-disease/guide/warfarin-other-blood-thinners?page=2",
	 "http://www.webmd.com/heart-disease/guide/warfarin-other-blood-thinners?page=3",
	 "http://www.webmd.com/heart-disease/guide/plant-based-diet-for-heart-health",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-recovering-after-heart-surgery",
	 "http://www.webmd.com/heart-disease/guide/heart-disease-recovering-after-heart-surgery?page=2",
	 "http://www.webmd.com/heart-disease/guide/strength-tough-times"

	]
	
	wikiurl=["https://en.wikipedia.org/wiki/Myocardial_infarction"]

	wikiList=defaultdict(list)
	
	print "Starting webmd stuff"
	webmd_list=defaultdict(list)
	webmd_list=scraping(webmdurl,'webmd')
	#print webmd_list
	print "Done\n"
	print "====webmd list====="

	print "Starting wiki stuff"
	wiki_list=defaultdict(list)
	wiki_list=scraping(wikiurl,'wiki')
	#print wiki_list
	print "Done\n"
	print "====wiki list====="
	

	os.remove('./sample_webmd.txt')
	os.remove('./sample_wiki.txt')
	#print webmd_list['develop']
	#print "\n"
	#print wiki_list['develop']
	print "combine senteces from both lists for each keyword\n"
	tempcount=0
	for key in webmd_list:
		if (key in webmd_list) and (key in wiki_list):
			temp_array=[]
			webmd_count=0
			count=0
			print key+'\n'
			for line in webmd_list[key]:
				print str(count) + " : " + line
				webmd_count += 1
				count += 1
				temp_array.append(line)
			print "\n" + "webmd combined is done\n"
			for line in wiki_list[key]:
				print str(count) + " : " + line
				count += 1
				temp_array.append(line)
			#print temp_array
			print "Webmd index ends at" + str(webmd_count-1)
			print "\n"
			dp2.compare(temp_array, webmd_count)


if __name__=="__main__":

	fun_main()





