import java.util.Arrays;



final class Pagerank {
	
	private int idLimit;
	
	// Number of page IDs with incoming links or outgoing links
	private int totalActive;
	
	//List of page with links associated Target page ID
	private int[] links;

	// Indicates whether each page ID is active or not
	private boolean[] isActive;
	
	//Score
	private double[] scores;

	// The number of outgoing links each page ID has
	private int[] numOutGoingLinks;

	// Temporary array
	private double[] newScores;

	// Set if each page ID has incominglinks.
	private boolean[] hasIncomingLinks;

	private final double DAMPING = 0.85;

	public double[] getScores()
	{
		return scores;
	}

	public void setScores(double[] scores)
	{
		this.scores = scores;
	}
	
	// Wth all the links, find the highest page ID 
	private int findHighId ()
	{
		int maxId = 0;
		int i = 0;
		while (i < this.links.length)
		{
			// Target page id
			int dest = this.links[i];

			maxId = Math.max(dest, maxId);

			// Number of incoming links
			int numIncoming = this.links[i + 1];

			// Check if it has an id over the maxId
			for (int j = 0; j < numIncoming; j++)
			{
				//Source of an incoming link
				int src = this.links[i + 2 + j];
				maxId = Math.max(src, maxId);
			}
			// Next target page id
			i += numIncoming + 2;
		}
		return maxId;
	}

	// Set wheter or not if the target id has incoming links and set the number of outgoinglink of an id.
	private void setIncAndNumber()
	{
		int i = 0;
		while (i < this.links.length)
		{
			// Target page id
			int dest = this.links[i];
			this.hasIncomingLinks[dest] = true;

			// Number of incoming links
			int numIncoming = this.links[i + 1];

			// For each incoming links from the target page id
			// We set up the number of outgoingLinks
			for (int j = 0; j < numIncoming; j++)
			{
				// Incoming link
				int src = this.links[i + 2 + j];
				this.numOutGoingLinks[src]++;
			}
			i += numIncoming + 2;
		}
	}



	// Initialize the score for all the pages
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
	
	// ------------ Constructor
	
	// Constructs a PageRank calculator 
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
	
	
	// ------------ Methods

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
			// Target page id
			int dest = this.links[i];
			// numIncoming is the number of incoming links
			int numIncoming = this.links[i + 1];
			double sumPastScore = 0;
			for (int j = 0; j < numIncoming; j++)
			{
				// Source of an incoming link
				int src = this.links[i + 2 + j];
				// Adding the past scores
				sumPastScore += this.scores[src];
			}
			// new score became the sum of past scores
			this.newScores[dest] = sumPastScore;
			i += numIncoming + 2;
		}
	}

	// Generate Bias for non active page
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

	// Compute scores
	public void calculScore()
	{
		divideByOutGoing();
		
	
		Arrays.fill(this.newScores, 0);

		setNewScore();
		
		double bias = generateBias();
		
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
