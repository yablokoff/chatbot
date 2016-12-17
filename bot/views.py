#  coding: utf-8

import json
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from models import Tweet

@csrf_exempt
def test_view(request):

    if request.method == 'POST':
        message = request.POST['message']
        stemmer = nltk.stem.snowball.RussianStemmer()
        tweets = Tweet.objects.all()
        texts = list()

        tokenized_message = nltk.tokenize.word_tokenize(message, language='slovene')
        tokenized_message = map(stemmer.stem, tokenized_message)

        processed_message = " ".join(tokenized_message)

        for tweet in tweets:
            texts.append(tweet.text)

        vectorizer = TfidfVectorizer(min_df=2, preprocessor=stemmer.stem)
        vectorizer.fit(texts)

        vector_context = vectorizer.transform([processed_message])
        vector_doc = vectorizer.transform(texts)

        result = np.dot(vector_doc, vector_context.T).todense()
        result = np.asarray(result).flatten()

        best_responses_indexes = np.argsort(result, axis=0)[::-1]
        best_responses = list()

        for i in best_responses_indexes[:10]:
            best_responses.append(texts[i])

        return HttpResponse(json.dumps({"responses": best_responses}), 'application/json', 200)
        # return HttpResponse(json.dumps({"responses": "hello"}), 'application/json', 200)
    else:
        return Http404
