# 2019LingProject
語言計算認知導論期末報告

To get the features of a news, run crawl_selenium.py with the pickle files

`$ python crawl_selenium.py`

To transfer the json files into pretty formatted, type the command:

`$ python -m json.tool > data_pretty.json < data.json`

Currently, data in this project include the following:

1. News articles in data frame format from News Lens(關鍵評論網) and Reporter(報導者). The number of articles are 1532 and 692 respectively.
`newslens_1.pkl`
`twreporter_1.pkl`

2. Tf-idf values of news article content from both sources.
`newslens_tfidf.json`
`newslens_tfidf_df.pkl`
`twreporter_tfidf.json`
`twreporter_tfidf_df.pkl`
