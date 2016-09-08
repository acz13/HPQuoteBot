
#IMPORTS
import re
from bs4 import BeautifulSoup
import time
import threading
import codecs
import os

#LOADING TO DISK
titles=[]
titles.append(('Harry Potter and the Sorcerer\'s Stone',17)) #book name,number of chapters
titles.append(('Harry Potter and the Chamber of Secrets',18))
titles.append(('Harry Potter and the Prisoner of Azkaban',22))
titles.append(('Harry Potter and the Goblet of Fire',37))
titles.append(('Harry Potter and the Order of the Phoenix',38))
titles.append(('Harry Potter and the Half-Blood Prince',30))
titles.append(('Harry Potter and the Deathly Hallows',37))
titles.append(('Fantastic Beasts and Where to Find Them',1))

chapterdata=[]
link=os.getcwd()+'//data'
i=1
for folders in titles:
	# print(link+'//'+str(i)+'//chapterdata.txt')
	# f=codecs.open(link+'//'+str(i))
	f=open(link+'//chapterdata//'+str(i)+'//pagenumbers.txt','r')
	chapterdata.append(f.readlines())
	# print(f.readlines())
	f.close()
	i+=1
	
def getPageNum(tuple):
	# book,chapter,paragraph
	book_number=tuple[0]
	chapter_number=tuple[1]
	paragraph_number=float(tuple[2]-1)
	
	pages_in_chapter=int(chapterdata[book_number-1][chapter_number])-int(chapterdata[book_number-1][chapter_number-1])
	print(pages_in_chapter)
	
	starting_page=int(chapterdata[book_number-1][chapter_number-1])
	print(starting_page)
	
	max_paragraph_number=(len(activeDocuments[book_number-1][2]))
	# input()
	# max_paragraph_number=
	position=paragraph_number/max_paragraph_number
	print(position)
	
	return (int(position * pages_in_chapter) + starting_page)#percent through the chapter we are
	# print(float(tuple[0]))
	# return chapterdata[int(tuple[0])][int(tuple[1])] #page number our chapter starts on

# str(getPageNumtitles(str([book-1][0]),str(chapter),str(paragraph+1)))
	
j=1
link=os.getcwd()+'//data'
activeDocuments=[]
full_arr=[]
for (title,length) in titles:
	for i in range(length):
		i+=1
		arr=codecs.open(link+'//'+str(j)+'//'+str(i)+'.txt','r',encoding='utf_8').readlines()
		for element in arr:
			tmp=str(re.sub(r'[^A-Za-z0-9]','', element))
			full_arr.append(tmp.lower())
		activeDocuments.append((j,i,arr))
		# print('Book '+str(j)+' and chapter '+str(i)+' and paragraphs '+str(len(arr)))
	j+=1

print()
# print(str(len(activeDocuments[0][2])))
print()
	
# for elements in range(1,int(chapterdata[0])+1):
	# print(elements)
	# break
	

# print(getPageNum((3,94,1))) #book,chapter,paragraph
	
# input()

	
print('Finished Loading.')

def printf(u):
	print(re.sub(r'[^\x00-\x7F]',' ', str(u)))

sub_name='harrypotter'

main_running_var=0

