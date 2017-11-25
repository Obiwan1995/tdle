import java.util.Arrays;
import java.util.stream.IntStream;

public class Pagerank {
    // Maximum id of pages + 1
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

    // A cell is set to true if the current page ID has incoming links
    private boolean[] hasIncomingLinks;

    private final double DAMPING = 0.85;

    public double[] getScores() {
        return scores;
    }

    public void setScores(double[] scores) {
        this.scores = scores;
    }

    // With all the links, find the highest page ID
    private int findHighId() {
        int maxId = 0;
        int i = 0;
        while (i < this.links.length) {
            // Target page id
            int dest = this.links[i];

            maxId = Math.max(dest, maxId);

            // Number of incoming links
            int numIncoming = this.links[i + 1];

            // Check if it has an id over the maxId
            for (int j = 0; j < numIncoming; j++) {
                //Source of an incoming link
                int src = this.links[i + 2 + j];
                maxId = Math.max(src, maxId);
            }
            // Next target page id
            i += numIncoming + 2;
        }
        return maxId;
    }

    // Set whether or not the target id has incoming links and set the number of outgoing links of an id.
    private void setIncAndNumber() {
        int i = 0;
        while (i < this.links.length) {
            // Target page id
            int dest = this.links[i];
            this.hasIncomingLinks[dest] = true;

            // Number of incoming links
            int numIncoming = this.links[i + 1];

            int finalI = i;
            IntStream.range(0, numIncoming).forEachOrdered(j -> this.numOutGoingLinks[this.links[finalI + 2 + j]]++);

            i += numIncoming + 2;
        }
    }


    // Initialize the score for all the pages
    private void initScore() {

        double initWeight = 1.0 / this.totalActive;

        IntStream.range(0, this.idLimit).filter(i -> this.isActive[i]).forEachOrdered(i -> this.scores[i] = initWeight);
    }

    // Set if the id is active and sum the total of active pages
    private void setActiveAndNumber() {
        IntStream.range(0, idLimit).filter(i -> this.numOutGoingLinks[i] > 0 || this.hasIncomingLinks[i]).forEachOrdered(i -> {
            this.isActive[i] = true;
            this.totalActive++;
        });
    }

    // ------------ Constructor

    // Constructs a PageRank calculator
    public Pagerank(int[] links) {
        // Set the links
        this.links = links;

        // Set the maximum size of array
        this.idLimit = findHighId() + 1;

        // Compute metadata fields
        // Array of bool where each index corresponds to a pageID.
        this.hasIncomingLinks = new boolean[idLimit];
        // Array of int where each index corresponds to a pageID
        this.numOutGoingLinks = new int[idLimit];

        setIncAndNumber();

        // Array of bool where each index corresponds to a pageID.
        this.isActive = new boolean[idLimit];
        // Set the total of active pages
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
        IntStream.range(0, this.idLimit).filter(i -> this.numOutGoingLinks[i] > 0).forEachOrdered(i -> this.scores[i] /= this.numOutGoingLinks[i]);
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
            // new score becomes the sum of past scores
            this.newScores[dest] = sumPastScore;
            i += numIncoming + 2;
        }
    }

    // Generate Bias for non active page
    private double generateBias() {
        double bias = IntStream.range(0, this.idLimit).filter(i -> this.isActive[i] && this.numOutGoingLinks[i] == 0).mapToDouble(i -> this.scores[i]).sum();
        bias /= this.totalActive;
        return bias;
    }

    // Compute scores (one iteration)
    public void computeScores() {
        divideByOutGoing();

        Arrays.fill(this.newScores, 0);

        setNewScore();

        double bias = generateBias();

        double temp = bias * this.DAMPING + (1 - this.DAMPING) / totalActive;

        IntStream.range(0, idLimit).filter(i -> isActive[i]).forEachOrdered(i -> scores[i] = newScores[i] * this.DAMPING + temp);
    }
}
