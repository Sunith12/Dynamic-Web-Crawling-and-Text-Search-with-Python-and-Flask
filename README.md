# Dynamic-Web-Crawling-and-Text-Search-with-Python-and-Flask

Naga Sunith Appasani - A20552681

1. Abstract
This project develops a web-based text search platform that crawls websites for documents, indexes them using TF-IDF and cosine similarity, and provides a query interface to search these indexed documents. The system employs a three-component architecture: a Scrapy crawler to download web pages, a Scikit-Learn indexer to create an inverted index, and a Flask server for query processing. Future enhancements might include integrating vector embeddings and neural search methods to enhance search relevance and accuracy.

2. Overview
The solution is built around a Python ecosystem, leveraging popular libraries such as Scrapy for crawling, Scikit-Learn for text processing and indexing, and Flask for serving web requests. The system is designed to be scalable and efficient, capable of processing and indexing large volumes of text data from web sources, and providing fast search responses.

3. Design
The system is capable of:
•	Dynamically crawling web pages up to a specified depth and page count.
•	Indexing the text content of web pages using TF-IDF scoring.
•	Responding to search queries with the most relevant documents, ranked by cosine similarity.
•	Optional enhancements like spelling correction and query expansion using WordNet.


4. Architecture
The architecture consists of three main components:
•	Crawler: Uses Scrapy with settings for auto-throttling to manage crawl rate and depth.
•	Indexer: Utilizes the TfidfVectorizer from Scikit-Learn to create and store an inverted index in pickle format.
•	Query Processor: A Flask application that handles HTTP requests, processes user queries, and returns search results in JSON format.

5. Operation
Commands and installations:
•	pip install scrapy flask scikit-learn nltk
•	To run the crawler: Navigate to the crawler directory and run scrapy crawl document_spider.
•	To build the index: Execute python build_index.py.
•	To start the Flask server: python app.py.

6. Conclusion
The system successfully meets the basic requirements of web crawling, indexing, and query processing. The simplicity of the Flask interface and the efficiency of the Scrapy and Scikit-Learn integration allow for effective text searching. However, handling large-scale data and complex queries may require further optimizations and use of advanced techniques like FAISS for faster similarity computations.

7. Data Sources
Data is dynamically sourced from web pages crawled by the Scrapy crawler, starting from a seed URL and extending up to a defined link depth and page count.

8. Test Cases
Manual Testing for post request just used postman. Tests cover:
•	Functionality of the crawler to fetch pages.
•	Accuracy of the TF-IDF indexing process.
•	Correctness of the query processing and response format.

9. Source Code
The complete source code is provided in Python files, including:
•	document_spider.py for the Scrapy crawler.
•	build_index.py for the indexer.
•	app.py for the Flask application.

10. References 
"Mining the Social Web, 3rd Edition" by Matthew A. Russell and Mikhail Klassen 
"Flask Web Development" by Miguel Grinberg
