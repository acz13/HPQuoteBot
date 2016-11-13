'''
                                  //|             //|
                                 // |            // |
                                //  //////////////  |
                               //  //////////////   |
          _        _          //  //////////////    |
         //|      //|        //  //////////////     |
        // //////// |       //  //////////////      |
       // ////////  |      //  //////////////       |
      // ////////   |     //  //////////////        |
     // ////////    |_   //  //////////////         |
    // ////////     //| //  //////////////          |
   // ////////     // //|===============|           |
  // ////////     // ///|***************|           |
 // ////////     // ////|===============|           |
// ////////     // /////|***************|           |
|********|     // //////|***************|           |
|********|    // ///////|===============|           |
|   A    |   // ////////|               |           |
|History |  // /////////|      The      |           |
|  Of    | // //////////|  LIFE & LIES  |           |
| Magic  |// ///////////|      of       |           |
|********||------------||     Albus     |           |
|********||------------||  Dumbledore   |           |
|        ||  Secrets   ||               |           |
|        ||    Of      ||               |          /|
|        ||    The     ||***************|         //|
|  `'`   ||  Darkest   ||     From      |        // |
| `,*,`  ||   Arts     ||  Bestselling  |       //  |
| ; |;   ||------------||    Author     |      //   |
|   |    ||------------||***************|     //    |
|   |    ||            ||*RITA SKEETER *|    //     |
|   |    ||            ||***************|   //     /
|   |    ||            ||  *   *   *   *|  //     /
|   |    ||            ||*   *   *   *  | //     /
|        ||            ||  *   *   *   *|//     /
|        ||            ||*   *   *   *  |/     /
|        ||            ||  *   *   *   *|     /
|********||            ||---------------|    /
|Bathilda||------------||***************|   /
|Bagshot ||   Owle     ||---------------|  /
|********||  Bullock   ||***************| /
|________||____________||_______________|/
'''


#IMPORTS
import re
from bs4 import BeautifulSoup
import time
import threading
import codecs
import os

#LOADING TO DISK
titles=[]

titles.append(('Harry Potter and the Sorcerer\'s Stone (US)',17)) #book name,number of chapters
titles.append(('Harry Potter and the Chamber of Secrets (US)',18))
titles.append(('Harry Potter and the Prisoner of Azkaban (US)',22))
titles.append(('Harry Potter and the Goblet of Fire (US)',37))
titles.append(('Harry Potter and the Order of the Phoenix (US)',38))
titles.append(('Harry Potter and the Half-Blood Prince (US)',30))
titles.append(('Harry Potter and the Deathly Hallows (US)',37))

titles.append(('Harry Potter and the Philosopher\'s Stone (UK)',17)) #book name,number of chapters
titles.append(('Harry Potter and the Chamber of Secrets (UK)',18))
titles.append(('Harry Potter and the Prisoner of Azkaban (UK)',22))
titles.append(('Harry Potter and the Goblet of Fire (UK)',37))
titles.append(('Harry Potter and the Order of the Phoenix (UK)',38))
titles.append(('Harry Potter and the Half-Blood Prince (UK)',30))
titles.append(('Harry Potter and the Deathly Hallows (UK)',37))

titles.append(('Fantastic Beasts and Where to Find Them',1))

short_titles=[]

short_titles.append('HP & the SS (US)')
short_titles.append('HP & the CoS (US)')
short_titles.append('HP & the PoA (US)')
short_titles.append('HP & the GoF (US)')
short_titles.append('HP & the OotP (US)')
short_titles.append('HP & the HBP (US)')
short_titles.append('HP & the DH (US)')

short_titles.append('HP & the PS (UK)')
short_titles.append('HP & the CoS (UK)')
short_titles.append('HP & the PoA (UK)')
short_titles.append('HP & the GoF (UK)')
short_titles.append('HP & the OotP (UK)')
short_titles.append('HP & the HBP (UK)')
short_titles.append('HP & the DH (UK)')

short_titles.append('Fantastic Beasts and Where to Find Them')


chapterdata=[]
link=os.getcwd()+'//data'

#load chapterdata to array
i=1
for folders in titles:
	f=open(link+'//chapterdata//'+str(i)+'//pagenumbers.txt','r')
	chapterdata.append(f.readlines())
	f.close()
	i+=1

#take paragraph number and return percentage
def getPageNum(tuple):
	# book,chapter,paragraph
	book_number=tuple[0]
	chapter_number=tuple[1]
	paragraph_number=float(tuple[2]-1)
	
	pages_in_chapter=int(chapterdata[book_number-1][chapter_number])-int(chapterdata[book_number-1][chapter_number-1])
	print(pages_in_chapter)
	
	starting_page=int(chapterdata[book_number-1][chapter_number-1])
	print(starting_page)
	
	chars_before = len(' '.join(activeDocuments[book_number-1][2][:int(paragraph_number)])) # takes elements before paragraph number. 0 indexed.

	max_paragraph_number=(len(activeDocuments[book_number-1][2]))
	max_chars= len(' '.join(activeDocuments[book_number-1][2]))
	print('max_chars just before this')

	#position=paragraph_number/max_paragraph_number
	position=chars_before/max_chars

	print(position)
	
	return (int(position * pages_in_chapter) + starting_page)#percent through the chapter we are
	
j=1
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
	j+=1
	
