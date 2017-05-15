/* 
 *
 * Parse 
 * <lang>wiki-<date>-page.sql.gz
 * <lang>wiki-<date>-page-links.sql.gz
 * to produce simplified files with page ids and links
 * 
 * Extracted from the original code :
 *
 *
 * Copyright (c) 2016 Project Nayuki
 * All rights reserved. Contact Nayuki for licensing.
 * https://www.nayuki.io/page/computing-wikipedias-internal-pageranks
 */

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.Arrays;
import java.util.Map;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.Writer;


/* 
 * This program reads the .sql.gz files containing Wikipedia's page metadata and page links
 * (or reads the cache files), writes out cached versions of the parsed data (for faster processing
 * next time), iteratively computes the PageRank of every page, and writes out the raw PageRank vector.
 * 
 * Run the program on the command line with no arguments. You may need to modify the file names below.
 * The program prints a bunch of statistics and progress messages on standard output.
 */

public final class ParseWiki {
	private static final int PRINT_INTERVAL = 30;
	
	/*---- Input/output files configuration ----*/
	
	private static final File PAGE_ID_TITLE_SQL_FILE = new File("frwiki-latest-page.sql.gz");           // Original input file
	private static final File PAGE_ID_TITLE_RAW_FILE = new File("wikipedia-page-id-title.raw");  // Cache after preprocessing
	
	private static final File PAGE_LINKS_SQL_FILE = new File("frwiki-latest-pagelinks.sql.gz");   // Original input file
	private static final File PAGE_LINKS_RAW_FILE = new File("wikipedia-page-links.raw");  // Cache after preprocessing
	
	private static final File INDEX_RAW_FILE = new File("wikipedia-linked.raw");  // Output file
	
	
	/*---- Main program ----*/
	
	public static void main(String[] args) throws IOException {
		// Read page-ID-title data
		Map<String,Integer> titleToId;
		if (!PAGE_ID_TITLE_RAW_FILE.isFile())
		{  // Read SQL and write cache
			titleToId = PageIdTitleMap.readSqlFile(PAGE_ID_TITLE_SQL_FILE);
			PageIdTitleMap.writeRawFile(titleToId, PAGE_ID_TITLE_RAW_FILE);
		}
		else  // Read cache
		{
			titleToId = PageIdTitleMap.readRawFile(PAGE_ID_TITLE_RAW_FILE);
		}
		Map<Integer,String> idToTitle = PageIdTitleMap.computeReverseMap(titleToId);
		
		// Read page-links data
		int[] links;
		if (!PAGE_LINKS_RAW_FILE.isFile())
		{  // Read SQL and write cache
			links = PageLinksList.readSqlFile(PAGE_LINKS_SQL_FILE, titleToId, idToTitle);
			PageLinksList.writeRawFile(links, PAGE_LINKS_RAW_FILE);
		}
		else  // Read cache
		{
			links = PageLinksList.readRawFile(PAGE_LINKS_RAW_FILE);
		}

		System.out.println("Done indexing.");

		System.out.println("Computing PageRank...");

		Pagerank pagerank = new Pagerank(links);

		long lastTimeMillis;

		// We iterate 200 times (enough to converge)
		for (int i = 0; i < 200; i++)
		{
			System.out.print("Iteration " + (i+1));
			lastTimeMillis = System.currentTimeMillis();
			pagerank.calculScore();

			System.out.printf(" (%.3f s)%n", (System.currentTimeMillis() - lastTimeMillis) / 1000.0);
		}

		Writer output = null;
		long startTime = System.currentTimeMillis();
		//on met try si jamais il y a une exception
		try
		{
			output = new BufferedWriter(new FileWriter("pagerank.txt"));

			long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;

			double[] scores = pagerank.getScores();
			int j = 0;
			for (int i = 0; i < scores.length; i++)
			{
				String title = idToTitle.get(i);
				if (title != null)
				{
					DecimalFormat format = new DecimalFormat("0.000");
					j++;
					double score = (double) Math.round((1 + (10 / Math.abs(Math.log10(scores[i])))) * 1000) / 1000;
					output.write(idToTitle.get(i) + " - " + format.format(score) + "\n");
				}

				if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL)
				{
					System.out.printf("\rWriting %s: %.3f of %.3f million pages...", "pagerank.txt", j / 1000000.0, idToTitle.size() / 1000000.0);
					lastPrint = System.currentTimeMillis();
				}
			}
			System.out.printf("\rWriting %s: %.3f of %.3f million pages... Done (%.3f s)%n", "pagerank.txt", j / 1000000.0, idToTitle.size() / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
			output.flush();
		}
		catch(IOException ioe)
		{
			System.out.print("Erreur : ");
			ioe.printStackTrace();
		}
		finally
		{
			if (output != null)
			{
				output.close();
			}
		}

	}
		
}
