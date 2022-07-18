"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
# this runs when webpages opens, need to import libraries, initialize, set variables
## import libraries for webpage
import os
from flask import Flask, render_template, request, redirect, url_for
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize, TextTilingTokenizer
import re
import keras
from keras.preprocessing.text import Tokenizer
from keras import models, layers, optimizers
from keras.models import load_model

## initializing webpage
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
#auto reload while testing
app.config["TEMPLATES_AUTO_RELOAD"] = True

## functions for use in webpage
def initialize():
    '''Loads model and tokenizer.'''
    # load model
    model = load_model('model.h5')
    # load tokenizer
    file = open('tokenizer.pickle', 'rb')
    tokenizer = pickle.load(file)
    return model, tokenizer

def lemmatize(data):
    '''With raw text data passed in as a single array, will return
    each word with each sentence and its punctuation lemmatized'''
    wnl = WordNetLemmatizer()
    processed = ' '.join(data.splitlines())
    tokens = [word for sent in nltk.sent_tokenize(processed) for word in nltk.word_tokenize(sent)]
    lemmas = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            lemmas.append(wnl.lemmatize(token))
        else:
            lemmas.append(token)
    return lemmas

def preprocessing(para):
    '''Loads stopwords to be used, splits data up into managable chunks for the model,
    lemmatizes input data, and vectorizes data.'''
    # loading stopwords (combination of elizabethan stopwords and nltk's english stopwords)
    file = open('stopwords.pickle', 'rb')
    stop_words = pickle.load(file)
    # generating paragraphs to evaluate based on full texts
    tt = TextTilingTokenizer(stopwords=stop_words)
    # ensure data passed in is a string
    para = str(para)
    try:
        # splitting data into smaller bits to pass into model
        print('Splitting input.')
        paragraph = tt.tokenize(para)
        # text processing -lemmatizing to pass into model
        print('Processing input.')
        lemmas = lemmatize(paragraph)
    except ValueError:
        # text processing -lemmatizing to pass into model
        print('Processing input.')
        lemmas = lemmatize(para)
    print('Returning data.')
    # vectoring
    one_hot_results= tokenizer.texts_to_matrix([lemmas], mode='tfidf')
    return one_hot_results

def model_predict(text):
    '''Passes preprocessed text into model and classifies text, returning approximate lexile level.'''
    file = open('labels.pickle', 'rb')
    classes = pickle.load(file)
    file.close()
    for index, value in enumerate(model.predict(preprocessing(text))[0]):
        if value > 0.70:
            print('Lexile Found!')
            found_lexile = classes[index]
            if found_lexile == classes[0]:
                to_post = 'This text is suitable for early elemetary aged readers. The lexile range for this text is from 0 to 650L.'
            elif found_lexile == classes[3]:
                to_post = 'This text is suitable for late elementary aged readers. The lexile range for this text is from 650L to 1050L.'
            elif found_lexile == classes[1]:
                to_post = 'This text is suitable for middle school aged readers. The lexile range for this text is from 1050L to 1200L.'
            else:
                to_post = 'This text is suitable for high school aged readers. The lexile range for this text is from 1200L to 1400L.'
            break
        elif value > 0.3:
            found_lexile = classes[index]
            if found_lexile == classes[0]:
                to_post = 'This text is most similar to texts suitable for early elemetary aged readers. The lexile match is closet to the range 0 to 650L.'
            elif found_lexile == classes[3]:
                to_post = 'This text is most similar to texts suitable for late elementary aged readers. The lexile match is closet to the range 650L to 1050L.'
            elif found_lexile == classes[1]:
                to_post = 'This text is most similar to texts suitable for middle school aged readers. The lexile match is closet to the range 1050L to 1200L.'
            else:
                to_post = 'This text is most similar to texts suitable for high school aged readers. The lexile match is closet to the range 1200L to 1400L.'
            break
        elif index > 3:
            to_post = 'No lexile match'
        else:
            print('Reevaluating.')
    return to_post

## setting variables for model
global model
model, tokenizer = initialize()

# Routing for your application.
@app.route('/', methods=["GET", "POST"])
def home():
    """Render website's home page."""
    return render_template('home.html')

#new route for /predict

@app.route('/predict', methods=["GET", "POST"])
def predict():
    """predicts what lexile level the user passed in"""
    user_input = request.form['user.input']
    to_post = model_predict(user_input)
    return render_template("home.html", to_post=to_post)#a thing to send to js in whatever format you want the user to see

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
