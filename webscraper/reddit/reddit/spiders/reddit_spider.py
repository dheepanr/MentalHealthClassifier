import scrapy
from bs4 import BeautifulSoup as bs
from uuid import uuid4
from reddit.items import RedditItem

class RedditSpider(scrapy.Spider):
	name = 'reddit'
	page_lim = 10
	page_num = 0

	def start_requests(self):
		urls = ['https://www.reddit.com/r/depression/', 'https://www.reddit.com/r/ptsd']

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = bs(response.body, 'html.parser')
		follow_urls = page.findAll('div',{'id':lambda x: x and x.startswith('thing')})	
		for url in follow_urls:
			url_name = url['data-url']
			follow_link = response.urljoin(url_name)
			yield scrapy.Request(follow_link, callback=self.post_parse)

		next_page =  page.find('span', {'class':'next-button'})
		if next_page and self.page_num < self.page_lim:
			next_link = response.urljoin(next_page.a['href'])
			self.page_num += 1
			yield scrapy.Request(next_link, callback=self.parse)

	def post_parse(self, response):
		item = RedditItem()
		page = bs(response.body, 'html.parser')
		comments = page.findAll('div', {'class':'entry unvoted'})

		item['url'] = response.url
		state = 0
		state_0_id = []
		for c_ix, c in enumerate(comments):

			comment_id = str(uuid4())
			item['comment_id'] = comment_id
			state_0_id.append(comment_id)

			comment_flag = c.find('a',{'data-event-action':'parent'})

			if comment_flag:
				item['reply_type'] = 'comment'
				state = 1
				item['conversation_resp'] = comment_flag['href']
				item['thread_starter'] = state_0_id[0]

			else:
				item['reply_type'] = 'reply'
				state = 0
				item['conversation_resp'] = None
				item['thread_starter'] = 'self'
				state_0_id = []

			author = c.find('a',{'class':lambda x: x and x.startswith('author')})
			if author:
				item['author'] = author.text
			else:
				item['author'] = None

			item['time'] =  c.find('time')['title'] 
			
			if c_ix == 0:
				likes = page.find('div',{'class':'score unvoted'}).text
				item['likes'] = int(likes[0])
			else:
				likes = c.find('span', {'class':'score unvoted'})
				if likes:
					item['likes'] = int(likes.text[0])

			title = c.find('p', {'class':'title'})
			if title:
				title_text = title.a.text
			else:
				title_text = ''

			comment = c.find('div', {'class':'md'})
			if comment:
				comment_text = comment.text.replace('\n','')
			else:
				comment_text = ''
			item['comment'] = title_text.join(comment_text)

			yield item








			