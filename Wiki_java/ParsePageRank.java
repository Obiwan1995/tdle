import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.FileWriter;

import org.json.simple.JSONObject;

public final class ParsePageRank
{
	private static final File PAGERANK_INPUT_FILE = new File("page-titles-sorted.txt");
	private static final File PAGERANK_JSON_FILE = new File("pagerank.json");

	private static final int PRINT_INTERVAL = 30;  // In milliseconds

	public static void main (String[] args) throws IOException
	{
		long startTime = System.currentTimeMillis();
		BufferedReader in0 = new BufferedReader(new InputStreamReader(new FileInputStream(PAGERANK_INPUT_FILE), "UTF-8"));
		FileWriter out = new FileWriter(PAGERANK_JSON_FILE);
		int nb = 0;
		try {
			long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;
			while (true) {
				String line = in0.readLine();
				if (line == null)
					break;
				String[] split = line.split("\t");
				double score = Double.parseDouble(split[0].replace(",","."));
				String title = split[1].replace("_", " ");
				nb++;

				JSONObject index = new JSONObject();
				JSONObject index1 = new JSONObject();
				index1.put("_index", "tdle");
				index1.put("_type", "article");
				index1.put("_id", String.valueOf(nb));
				index.put("index", index1);
				JSONObject obj = new JSONObject();
				obj.put("title", title);
				obj.put("score", score);
				
				out.write(index.toJSONString());
				out.write("\n");
				out.write(obj.toJSONString());
				out.write("\n");

				if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL) {
					System.out.printf("\rWriting %s: %.3f million entries...", "pagerank.json", nb / 1000000.0);
					lastPrint = System.currentTimeMillis();
				}
			}
			System.out.printf("\rWriting %s: %.3f million entries... Done (%.3f s)%n", "pagerank.json", nb / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
		} finally {
			in0.close();
			out.close();
		}
	}
}
