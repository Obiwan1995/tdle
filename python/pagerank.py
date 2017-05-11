# -*- coding: utf-8 -*-
# !/usr/bin/python3


"""
Pagerank object 

Different function to calcul a pagerank

"""


import numpy as np

class Pagerank:


    def __init__(self,pageLinks):
        self.pageLinks = pageLinks

    def calcul(self):
        self.pageLinksToInputLink()
        self.computeMatrix()
        self.computePageRank()


    def pageLinksToInputLink(self):
        """
          pageLinks is dictionary of pageIndex -> list of output pageIndex (lien sortant)
          InputLink (lien entrant)
         
        """
        inputDict = {}
        listLinks = []

        for key, list in self.pageLinks.items():
            for value in list:
                if(value in inputDict): # on ajoute à la liste la key
                    inputDict[value] = inputDict[value] + [key]
                else: # on créer une nouvelle list
                    inputDict[value] = [key]
                # Permet d'obtenir tout les liens inscrit (sortant ou entrant)
                if(not(value in listLinks)):
                    listLinks.append(value)
                if(not(key in listLinks)):
                    listLinks.append(key)


        self.inputLinksData = inputDict
        self.links = sorted(listLinks)
        self.computeMatrix()

    def computeMatrix(self):
        """
         M(i,j)=1 <=> P_i has an outgoing link to P_j 
        """
        M = np.zeros((len(self.links),len(self.links)))

        inl = self.inputLinksData

        i = 0
        for v1 in self.links :
            j = 0
            for v2 in self.links :
                if(v1!=v2 and v1 in inl):
                    M[j,i] = inl[v1].count(v2)
                j = j+1
            i = i+1

        self.matrix = M
    def computePageRank(self):
        npages  = len(self.links)

        # initially, page rank of each page is 1/npages
        PR = np.ones(npages)*(1/npages)
        C = np.zeros(npages)
        recv = np.zeros(npages)
        d = 0.85
        k = 5 # number of iteration
        # compute number of outgoing links for page i
        for i in range(npages):
            C[i] = sum(self.matrix[i])

        #print("PR=", PR)
        #print("C=", C)
        for _ in range(k):
            # for each row
            for i in range(npages):
                # compute how much page i receives from other pages
                recv[i] = 0
                for j in range(npages):
                    # if not myself (but M[i][i] should be 0) and there is an ingoing link from page j
                    if (i != j) and (self.matrix[j,i] == 1):
                        recv[i] += PR[j] / C[j]
                        # print("+PR[",j,"]/C[",j,"]=",PR[j],"/",C[j],"=",recv[i])
                        # print("recv[",i,"]=",recv[i])
            # now update PRs
            for i in range(npages):
                # PR[i]=recv[i]  # no damping  (All values sum to 1)
                PR[i] = (1 - d) + d * recv[i]  # damping
                # print("PR_", i, "=", PR[i])
        self.pageRankCalcul = PR

    @staticmethod
    def test():

        print("Test execute pagerank")
        pageLinks_test = {}
        pageLinks_test["lien1"] = ["lien2","lien3","lien6"]
        pageLinks_test["lien2"] = ["lien2","lien6"]
        pageLinks_test["lien3"] = ["lien2","lien2","lien5"]
        pageLinks_test["lien4"] = ["lien2"]
        pageLinks_test["lien5"] = ["lien2","lien6"]
        print(pageLinks_test)
        pagerank = Pagerank(pageLinks_test)
        pagerank.calcul()
        print(" All links \n",pagerank.links)
        print("Input dict\n",pagerank.inputLinksData, "\n")
        print(pagerank.matrix,"\n")
        for i in range(len(pagerank.links)):
            print(pagerank.links[i], "=", pagerank.pageRankCalcul[i])



if __name__ == '__main__':
    Pagerank.test()


