from helper_functions import plot_10_most_common_words, print_topics
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import os
import warnings

def lda_func(string, filename):
    sns.set_style('whitegrid')
    count_vectorizer = CountVectorizer(stop_words=('english'))
    count_data = count_vectorizer.fit_transform([string])
    plot_10_most_common_words(count_data, count_vectorizer, filename)
    warnings.simplefilter("ignore", DeprecationWarning)
    number_topics = 3
    number_words = 5
    lda = LDA(n_components=number_topics, n_jobs=-1, learning_method='online')
    lda.fit(count_data)
    print("Topics found via LDA:")
    print_topics(lda, count_vectorizer, number_words)

    from pyLDAvis import sklearn as sklearn_lda
    import pickle
    import pyLDAvis
    LDAvis_data_filepath = os.path.join('./ldavis_prepared_' + str(number_topics) + filename)
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:

        LDAvis_prepared = sklearn_lda.prepare(lda, count_data, count_vectorizer)

        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)

    # load the pre-prepared pyLDAvis data from disk
        with open(LDAvis_data_filepath, 'rb') as f:
            LDAvis_prepared = pickle.load(f)
            pyLDAvis.save_html(LDAvis_prepared, './ldavis_prepared_' + str(number_topics) + filename + '.html')
