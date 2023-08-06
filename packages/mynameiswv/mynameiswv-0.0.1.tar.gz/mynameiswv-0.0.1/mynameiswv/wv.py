class WV:
	"""
	Class wv is the record of wv.
	There are the details and youtube.

	Example
	# -------------------------
	wv = WV()
	wv.show_name()
	wv.show_youtube()
	wv.show_page()
	wv.about()
	wv.show_art()
	# -------------------------
	"""


	def __init__(self):
		self.name = 'WV'
		self.page = 'https://github.com/WasinV'

	def show_name(self):
		print('Hello {}'.format(self.name))

	def show_youtube(self):
		print('Youtube: https://www.youtube.com/')

	def show_page(self):
		print('Github Page: {}'.format(self.page))

	def about(self):
		text = """
		-------------------------------
		Hello I am WV. 
		I am the owner of this library.
		Nice to meet you.
		-------------------------------"""
		print(text)

	def show_art(self):
		text= """
		     ;;;;;;;;;;;;;;;;;;; 
		     ;;;;;;;;;;;;;;;;;;;
		     ;                 ;
		     ;                 ;
		     ;                 ;
		     ;                 ;
		     ;                 ;
		     ;                 ;
		     ;                 ;
		,;;;;;            ,;;;;;
		;;;;;;            ;;;;;;
		`;;;;'            `;;;;'
		"""
		print(text)

if __name__ == '__main__':
	wv = WV()
	wv.show_name()
	wv.show_youtube()
	wv.show_page()
	wv.about()
	wv.show_art()

