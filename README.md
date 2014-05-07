There are two crawler in this scrapy project.
The first one is gm crawler for massive data import.
The second one is tinygm crawler for speed import. 

execute main crawler:
$ scrapy crawl gm -o test.csv -t csv

execute tiny crawler: 
$ scrapy crawl tinygm -o tiny_test.csv -t csv

Both crawlers accepts some parameters for size and paging.
This parameters are:

dim1 = first size
dim2 = second size
dim3 = third size
paging = number of elements in search results pages

execute main crawler with parameters:
$ scrapy crawl gm -a dim1=145 -a dim2=70 -a dim3=12 -a paging=50 -o test18.csv -t csv

execute tiny crawler with parameters:
$ scrapy crawl tiygm -a dim1=145 -a dim2=70 -a dim3=12 -a paging=50 -o test18.csv -t csv

where -o is output file and "-t csv" is file format.

References
http://doc.scrapy.org/en/latest/index.html