print('Finished Loading.')

#printing utf-8 to console risk-free
def printf(u):
	print(re.sub(r'[^\x00-\x7F]',' ', str(u)))

#target subreddit
sub_name='harrypotter'

delay_between = 30

main_running_var=0 #number of iterations done thus far

while(True):
	try:
		if main_running_var == 0:
			print('Beginning first iteration.')
			import praw 
			
			r=praw.Reddit(user_agent="HPQUOTE/0.1 by anonymous853")

			r.login('[]','[]',disable_warning=True)
			try:
				threads=r.get_subreddit(sub_name).get_comments(limit=1)
			except Exception as e:
				print('Error,',e)
			
			for submission in threads:
				f=open('time.txt','w+')
				f.write(str(submission.created_utc))
				f.close()
		#necessary for re-logging in, in case of expiration
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
		
		'''
		the intent of breaking this into two iterations (for submission in threads and for
			submission in out is to check OP's and responses independently
		'''

		for submission in threads:
			if submission.is_self == True:
				if str(submission.author) != 'hpquotebot':
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

			ignore_length = False
			continue_stopping = False

			if '+nobot' in htmlpoint:
				continue_stopping = True
			elif '+bot' in htmlpoint:
				ignore_length = True

			if continue_stopping == True:
				continue

			outFind=[]
			for element in soup.findAll('div'):
				for line in soup.findAll('blockquote'):
					duplicate = False
					for parts in outFind:
						if line.text[1:] in parts:
							duplicate = True
					if duplicate == False:
						outFind.append(line.text)
			if len(outFind)==0:
				print('Did not find Quote, stopping.')
				print()
				continue
			else:
				print('Found Quote, Continuing.')

			final=[] #has simplified quote for searching with
			for outquote in outFind:
				print('starting function')
				tmp=outquote.split(' ')
				if len(tmp) < 6:
					if ignore_length == False:
						print('Continuing')
						continue
						
				finished_str=''
				
				i=0
				for element in tmp: #if there is more than one, more than one quote was detected
					finished_str+=element+' '

					if i > 20:
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
							elem_before = ''
							if i != 0:
								try:
									elem_before=arr[i-1].strip()
								except:
									pass

							real_element=element.strip()

							elem_after = ''
							try:
								elem_after=arr[i+1].strip()
							except:
								pass

							tmpresults.append((searching_str,book,chapter,i,elem_before,real_element,elem_after))
							
							match_found=True

						elif lower_searching_str in full_arr[j]:
							elem_before = ''
							if i != 0:
								try:
									elem_before=arr[i-1].strip()
								except:
									pass

							real_element=element.strip()

							elem_after = ''
							try:
								elem_after=arr[i+1].strip()
							except:
								pass

							tmpresults.append((searching_str,book,chapter,i,elem_before,real_element,elem_after))

							match_found=True
						i+=1
						j+=1
				if len(tmpresults) != 0:
					for elementa in tmpresults:
						results.append(elementa)
			
			for element in results:
				printf(element)
			
			print(len(results))
			
			if len(results) != 0:
				print('Exporting Data...')
			
			i=0
			fin_str=''
			
			#I honestly no idea what this does. Thanks, past me.
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

				out_message = '***\n\n[Happy Holidays!](http://i.imgur.com/xC38gcG.jpg)' + '\n\n' + r'^^\[[code](https://github.com/joshuajolly/HPQuoteBot)\]\[[issues\\feedback](https://www.reddit.com/message/compose?to=anonymous853&subject=Issue%2FFeedback%20with%20HPQuoteBot&message=Issue%3A%0A%0ALink%20to%20post%20\(if%20applicable\)%3A)\]'

				if len(results) == 1:
					str_tmp=(
						'Quote starting with:\n\n>'+quote+
						'\n\nQuote found in '+str(titles[book-1][0])+
						', Chapter '+str(chapter)+
						', Page '+str(getPageNum((int(book),int(chapter),int(paragraph+1))))+
						'\n\n***\n\n['
					)

					if len(elem_before) > 1:
						str_tmp += elem_before+'    \n'

					str_tmp += element+'     \n'

					if len(elem_after) > 1:
						str_tmp += elem_after+'    \n'
					str_tmp += '](/spoiler)\n\n' + out_message
					
					try:
						reply_to_link.reply(str_tmp)
					except:
						reply_to_link.add_comment(str_tmp)
				
				#don't want it clogging up the page! Simplified form
				else:
					if i == 0:
						fin_str+='|Phrase Quote Begins with|Book|Chapter|Page|\n|:--|:--:|:--:|:--:|\n';
					fin_str+=(
						'|'+' '.join(quote.split(' ')[:5]).strip()+
						'|'+str(short_titles[book-1]).strip()+
						'|'+str(chapter).strip()+
						'|'+str(getPageNum((int(book),int(chapter),int(paragraph+1)))).strip()+
						'|\n'
					)
					i+=1
				
			if len(results) != 0:
				if len(fin_str) != 0:
					fin_str += out_message
					try:
						reply_to_link.reply(fin_str)
					except:
						reply_to_link.add_comment(fin_str)
				f.close()
			else:
				print('Failed Exporting Data')
			
			print()
		
		print('Sleeping for 30 seconds')
		time.sleep(delay_between)
	except Exception as e:
		time.sleep(30)
		print('Very serious error',e)