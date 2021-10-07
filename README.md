# Scrapy Demo
Here are the commands that I used in the A51 demo to show Scrapy's functionality. I'm running Ubuntu 20.04 and using Google Chrome, I leave it to you to find out how to convert these commands depending on your operating system and your browser. 

This demo will show you how to install and use scrapy, including scrapy's shell functionality and scrapy projects. By the end of this demo, I will show you how to crawl a digital library using a pre-defined query, and combine the output of multiple queries into one bibtex file.

### Scrapy Functionality
Before jumping into installing and implementing scrapy, a couple quick notes.

First, scrapy is a web crawler, not a browser. So, it can scrape information from the HTML of a website, it can have trouble rendering Javascript. If you are crawling and are having issues because the content is being rendered using Javascript, you might have to switch to a headless browser such as Selenium. I do not have experience with this, so I leave research in this area to you if needed.

Secondly, some sites welcome users to scrape their content, other sites might not be as compliant. Some sites will try to identify scraping behavior and block your IP temporarily if you're found out. I'll show you how to circumvent this, but it's something that's important to remember. If your IP gets blocked by a content delivery network, your IP will be banned by a notable portion of the internet :) 

Lastly, we need to understand the flow for how we will be crawling websites with scrapy. Here's a general flow we will be following:
1. Use list of search terms to build queries
2. Embed each query into a URL
3. Load URLs into scrapy
4. Have scrapy crawl URLs and scrape relevant content
5. Output content into query/URL-specific file
6. Combine output files into single file with relevant statistics

Keep in mind that one general goal you want to try to accomplish is to get the information you need in as little web-requests as possible. This flow will be followed more closely when we build a spider later on. For now, I will show you how to install scrapy and practice scraping content from a website.

### Installing Scrapy
To install Scrapy, I used the pip package manager after creating a virtual environment using python3. First, here's the command I used to create my virtual environment. 
`$ python3 -m venv env`

Now that I've created my virtual environment, there should be a new subdirectory in my current directory called `env`. To open into my virtual environment, run this command from your current working directory (where you ran the previous command).
`$ source env/bin/activate`

You are now in your python3 virtual environment, which isolates packages installed in this environment from ones installed in the system site directories. You can read more about virtual environments by searching for the `venv` library in Python's documentation. With that out of the way, here's the command for installing scrapy.
`$ pip install scrapy`

I leave it to your own research if you want to install scrapy through a different medium, or run into errors during the installation process. Now that we have scrapy installed, let's look at how to use it.


### Scrapy Shell
Now that scrapy is installed, we will explore the scrapy shell. The scrapy shell is a really easy way to begin playing with and getting comfortable using the framework, and learning how to scrape content. 

To enter scrapy's customized shell interface, you first need a URL that you would like to practice scraping. For this, I'm going to perform a query on ACM's digital library for '"UAS" AND "security"'. This gives me the following URL: 
`https://dl.acm.org/action/doSearch?AllField=%22UAS%22+AND+%22security%22`

So, to enter scrapy's shell with this URL, I run this command:
`$ scrapy shell 'https://dl.acm.org/action/doSearch?AllField=%22UAS%22+AND+%22security%22'`

You should see a bit of stuff output to your console. If you see a line that says `<date> <time> [scrapy.core.engine] DEBUG: Crawled (200) .....`, then scrapy was able to pull the content from the URL you provided. Nice! Here's the command that will render all of the HTML/CSS that scrapy collected into your browser:
`>>> view(response) `

If you run this command in the scrapy shell and see the content you want to scrape, then the content is rendered in HTML/CSS. Nice! In the case for ACM's digital library (specifically for the URL above), if you run this command, you will see information that can be scraped. 

Now in your scrapy shell, the following command will print all of the HTML/CSS that was rendered to your console:
`>>> print(response.body)`

This looks like jibberish, but scrapy makes pulling information out of this easily. Scrapy uses 'selectors' to help us do this, and I will show you how to use selectors to extract the titles of each article found in the ACM digital library URL (above). To do so, follow these steps.

In your console...
* Run the earlier command to enter the scrapy shell to the ACM digital library URL, `$ scrapy shell 'https://dl.acm.org/action/doSearch?AllField=%22UAS%22+AND+%22security%22'`
* Run `>>> view(response)` in the scrapy shell, opening your browser to the scraped website response

