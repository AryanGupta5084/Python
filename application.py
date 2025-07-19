from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import pymongo
import cloudscraper
import time
import random
from requests.exceptions import RequestException
import csv

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)


@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "cPHDOP col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            }
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                }
            )
            try:
                prodRes = scraper.get(productLink, headers=headers, timeout=60)  # Increased timeout
                print(f"Status code: {prodRes.status_code}")

                if prodRes.status_code == 200:
                    prodRes.encoding = 'utf-8'
                    prod_html = bs(prodRes.text, "html.parser")
                else:
                    print(f"Failed to fetch page. Status code: {prodRes.status_code}")

            except RequestException as e:
                print(f"Error fetching the page: {e}")
                print("Site may be overloaded or blocking requests.")

            time.sleep(random.uniform(5, 10))
            commentboxes = prod_html.find_all('div', {'class': "RcXBOT"})

            filename = searchString + ".csv"
            fw = open(filename, 'a', newline='')
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw_writer = csv.writer(fw)
            fw_writer.writerow(headers)
            fw.close()
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2NsDsF AwS1CA'})[0].text

                except:
                    logging.info("name")

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                fw = open(filename, 'a', newline='')
                fw_writer = csv.writer(fw)
                fw_writer.writerow(mydict)
                fw.close()
            logging.info("log my final result {}".format(reviews))

            from pymongo import MongoClient
            uri = "mongodb+srv://aryan_gupta84:Bhalua12@cluster0.dp1f01p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            # Create a new client and connect to the server
            client = MongoClient(uri)
            # Send a ping to confirm a successful connection
            try:
                client.admin.command('ping')
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

            db =  client['scrapper_flipkart_review']
            coll = db['scrapper_review']
            coll.insert_many(reviews)

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")