
import requests
import pycountry

from bs4 import BeautifulSoup

cb = codebook = {
    1 : "(Not set)",
    2 : "(Guess) ",
    3 : '(Failure)',
    4 : '(Translated) '
}

class Proto_eye():
    """
    Default eye of argus.
    """

    def __init__(self, url = cb[1], newspaper = cb[1], country = cb[1], language = cb[1], notes = cb[1]):
        self.url = url
        self.newspaper = newspaper
        self.country = country
        self.language = language
        self.notes = notes
        self.soup = cb[1]
        self.name = cb[2]

    def infer_data(self):
        """
        Use the url to infer newspaper name as well as country of origin
        """
        if self.newspaper == cb[1]:
            self.newspaper = cb[2] +  self.url.split(sep = '.')[-2]
        if self.country == cb[1]:
            domain = self.url.split(sep = '.')[-1][:-1] 
            try:
                country = pycountry.countries.get(alpha_2=domain).name
                self.country = cb[2]  + country
            except:
                self.country = cb[3]

    def describe(self):

        d = {
            'url' : self.url,
            'newspaper' : self.newspaper,
            'country' : self.country,
            'language': self.language,
            'notes' : self.notes,

        }
        return d

    
    def format_string(self, string):
        split = string.split()
        join = ' '.join(split)
        return join

    def watch(self):
        """
        Get the soup from the url and attempt to extract header and excerpt, returning them as a json object
        """
        self.soup = self.get_soup()

        response = {
            'header' : "Not Found",
            'excerpt' : "Not Found"
        }

        try:
            response['header'] = self.format_string(self.get_header())
            #logging.info(f"Extracted {response['header']}")
        except Exception as e:
            logging.warn(f"FAIL: getting header {e}")
        try:
            response['excerpt'] = self.format_string(self.get_excerpt())
            #logging.info(f"Extracted {response['excerpt']}")
        except Exception as e:
            logging.warn(f"FAIL: getting excerpt {e}")

        return response


    def get_soup(self):
        soup = cb[1]
        try:
            html = requests.get(self.url)
            soup = BeautifulSoup(html.content)
        except Exception as e:
            logging.warn(f"FAIL: {e}")
       
        return soup

    def get_header(self):
         for head in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header = self.soup.find(head)
            if header != None: 
                return cb[2] +  header.text

    def get_excerpt(self):
        excerpt = "Not found"
        for head in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header = self.soup.find(head)
            if header != None:
                excerpt = header.findNext().text
                if excerpt == '\n':
                    excerpt = header.findNext().findNext().text
        return cb[2] excerpt

### NORTH AMERICA
# CANADA
# USA

### SOUTH AMERICA
# ARGENTINA
# BRAZIL

### AFRICA
# EGYPT

### ASIA
# CHINA
# JAPAN
# THAILAND
# INDIA

### EUROPE
# GERMANY
# FRANCE
# SPAIN
# GREECE

## SCANDINAVIA

# FINLAND
# ICELAND
# NORWAY
# DENMARK
class eye_den_1(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url ='https://politiken.dk/'
        
    def get_header(self):
        return self.soup.find('h2', attrs={'class': 'article-intro__title headline headline--xxxlarge'}).text
    def get_excerpt(self):
        return self.soup.find('h2', attrs={'class': 'article-intro__title headline headline--xxxlarge'}).parent.find('ul', attrs={'class': 'article-intro__related'}).text


# SWEDEN
class eye_swe_1(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url = 'https://www.expressen.se/'
    def get_header(self):
        return self.soup.find('div', attrs={'class': 'teaser'}).find('h2').text
    def get_excerpt(self):
        return self.soup.find('div', attrs={'class': 'teaser'}).find('h2').next_sibling.text

class eye_swe_2(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url = 'https://www.aftonbladet.se/'       
    def get_header(self):
        return self.soup.find('h3').text
    def get_excerpt(self):
        return self.soup.find('h3').next_sibling.text

class eye_swe_3(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url = 'https://www.svd.se/'
    def get_header(self):
        return self.soup.find('h2').text
    def get_excerpt(self):
        return self.soup.find('h2').next_sibling.next_sibling.text

class eye_swe_4(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url = 'https://www.gp.se/'
    def get_header(self):
        return self.soup.find("div",  attrs = {'class': 'c-teaser__content'}).find("h2", attrs = {'class': 'c-teaser__title'}).text
    def get_excerpt(self):
        return self.soup.find("div", attrs = {'class': 'c-teaser__summery'}).text

class eye_swe_5(Proto_eye):
    def __init__(self):
        super().__init__(self)
        self.url = 'https://www.dn.se/' 
    def get_header(self):
        return self.soup.find('div', attrs= {'class': 'teaser-package__content'}).find('h1').text
    def get_excerpt(self):
        return self.soup.find('div', attrs= {'class': 'teaser-package__content'}).find('h1').next_sibling.next_sibling.text