In your browser...
* In the browser tab that opened up, scroll down until you find an article title. Right click on the article title, and hit "Inspect"
* On the right side, the inspect element sub-window should have opened up. A line with `<a href="/doi/...">...</a>` should be highlighted.
* Above this, there's a line that has `<span class="hlFld-Title">`. This `span` object has a class ID of `hlFld-Title`. This is potentially a unique identifier for the article title, which is important.

Back to your console... let's print out all the article titles. Based off of the potential unique identifier we found earlier, let's use scrapy's selectors to grab the content held by objects with those identifiers within the HTML response. We can do that using this command. Notice it's similarity to the information we got from the browser.
`>>> response.css('span.hlFld-Title')`

What's the length of this list? 20. How many articles are shown by default per page in ACM's digital library? Also, 20! So likely, within each of the objects in this list, exists the title for each article shown on the URL we scraped. Let's extract the raw HTML using the `extract()` function.
`>>> response.css('span.hlFld-Title').extract()`

Now, you can see the title of each article from the URL we scraped. Unfortunately it's surrounded by HTML tags that we don't really need. Luckily, I've put together a Python function that will lazily use regular expressions to remove the tags. Here it is:
```
>>> import re
>>> def scrub_html_tags(html_str): return re.sub(" +", " ", (re.sub("<.*?>","",html_str)).replace("\n",""))
```

The regular expressions first take out anything surrounded by (and including) pointy brackets ('<' and '>'), then I string replace newline characters with spaces, and finally I use regular expressions again to replace any instance of 2+ space characters with just 1 space character. Now, we can iterate through the `response.css('span.hlFld-Title').extract()` list and extract the article titles! Let's give it a shot.
```
>>> for html in response.css('span.hlFld-Title').extract(): print(scrub_html_tags(html))
... 
Automation and interoperability challenges for heterogeneous UAS fleet management
An architecture to automate UAS operations in non-segregated airspace
Design and Experiment of Autonomous Flight UAS Geofence Algorithm
A taxonomy of UAS separation maneuvers and their automated execution
Cognitive Security: Security Analytics and Autonomics for Virtualized Networks
An approach for safety assessment in UAS operations applying stochastic fast-time simulation with parameter variation
Security issues with the IP multimedia subsystem (IMS)
Security considerations for active messages
Localisation of Drone Controllers from RF Signals using a Deep Learning Approach
Specification based intrusion detection for unmanned aircraft systems
Reliable Command, Control and Communication Links for Unmanned Aircraft Systems: Towards compliance of commercial drones
Critical vpn security analysis and new approach for securing voip communications over vpn networks
The study and implementation of VoIP intelligent voice communication system based on SIP protocol
Security considerations for active messages
A Comparison of Avionics Open System Architectures
Good security practice for personal computers
Software Radios for Unmanned Aerial Systems
The Other Side of the Coin: A Framework for Detecting and Analyzing Web-based Cryptocurrency Mining Campaigns
VirtualDrone: virtual sensing, actuation, and communication for attack-resilient unmanned aerial systems
Movement Patterns as Enrichment: Exploratory Canine-Drone Interaction Pilot Study
```

Nice! We can follow a similar process to extract the authors for each article in this URL. Here I used regular expressions again to remove extra commas and make things look pretty.
```
>>> for list_of_auths in response.css('ul.loa'):
...  print([re.sub(", $","",scrub_html_tags(auth)) for auth in list_of_auths.css('li').extract()])
... 
['Nicolas Giuditta', 'Marcel Quintana', 'Lorena Fernández', 'Esteban Gutiérrez', 'Joaquim Oliveira', 'Santi Vilardaga']
['Enric Pastor', 'Pablo Royo', 'Eduard Santamaria', 'Marc P. Batlle', 'Cristina Barrado', 'Xavier Prats']
['Qixi Fu', 'Xiaolong Liang', 'Jiaqiang Zhang', 'Duo Qi', 'Xiujun Zhang']
['Marc Pérez-Batlle', 'Enric Pastor', 'Pablo Royo', 'Xavier Prats', 'Cristina Barrado']
['Lalita Jagadeesan', 'Alan Mc Bride', 'Vijay K. Gurbani', 'Jie Yang']
['Joao Luiz de Castro Fortes', 'Rafael Fraga', 'Kenny Martin']
['Michael T. Hunter', 'Russell J. Clark', 'Frank S. Park']
['R. A. McBride']
['David Shorten', 'Ashley Williamson', 'Saket Srivastava', 'John C. Murray']
['Robert Mitchell', 'Ing-Ray Chen']
['Jens Finkhäuser', 'Morten Larsen']
['Wafaa Bou Diab', 'Samir Tohme', 'Carole Bassil']
['Zhou Gongjian']
['R. A. McBride']
['Joyce L. Tokar']
['William Murray']
['Keith Powell', 'Aly Sabri Abdalla', 'Daniel Brennan', 'Vuk Marojevic', 'R. Michael Barts', 'Ashwin Panicker', 'Ozgur Ozdemir', 'Ismail Guvenc']
['Julian Rauchberger', 'Sebastian Schrittwieser', 'Tobias Dam', 'Robert Luh', 'Damjan Buhov', 'Gerhard Pötzelsberger', 'Hyoungshick Kim']
['Man-Ki Yoon', 'Bo Liu', 'Naira Hovakimyan', 'Lui Sha']
['K. Cassie Kresnye', 'Patrick C. Shih']
```

