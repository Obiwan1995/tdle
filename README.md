# TDLE

Project for the TDLE class in ENSIIE.
This project should use elasticsearch, hadoop and map-reduce

### Useful links
- Pagelinks: https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pagelinks.sql.gz (132,958,214 links total as of 21st October)
- Pages: https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-page.sql.gz (3,392,075 pages total as of 21st October)
- Article (might change): https://pdfs.semanticscholar.org/c982/d2ca924aab410cc0e74fb48b97f1e6927b5d.pdf

### Elastic Search

Download it here: https://www.elastic.co/downloads/elasticsearch    

Then, use `ParsePageRank.java` to parse the pagerank file into JSON format, which is needed to insert data into ElasticSearch.

To be able to insert everything at once, you need to increase the http request size in the `file config/elasticsearch.yml`:
```http.max_content_length: 500mb```

You also need to increase the ElasticSearch heap size in the file `config/jvm.options`:
```
-Xms4G
-Xmx4G
```

Finally, type the following command in a shell:    
```curl -s -XPOST localhost:9200/_bulk --data-binary "@pagerank.json"```  
It may take a while so be patient. At the end, a lot of prints will be displayed in the shell.