while(True):
	try:
		if main_running_var == 0:
			print('Beginning first iteration.')
			import praw 
			
			r=praw.Reddit(user_agent="HPQUOTE/0.1 by anonymous853")

			# s3 = S3Client(os.environ['REDDIT_PASSWORD'])
			# s3='q2w345'
			r.login('[]','[]',disable_warning=True)
			try:
				threads=r.get_subreddit(sub_name).get_comments(limit=1)
			except Exception as e:
				print('Error,',e)
			
			for submission in threads:
				f=open('time.txt','w+')
				f.write(str(submission.created_utc))
				f.close()
		elif main_running_var > 1440:
				main_running_var=0
		
		print(main_running_var)
		
		main_running_var+=1
		
		print('Starting Main Function.')

		out=r.get_subreddit(sub_name).get_comments(limit=100)
		threads=r.get_subreddit(sub_name).get_new(limit=100)
		
		htmlarr=[]

		f=open('time.txt','r')
		created_utc=float(f.read())
		f.close()

		i=0
		new_arr=[]
		
		for submission in threads:
			if submission.is_self == True:
				if str(submission.author) != 'hpquotebot': #continue
					if submission.selftext_html is not None:
						if submission.created_utc <= created_utc:
							break
						print(submission.permalink)
						tmp_link=submission.permalink
						new_arr.append(submission)
						htmlarr.append((submission.selftext_html,tmp_link)) # we need the link and the body html (for searching)
						if i==0:
							created_utc=submission.created_utc #most recent post
							i=1

		for submission in out:
			if str(submission.author) != 'hpquotebot':
				if submission.created_utc <= created_utc:
					break
				print(submission.permalink)
				tmp_link=submission.permalink
				new_arr.append(submission)
				htmlarr.append((submission.body_html,tmp_link))
				if i==0:
					created_utc=submission.created_utc
					i=1

		f=open('time.txt','w+')
		f.write(str(created_utc))
		f.close()
		
		print()

		if len(htmlarr) == 0:
			print('Didn\'t detect any new quotes')

		
		#SEARCHING RETRIEVED POST FOR QUOTES
		for (htmlpoint,link_to_post) in htmlarr:
			soup=BeautifulSoup(htmlpoint,'html.parser')

			outFind=[]
			for element in soup.findAll('div'):
				for line in soup.findAll('blockquote'):
					outFind.append(line.text)
			if len(outFind)==0:
				print('Did not find Quote, stopping.')
				print()
				continue
			else:
				print('Found Quote, Continuing.')

			final=[] #has simplified quote for searching with
			final2=[] #only has extended quote
			for outquote in outFind:
				tmp=outquote.split(' ')
				if len(tmp) < 5:
					continue
				finished_str=''
				longer_str=''
				
				i=0
				for element in tmp: #if there is more than one, more than one quote was detected
					
					if i < 5:
						finished_str+=element+' '
					longer_str+=element+' '
					if i < 20:
						longer_str+=element+' '
					else:
						break
					
					i+=1
				final.append(finished_str)

			if len(final) == 0:
				print('No elements to move forward with, stopping.')
				print()
				continue
			
			for element in final:
				printf(element)

			
			#SEARCHING BOOKS
			print('Searching Books...')
			results=[]
			for searching_str in final:
			
				print('Starting new element')
			
				tmpresults=[]
			
				lower_searching=re.sub(r'[^A-Za-z0-9]','', str(searching_str))
				lower_searching_str=lower_searching.lower()
				
				print(lower_searching_str)

				match_found=False
				j=0
				for (book,chapter,arr) in activeDocuments:
					i=0
					for element in arr:
						if match_found:
							pass
						elif searching_str in element:

							element=element.strip()

							elem_before=''

							print('found type one')

							try:
								if i != 0:
									elem_before=arr[i-1].strip()+'     \n'
							except:
								print('LOWER ELEMENT NOT FOUND')

							elem_after=''

							try:
								elem_after='     \n'+arr[i+1].strip()
							except:
								print('UPPER ELEMENT NOT FOUND')

							if i == 0: # ok I changed my mind
								elem_before=element
								element=elem_after
								elem_after=arr[i+2].strip()
							elif len(elem_after)==0:
								elem_before=arr[i-2].strip()
								element=arr[i-1].strip()
								elem_after=arr[i].strip()

							tmpresults.append((searching_str,book,chapter,i,elem_before,element,elem_after))


							match_found=True
						elif lower_searching_str in full_arr[j]:
							
							element=element.strip()

							elem_before=''

							print('found type one')

							try:
								if i != 0:
									elem_before=arr[i-1].strip()+'     \n'
							except:
								print('LOWER ELEMENT NOT FOUND')

							elem_after=''

							try:
								elem_after='     \n'+arr[i+1].strip()
							except:
								print('UPPER ELEMENT NOT FOUND')

							if i == 0: # ok I changed my mind
								elem_before=element
								element=elem_after
								elem_after=arr[i+2].strip()
							elif len(elem_after)==0:
								elem_before=arr[i-2].strip()
								element=arr[i-1].strip()
								elem_after=arr[i].strip()

							tmpresults.append((searching_str,book,chapter,i,elem_before,element,elem_after))

							match_found=True
						i+=1
						j+=1
				if len(tmpresults) != 0:
					for elementa in tmpresults:
						results.append(elementa)
			
			for element in results:
				printf(element)
			
			print(len(results))
			
			#exports finished data to file
			if len(results) != 0:
				print('Exporting Data...')
			
			i=0
			fin_str=''
			
			for element_temporary in new_arr:
				if str(element_temporary.permalink[-6:]) == str(link_to_post[-6:]):
					reply_to_link=element_temporary
					break
			#just testing for now		
			for (quote,book,chapter,paragraph,elem_before,element,elem_after) in results:
				print('Just replied, hopefully')
				print(book)
				print(chapter)
				print(paragraph)
				if len(results) == 1:
					str_tmp=(
						'Quote starting with:\n\n>'+
						quote+
						'\n\nContext:\n\n'+
						'>Quote first found in '+str(titles[book-1][0])+
						' in Chapter '+str(chapter)+
						', approx. Page '+str(getPageNum((int(book),int(chapter),int(paragraph+1))))+
						'\n\nFull Context:\n\n['+
						elem_before+element+elem_after+
						'](/spoiler)\n\n***\n\n'+
						r'^^\[[code](https://github.com/joshuajolly/HPQuoteBot)\]\[[issues\\feedback](https://www.reddit.com/message/compose?to=anonymous853&subject=Issue%2FFeedback%20with%20HPQuoteBot&message=Issue%3A%0A%0ALink%20to%20post%20\(if%20applicable\)%3A)\]'
					)
					try:
						reply_to_link.reply(str_tmp)
						# pass
					except:
						reply_to_link.add_comment(str_tmp)
						# pass
				
				#don't want it clogging up the page! Simplified form
				else:
					if i==0:
						fin_str+=(
							'Quote starting with:\n\n>'+
							quote+
							'\n\nContext:\n\n'
							'>Quote found in '+str(titles[book-1][0])+
							' in Chapter '+str(chapter)+
							', approx. Page '+str(getPageNum((int(book),int(chapter),int(paragraph+1))))+
							'\n\n'+
							'***'+
							'\n\n'
						)
					else:
						fin_str+=(
							'Quote starting with:\n\n>'+
							quote+
							'\n\nContext:\n\n'
							'>Quote found in '+str(titles[book-1][0])+
							' in Chapter '+str(chapter)+
							', approx. Page '+str(getPageNum((int(book),int(chapter),int(paragraph+1))))+
							'\n\n'+
							'***'+
							'\n\n'
						)
					i+=1
				
			if len(results) != 0:
				if len(fin_str) != 0:
					fin_str += str(r'^^\[[code](https://github.com/joshuajolly/HPQuoteBot)\]\[[issues\\feedback](https://www.reddit.com/message/compose?to=anonymous853&subject=Issue%2FFeedback%20with%20HPQuoteBot&message=Issue%3A%0A%0ALink%20to%20post%20\(if%20applicable\)%3A)\]')
					try:
						# pass
						reply_to_link.reply(fin_str)
					except:
						# pass
						reply_to_link.add_comment(fin_str)
				f.close()
			else:
				print('Failed Exporting Data')
			
			print()
		
		print('Sleeping for 10 seconds')
		time.sleep(30)
	except Exception as e:
		time.sleep(30)
		print('Very serious error',e)