So, using the above URL, we were able to scrape a bunch of data, including the titles and authors of articles found on that URL. You can do the same to gather the DOI link, the year the article was published, and more. This is cool, but we want to extend this capability a bit to automate the crawling and scraping process. I'll show you how to do that in the next section, where we talk about scrapy projects and spiders.


### Scrapy Projects & Spiders
Our goal here is to build a spider to crawl a URL and scrape information from the site. To do that, we need to build a scrapy project to define settings and configurations, and to manage our spiders. To build a scrapy project named 'demo', run this command in your console (we aren't in the scrapy shell any longer).
`$ scrapy startproject demo`

A new directory `demo` was created. Within this directory we have a `scrapy.cfg` configuration file and another `demo` subdirectory. The `demo` subdirectory holds more files and a `spider` subdirectory, which is where you will put your spiders once you have coded them. In order to build a template to start coding a spider, run the following command in your console:
`$ scrapy genspider acm dl.acm.org`

This command will create a spider template with a specific name (in this case, "acm") and a specified starting URL (in this case, http://dl.acm.org). If we open `spiders/acm.py`, we can see the template. As I said in the beginning, we need to first come up with a set of URLs that we would like to scrape. To do this, we would first need to build a set of search terms, and combine all permutations of this search terms to build larger queries. From there, we can use those queries to build URLs. 

For this demo, we only want to show one URL being scraped. So, go ahead and replace the `start_urls` variable with this:
```
start_urls = ["https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&text1=%22uas%22+AND+%22drone%22+AND+%22security%22&startPage=0&pageSize=20"]
```

This URL is for the query '"uas" AND "drone" AND "security"'. Notice how you could alter the `pageSize` parameter in the URL to potentially reduce the number of HTTP requests made to `dl.acm.org`. Let's also change the `parse` function to look like this:
```
def parse(self, response):
    print(response.body)
    pass
```

With this, all we are doing is printing the response content before returning. Now let's run our spider. Save the changes that you've made and run the following command in your console:
`$ scrapy crawl acm`

It doesn't look like we got the output of the response, so something appears to have gone wrong. Looking at our debugging output, we can see..
```
2021-10-07 16:19:22 [scrapy.downloadermiddlewares.robotstxt] DEBUG: Forbidden by robots.txt: <GET https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&text1=%22uas%22+AND+%22drone%22+AND+%22security%22&startPage=0&pageSize=20>
```

It looks like the `robots.txt` file under `dl.acm.org` is forbidding us from crawling this site. How can we circumvent this? By going into the `settings.py` file and changing `ROBOTSTXT_OBEY = False` to `True`. Here's another couple changes to the settings that I would recommend...
* Set `DOWNLOAD_DELAY = 5`, and try not to dip below 5. This decides how many seconds to wait before making another HTTP GET request to the same URL. This can save you from having your IP blacklisted :) 
* Change the `USER_AGENT` to a string that mimics a browsers user agent. I use `USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'`. Some websites will watch for and forbid weird/specific user agents.

With those settings, try running `$ scrapy crawl acm` again. You should see the response being printed, so stuff is working!

Now we want to automate the process of scraping the content we are looking for, per article. Here's the crawler I wrote to scrape the title, DOI link and author listing for each article in the first page of the URL listed above.
```py
import scrapy
import re

def scrub_html_tags(html_str): 
    return re.sub(" +", " ", (re.sub("<.*?>","",html_str)).replace("\n",""))

class AcmSpider(scrapy.Spider):
    name = 'acm'
    allowed_domains = ['acm.org']
    start_urls = ["https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&text1=%22uas%22+AND+%22drone%22+AND+%22security%22&startPage=0&pageSize=20"]

    def parse(self, response):
        # get results from current page
        page_results = response.css('li.issue-item-container')

        # for each result, print the title, authors, and DOI.
        for result_i in page_results:
            try:
                title = scrub_html_tags(result_i.css('span.hlFld-Title').extract()[0])

                doi = re.findall(r'a href=".*?"', result_i.css('span.hlFld-Title').css('a').extract()[0])
                doi = doi[0].replace('/doi/','https://doi.org/')
                doi = re.sub('^a href="', '', doi)
                doi = re.sub('"$', '', doi)

                authors = [scrub_html_tags(html_str) for html_str in result_i.css('ul.loa').css('li').extract()]
                authors = [re.sub(', $','', auth_i) for auth_i in authors]

                json_obj = {'Title': title, 'DOI': doi, 'Authors': authors, 'Keywords': ['"uas" AND "Drone" AND "security"']}
                yield json_obj
            except:
                pass

        pass
```

Notice we are using the `yield` built-in in python. This is so we can begin printing our results to a file. Also notice that we are adding the search terms used for this query as "keyword" objects, this will be important later. To run this crawler and print our results to `test.json`, we run the following command:
`$ scrapy crawl acm -o test.json `

Now if we open `test.json`, we can see all the results from the first page, awesome! But, what if we also want results from the following pages? We can write a loop to identify the "next page" button and use it to continue to the next page. Like so:
```py
import scrapy
import re

def scrub_html_tags(html_str): 
    return re.sub(" +", " ", (re.sub("<.*?>","",html_str)).replace("\n",""))

class AcmSpider(scrapy.Spider):
    name = 'acm'
    allowed_domains = ['acm.org']
    start_urls = ["https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&text1=%22uas%22+AND+%22drone%22+AND+%22security%22&startPage=0&pageSize=20"]

    def parse(self, response):
        # get results from current page
        page_results = response.css('li.issue-item-container')

        # for each result, print the title, authors, and DOI.
        for result_i in page_results:
            try:
                title = scrub_html_tags(result_i.css('span.hlFld-Title').extract()[0])

                doi = re.findall(r'a href=".*?"', result_i.css('span.hlFld-Title').css('a').extract()[0])
                doi = doi[0].replace('/doi/','https://doi.org/')
                doi = re.sub('^a href="', '', doi)
                doi = re.sub('"$', '', doi)

                authors = [scrub_html_tags(html_str) for html_str in result_i.css('ul.loa').css('li').extract()]
                authors = [re.sub(', $','', auth_i) for auth_i in authors]

                json_obj = {'Title': title, 'DOI': doi, 'Authors': authors, 'Keywords': ['"uas" AND "Drone" AND "security"']}
                yield json_obj
            except:
                pass

        # act on pagination
        next_pg = response.css('a.pagination__btn--next::attr("href")').get()
        if next_pg is not None:
            yield response.follow(next_pg, self.parse)
        else:
            pass
```

If you find that the visiting the actual DOI link of an article provides more information that you would like to keep in each JSON object, you can customize scrapy to reach out to those sites and collect that information as well. For the purpose of keeping this demo on the shorter side, I'm going to leave that to your own research. Although the scrapy documentation is very well put-together, it shouldn't take long to accomplish this. Remember that the goal is to perform as little web requests as possible, so try to avoid reaching out to 1 site per article if possible. 

If we perform this process for several URLs, we come up with several output files. Specifically, there will be one file for each URL/query. Next, we will explore combining these output files into one file with deduplicated results and additional statistics. This single output file will also be in a format that can be accepted by reference managers, we will be using bibtex.


### Combining Output Files
Again, the purpose of combining the output files into just one file is to:
1. Deduplicate results
2. For each result, adding keywords that tell which search query/queries found the article, and how often it appeared
3. Change the output format into something accepted by a reference manager (like bibtex)

To accomplish #1, we just need to use a unique identifier for each article that we collect. Luckily, each article's unique identifier is it's DOI code! To accomplish #2, we need to keep track of which query we are working with, and how often we see throughout each file. To accomplish #3, we can write a function that takes a JSON object as input and produces a corresponding bibtex string.

Given that each article has a title, DOI and list of authors, I've written a script called `json2bib.py` which performs #1, #2 and #3. Each function within this script is labeled according to which goal it accomplishes. For example, the function `req_1` accomplishes #1, etc.

I have a few json files that can be used to test this script. You can perform this test, assuming that `json2bib.py` and `test_files/` are in the current working directory:
`$ json2bib.py test_files`

This will produce a new file within the current working directory, `all.bib`, which is the new single output file that contains all results. This can be imported into Zotero. 