import os.path
from page_id_title_map import PageIdTitleMap
from page_links_list import PageLinksList
import sys
from pathlib import Path # if you haven't already done so
root = str(Path(__file__).resolve().parents[1])

sys.path.append(root)

class ParseWiki:
    PAGE_ID_TITLE_SQL_FILE = "frwiki-latest-page.sql.gz"  # Original input file
    PAGE_ID_TITLE_RAW_FILE = "wikipedia-page-id-title.raw"
    PAGE_LINKS_SQL_FILE = "frwiki-latest-pagelinks.sql.gz"  # Original input file
    PAGE_LINKS_RAW_FILE = "wikipedia-page-links.raw"  # Cache after preprocessing
    INDEX_RAW_FILE = "wikipedia-linked.raw"

    # Cache after preprocessing
    # ---- Main program ----

    @staticmethod
    def main():
        # def main(args):

        if not os.path.exists(ParseWiki.PAGE_ID_TITLE_RAW_FILE):
            title_to_id = PageIdTitleMap.read_sql_file(ParseWiki.PAGE_ID_TITLE_SQL_FILE)
            PageIdTitleMap.write_raw_file(title_to_id, ParseWiki.PAGE_ID_TITLE_RAW_FILE)
        else:
            title_to_id = PageIdTitleMap.read_raw_file(ParseWiki.PAGE_ID_TITLE_RAW_FILE)

        id_to_title = PageIdTitleMap.compute_reverse_map(title_to_id)

        # Read page-links data
        if not os.path.exists(ParseWiki.PAGE_LINKS_RAW_FILE):  # Read SQL and write cache
            links = PageLinksList.read_sql_file(ParseWiki.PAGE_LINKS_SQL_FILE, title_to_id, id_to_title)
            PageLinksList.write_raw_file(links, ParseWiki.PAGE_LINKS_RAW_FILE)
        else:  # Read cache
            links = PageLinksList.read_raw_file(ParseWiki.PAGE_LINKS_RAW_FILE)

        print("* Done indexing.")


if __name__ == '__main__':
    ParseWiki.main()
