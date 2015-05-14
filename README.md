# nltk-wrapper
Wrapper that helps making text analysis with NLTK more comfortable

By structuring text into documents, sentences and words. Handling of text becomes much more comfortable. The wrapper performs tokenization and structuring of sentences and words into dictionaries, stemming, POS-tagging and sentiment weighting with one function call
```
document = Doc(body_string)
```

and easily compiles a breakdown of the body of the text
```
document.breakdown()
```

The wrapper is also able to perform trivial sentiment analysis by counting the number of positive and negative words.

Based on NLTK and dictionaries from the Harvard Inquirer.

Requires Python 3 and the Natural Language ToolKit.
