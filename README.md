# twitter_sentiment_analysis

Hi! in this project I've downloaded datasets from IEEEDataport ([CORONAVIRUS (COVID-19) GEO-TAGGED TWEETS DATASET](https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset) and [TWEETS ORIGINATING FROM INDIA DURING COVID-19 LOCKDOWNS](https://ieee-dataport.org/open-access/tweets-originating-india-during-covid-19-lockdowns)). The datasets contains two columns tweetid and sentiment_score the dataset is in form for csv file and database (you can use sqlite3 to open them). I used tweepy to download tweets using tweet id using twitter api. I was used [OPTUNA](https://optuna.org/) for hyperparameter tunning.

The api folder contains a flask api to test the model. The api support both POST and GET methods.
To run api in your local env donwload the code. In the api folder

```python
pip install -U -r requirements.txt
```
Then 
```python
python testModelAPI.py
```
[Demo video](https://drive.google.com/file/d/1CdK6b5jFuc8-JEgyoc3GvvQY27ghas6x/view?usp=sharing) how to test api using postman.
