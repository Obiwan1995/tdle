import java.util.Arrays;


/* 
 * Calculates the pagerank
 */
final class Pagerank {
	
	/*---- Fields ----*/

	//Store the score of the pagerank
	private double[] scores;
	
	//List of page with links associated
	// target page ID, number of incoming links, source page IDs.
	private int[] links;
	
	// Maximum page ID value plus 1. This sets the length of various arrays.
	private int idLimit;
	
	// Number of page IDs with incoming links or outgoing links (ignores disconnected nodes).
	private int totalActive;
	
	// Indicates whether each page ID is active or not. Length equals idLimit.
	private boolean[] isActive;
	
	// The number of outgoing links each page ID has. Length equals idLimit.
	private int[] numOutGoingLinks;

	// Indicates whether each page ID has incominglinks. Length equals idLimit.
	private boolean[] hasIncomingLinks;
	
	// Temporary array, which is filled and discarded per iteration. Length equals idLimit.
	private double[] newScores;

	// Applied damping at each iteration of the pagerank
	private final double DAMPING = 0.85;

	public double[] getScores()
	{
		return scores;
	}

	public void setScores(double[] scores)
	{
		this.scores = scores;
	}
	
	// Find the highest page ID among all links
	private int findHighId ()
	{
		int maxId = 0;
		int i = 0;
		while (i < this.links.length)
		{
			// dest is the target page id
			int dest = this.links[i];
			// Compare the current id to the max
			maxId = Math.max(dest, maxId);
			// numIncoming is the number of incoming links
			int numIncoming = this.links[i + 1];
			// For each incoming links from the target page id
			// We check if it has an id over the maxId
			for (int j = 0; j < numIncoming; j++)
			{
				//The source of an incoming link
				int src = this.links[i + 2 + j];
				maxId = Math.max(src, maxId);
			}
			// Next target page id
			i += numIncoming + 2;
		}
		return maxId;
	}

	// Set if the target id has incoming links and set the number of outgoinglink of an id.
	private void setIncAndNumber()
	{
		int i = 0;
		while (i < this.links.length)
		{
			// dest is the target page id
			int dest = this.links[i];
			this.hasIncomingLinks[dest] = true;
			// numIncoming is the number of incoming links
			int numIncoming = this.links[i + 1];
			// For each incoming links from the target page id
			// We set up the number of outgoingLinks
			for (int j = 0; j < numIncoming; j++)
			{
				// The source of an incoming link
				int src = this.links[i + 2 + j];
				this.numOutGoingLinks[src]++;
			}
			i += numIncoming + 2;
		}
	}

	// Set if the id is active and sum the total of active page
	private void setActiveAndNumber()
	{
		for (int i = 0; i < idLimit; i++)
		{
			if (this.numOutGoingLinks[i] > 0 || this.hasIncomingLinks[i])
			{
				this.isActive[i] = true;
				this.totalActive++;
			}
		}
	}

	// Initialize the score of each page
	private void initScore()
	{

		double initWeight = 1.0 / this.totalActive;

		for (int i = 0; i < this.idLimit; i++)
		{
			if (this.isActive[i])
			{
				this.scores[i] = initWeight;
			}
		}
	}
	
	/*---- Constructor ----*/
	
	// Constructs a PageRank calculator based on the given array of links
	// in the compressed format returned by class PageLinksList.
	public Pagerank(int[] links)
	{
		// Set the links
		this.links = links;
		
		// Set the maximum size of array
		this.idLimit = findHighId() + 1;
		
		// Compute metadata fields
		// Array of bool with each indice correspond to a pageID.
		this.hasIncomingLinks = new boolean[idLimit];
		// Array of int with each indice correspond to a pageID
		this.numOutGoingLinks = new int[idLimit];

		setIncAndNumber();

		// Array of bool with each indice correspond to a pageID.
		this.isActive = new boolean[idLimit];
		// Set the total of page active
		this.totalActive = 0;

		setActiveAndNumber();

		
		// Initialize PageRanks uniformly for active pages
		this.scores = new double[idLimit];
		initScore();

		this.newScores = new double[idLimit];
	}
	
	
	/*---- Methods ----*/

	// Divide the score by the number of outgoing links
	private void divideByOutGoing()
	{

		for (int i = 0; i < this.idLimit; i++)
		{
			if (this.numOutGoingLinks[i] > 0)
			{
				this.scores[i] /= this.numOutGoingLinks[i];
			}
		}
	}
	// Set new scores based on the sum of incoming links scores
	private void setNewScore()
	{
		int i = 0;
		while (i < this.links.length)
		{
			// dest is the target page id
			int dest = this.links[i];
			// numIncoming is the number of incoming links
			int numIncoming = this.links[i + 1];
			double sumPastScore = 0;
			for (int j = 0; j < numIncoming; j++)
			{
				// The source of an incoming link
				int src = this.links[i + 2 + j];
				// Adding the past scores
				sumPastScore += this.scores[src];
			}
			// new score became the sum of past scores
			this.newScores[dest] = sumPastScore;
			i += numIncoming + 2;
		}
	}

	// Generate Bias to compensate non active page
	private double generateBias()
	{
		double bias = 0;
		for (int i = 0; i < this.idLimit; i++)
		{
			if (this.isActive[i] && this.numOutGoingLinks[i] == 0)
			{
				bias += this.scores[i];
			}
		}
		bias /= this.totalActive;
		return bias;
	}

	// Performs one iteration of the PageRank algorithm and updates the values in the array 'scores'.
	public void calculScore()
	{
		// Pre-divide by number of outgoing links
		divideByOutGoing();
		
		// Distribute PageRanks over links (main calculation)
		Arrays.fill(this.newScores, 0);

		setNewScore();
		
		// Calculate global bias due to pages without outgoing links
		double bias = generateBias();
		
		// Apply bias and damping to all active pages
		double temp = bias * this.DAMPING + (1 - this.DAMPING) / totalActive;

		for (int i = 0; i < idLimit; i++)
		{
			if (isActive[i])
			{
				scores[i] = newScores[i] * this.DAMPING + temp;
			}
		}
	}
}
