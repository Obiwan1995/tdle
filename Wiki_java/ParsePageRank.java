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
	private static final File PAGERANK_INPUT_FILE = new File("sorted-pagerank.txt");
	private static final File PAGERANK_JSON_FILE = new File("pagerank.json");

	private static final int PRINT_INTERVAL = 30;  // In milliseconds

	public static void main (String[] args)
	{
		long startTime = System.currentTimeMillis();
		BufferedReader in = null;
		FileWriter out = null;
		int nb = 0;
		try
		{
			in = new BufferedReader(new InputStreamReader(new FileInputStream(PAGERANK_INPUT_FILE), "UTF-8"));
			out = new FileWriter(PAGERANK_JSON_FILE);

			long lastPrint = System.currentTimeMillis() - PRINT_INTERVAL;
			String line = in.readLine();

			while (line != null)
			{
				String[] split = line.split("\t");
				String title = split[0].trim().replace("_", " ");
				double score = Double.parseDouble(split[1].trim());
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

				if (System.currentTimeMillis() - lastPrint >= PRINT_INTERVAL)
				{
					System.out.printf("\rWriting %s: %.3f million entries...", PAGERANK_JSON_FILE.getName(), nb / 1000000.0);
					lastPrint = System.currentTimeMillis();
				}
				line = in.readLine();
			}
			System.out.printf("\rWriting %s: %.3f million entries... Done (%.3f s)%n", PAGERANK_JSON_FILE.getName(), nb / 1000000.0, (System.currentTimeMillis() - startTime) / 1000.0);
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		finally
		{
			try
			{
				if (in != null)
				{
					in.close();
				}
				if (out != null)
				{
					out.close();
				}
			}
			catch (IOException e)
			{
				e.printStackTrace();
			}
		}
	}
}
