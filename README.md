execute crawler:
$ scrapy crawl gm -o test18.csv -t csv

The crawler accept some parameters for size and paging.
This parameters are:

dim1 = first size
dim2 = second size
dim3 = third size
paging = number of elements in search results pages

execute crawler with parameters:
$ scrapy crawl gm -a dim1=145 -a dim2=70 -a dim3=12 -a paging=50 -o test18.csv -t csv

where -o is output file and "-t csv" is file format.

References
http://doc.scrapy.org/en/latest/index.html
