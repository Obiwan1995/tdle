#
# Page Rank
# naive implementation by S. Genaud, 2016
# based on example
# from http://www.cs.cornell.edu/home/kleinber/networks-book/networks-book-ch14.pdf

# From matrix M reprensenting the web pages connexity, compute pagerank (PR) of each page.
# This is an iterative algorithm, the number k of iterations is to be set in the code.


npages = 8

# M(i,j)=1 <=> P_i has an outgoing link to P_j
# np.array(
M = [[0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 1, 0],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0]]
# )


# initially, page rank of each page is 1/npages
PR = [1.0 / npages] * npages
C = [0] * npages
recv = [0] * npages
d = 0.85
# number of iterations
k = 5

# compute number of outgoing links for page i
for i in range(npages):
    C[i] = sum(M[i])

print("PR=", PR)
print("C=", C)
for _ in range(k):
    # for each row
    for i in range(npages):
        # compute how much page i receives from other pages
        recv[i] = 0
        for j in range(npages):
            # if not myself (but M[i][i] should be 0) and there is an ingoing link from page j
            if (i != j) and (M[j][i] == 1):
                recv[i] += PR[j] / C[j]
            # print("+PR[",j,"]/C[",j,"]=",PR[j],"/",C[j],"=",recv[i])
            # print("recv[",i,"]=",recv[i])
    # now update PRs
    for i in range(npages):
        # PR[i]=recv[i]  # no damping  (All values sum to 1)
        PR[i] = (1 - d) + d * recv[i]  # damping
        print("PR_", i, "=", PR[i])

for i in range(npages):
    print("PR_", i, "=", PR[i])
