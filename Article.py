from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
import codecs
from newspaper import Article as NewspaperArticle
import urllib.request

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')

ps = PorterStemmer()

class Article:
    """Article class to parse and store contents of a single HTML file or URL

    Attributes:
        filePath: file path or URL
        title: title of the article
        rawLines: list of sentences, each item in the list is one sentence
    """
    def __init__(self, fileName):
        '''
        Parse the HTML document content to sentences or fetch article content from URL

        :param fileName: path of HTML file or URL to be parsed
        '''
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        
        # Handling URLs
        if fileName.startswith('http'):
            article = NewspaperArticle(fileName)
            article.download()
            article.parse()
            self.filePath = fileName
            self.title = article.title
            data = article.text
            self.rawLines = tokenizer.tokenize(data)

        # Handling HTML files
        elif fileName.endswith('.htm') or fileName.endswith('.html'):
            with open(fileName) as file:
                self.filePath = fileName
                html_doc = file.read()
                soup = BeautifulSoup(html_doc, "lxml")
                self.title = soup.title.string
        
                # Get contents from the HTML without section titles
                paragraphs = [paragraph.get_text() for paragraph in soup.find_all('p')]
                data = "\n".join(paragraphs)
                self.rawLines = tokenizer.tokenize(data)

        else:
            print('Error, unable to read file', fileName)

    def showRawLines(self):
        print('\n-----\n'.join(self.rawLines).encode('utf-8').strip())

    def getTitle(self):
        return self.title

    def getRawLines(self):
        return self.rawLines

    def getRawLines_stem(self):
        return [' '.join([ps.stem(word) for word in wordpunct_tokenize(sentence)]) for sentence in self.rawLines]


if __name__ == '__main__':
    article = Article("https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2023")
    print("=== Title ===\n", article.getTitle())
    article.showRawLines()
