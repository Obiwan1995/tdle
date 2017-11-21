import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.GZIPInputStream;

/*
 *	-> 15 columns :
 *
CREATE TABLE `page` (
  `page_id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `page_namespace` int(11) NOT NULL DEFAULT '0',
  `page_title` varbinary(255) NOT NULL DEFAULT '',
  `page_restrictions` varbinary(255) NOT NULL DEFAULT '',
  `page_counter` bigint(20) unsigned NOT NULL DEFAULT '0',
  `page_is_redirect` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `page_is_new` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `page_random` double unsigned NOT NULL DEFAULT '0',
  `page_touched` varbinary(14) NOT NULL DEFAULT '',
  `page_links_updated` varbinary(14) DEFAULT NULL,
  `page_latest` int(8) unsigned NOT NULL DEFAULT '0',
  `page_len` int(8) unsigned NOT NULL DEFAULT '0',
  `page_no_title_convert` tinyint(1) NOT NULL DEFAULT '0',
  `page_content_model` varbinary(32) DEFAULT NULL,
  `page_lang` varbinary(35) DEFAULT NULL,
  PRIMARY KEY (`page_id`),
  UNIQUE KEY `name_title` (`page_namespace`,`page_title`),
  KEY `page_random` (`page_random`),
  KEY `page_len` (`page_len`),
  KEY `page_redirect_namespace_len` (`page_is_redirect`,`page_namespace`,`page_len`)
) ENGINE=InnoDB AUTO_INCREMENT=10762705 DEFAULT CHARSET=binary;
*/

/* 
 * Provides static functions for working with page ID/title data.
 */
final class PageIdTitleMap {
	private static final int PRINT_INTERVAL = 30;  // In milliseconds

	private PageIdTitleMap() {}  // Not instantiable

	/**
	 * Read a SQL file and returns a HashMap, which associates an article id to its title
	 * @param file File to read
	 * @return A HashMap, which associates an article id to its title
	 * @throws IOException If a problem occurred when reading the file
	 */
	public static HashMap<String, Integer> readSqlFile(File file) throws IOException {
		long startTime = System.currentTimeMillis();
		HashMap<String, Integer> titleToId = new HashMap<>();
		
		SqlReader in = new SqlReader(new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(file)), "UTF-8")), "page");
		long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;
		List<List<Object>> multipleRows = in.readInsertionTuples();
		try {
			while (multipleRows != null) {
				for (List<Object> tuple : multipleRows) {
					if (tuple.size() != 15) {
						throw new IllegalArgumentException("Incorrect number of columns");
					}
					Object namespace = tuple.get(1);
					Object id = tuple.get(0);
					Object title = tuple.get(2);

					if (!(namespace instanceof Integer)) {
						throw new IllegalArgumentException("Namespace must be integer");
					}
					if (!(id instanceof Integer)) {
						throw new IllegalArgumentException("ID must be integer");
					}
					if (!(title instanceof String)) {
						throw new IllegalArgumentException("Title must be string");
					}
					if ((int)namespace == 0) { // Filter out pages not in the main namespace
						if (titleToId.containsKey(title)) {
							throw new IllegalArgumentException("Duplicate page title");
						}
						titleToId.put((String) title, (Integer) id);
					}
				}

				if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL) {
					System.out.printf("\rParsing %s: %.3f million entries stored...", file.getName(), titleToId.size() / 1000000.0);
					lastPrint = System.currentTimeMillis();
				}

				multipleRows = in.readInsertionTuples();
			}
		} finally {
			in.close();
		}
		System.out.printf("\rParsing %s: %.3f million entries stored... Done (%.3f s)%n", file.getName(), titleToId.size() / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
		return titleToId;
	}

	/*
		File structure:
		title1
		id1
		title2
		id2
		...
	 */
	public static HashMap<String, Integer> readRawFile(File file) throws IOException {
		long startTime = System.currentTimeMillis();
		HashMap<String, Integer> titleToId = new HashMap<>();
		
		BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF-8"));
		long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;
		String line = in.readLine();
		int i = 0;
		while (line != null) {
			/*	If title is on the first line,
				Id is on the line after */
			titleToId.put(line, new Integer(in.readLine()));

			if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL) {
				System.out.printf("\rReading %s: %.3f million entries...", file.getName(), i / 1000000.0);
				lastPrint = System.currentTimeMillis();
			}
			line = in.readLine();
			i++;
		}
		System.out.printf("\rReading %s: %.3f million entries... Done (%.3f s)%n", file.getName(), titleToId.size() / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
		in.close();
		return titleToId;
	}
	
	
	public static void writeRawFile(Map<String,Integer> idByTitle, File file) throws IOException {
		long startTime = System.currentTimeMillis();
		PrintWriter out = new PrintWriter(new OutputStreamWriter(new BufferedOutputStream(new FileOutputStream(file), 128 * 1024), "UTF-8"));
		int i = 0;
		long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;
		for (String title : idByTitle.keySet()) {
			out.println(title);
			out.println(idByTitle.get(title));
			i++;

			if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL) {
				System.out.printf("\rWriting %s: %.3f million entries...", file.getName(), i / 1000000.0);
				lastPrint = System.currentTimeMillis();
			}
		}
		System.out.printf("\rWriting %s: %.3f million entries... Done (%.3f s)%n", file.getName(), i / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
		out.close();
	}

	public static HashMap<Integer, String> computeReverseMap(HashMap<String, Integer> titleToId)
	{
		System.out.printf("\rComputing reverse map...");
		long startTime = System.currentTimeMillis();
		HashMap<Integer, String> idToTitle = new HashMap<>();
		for (Map.Entry<String, Integer> entry : titleToId.entrySet()) {
			String key = entry.getKey();
			Integer value = entry.getValue();
			idToTitle.put(value, key);
		}
		System.out.printf("\rComputing reverse map... Done (%.3f s)%n", (System.currentTimeMillis() - startTime) / 1000.0);
		return idToTitle;
	}
}
