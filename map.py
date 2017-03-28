# -*- coding: utf-8 -*-
# !/usr/bin/python3


import sys
from analyzer import *
from ignorecontent import *

# Global var
#Toggle var (boolean)
HEADER = True
CONTENT = False
SKIP_CONTENT = False
#other var
contentHtml = ""

# input comes from STDIN (standard input)
for line in sys.stdin:



    if HEADER and not SKIP_CONTENT:
        # Dans le HEADER :
        # TODO récupérer l'url du site
        # TODO skip si l'url est dans l'ignore extension list

        if Analyzer.isUrlLine(line) :
            #Url found
            url = Analyzer.extractUrl(line)
            if IgnoreContent.isIgnoreUrl(url) :
                #On rentre en mode skip
                SKIP_CONTENT = True

        # Phase de transition
        if Analyzer.isContentLine(line):

            HEADER = False
            contentHtml += line # En supposant qu'une content line est un <doctype ...>

    elif CONTENT and not SKIP_CONTENT:
        # Dans le CONTENT :
        if not Analyzer.isContentEnd(line): # TODO contentEnd peut être </html> du coup il faut rajouter à contentHtml dans le else
            #On ajoute les lignes pour le parseur  après
            contentHtml += line
        else:
            # TODO PARSE l'html

            # TODO send word and url

            # write the results to STDOUT (standard output);
            # what we output here will be the input for the
            # Reduce step, i.e. the input for reducer.py
            #
            # tab-delimited; the trivial word count is 1
            # print('%s\t%s' % (word, 1))

            CONTENT = False
            SKIP_CONTENT = False # à priori stupide
            HEADER = True
    else:
        # Dans le cas ou on est en mode SKIP_CONTENT
        if Analyzer.isContentEnd(line):
            #On revient à la normal en rentrant dans un HEADER
            CONTENT = False
            SKIP_CONTENT = False
            HEADER = True
