from sys import *
import os.path

class ParseWiki():

	PAGE_ID_TITLE_SQL_FILE =  "frwiki-latest-page.sql.gz" # Original input file
	PAGE_ID_TITLE_RAW_FILE = "wikipedia-page-id-title.raw"
	PAGE_LINKS_SQL_FILE = "frwiki-latest-pagelinks.sql.gz"# Original input file
	PAGE_LINKS_RAW_FILE = "wikipedia-page-links.raw" # Cache after preprocessing
	INDEX_RAW_FILE = "wikipedia-linked.raw"
		
		
		
	# Cache after preprocessing
	# ---- Main program ----
	
	@staticmethod
	def main(args):
	
		titleToId = {}
		
		if not os.path.exists(ParseWiki.PAGE_ID_TITLE_RAW_FILE):
			titleToId = PageIdTitleMap.readSqlFile(ParseWiki.PAGE_ID_TITLE_SQL_FILE)
			PageIdTitleMap.writeRawFile(titleToId, ParseWiki.PAGE_ID_TITLE_RAW_FILE)
		else:
			titleToId = PageIdTitleMap.readRawFile(ParseWiki.PAGE_ID_TITLE_RAW_FILE)
		
		idToTitle = PageIdTitleMap.computeReverseMap(titleToId)
		
		#Read page-links data
		links=[]	
		if not os.path.exists(ParseWiki.PAGE_LINKS_RAW_FILE):  #Read SQL and write cache
			links = PageLinksList.readSqlFile(ParseWiki.PAGE_LINKS_SQL_FILE, titleToId, idToTitle);
			PageLinksList.writeRawFile(links, ParseWiki.PAGE_LINKS_RAW_FILE);
		else: #Read cache
			links = PageLinksList.readRawFile(ParseWiki.PAGE_LINKS_RAW_FILE);
		
		print("* Done indexing.");
		

	