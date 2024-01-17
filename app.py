import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv('data.csv')
embedded_description = pd.read_csv('embedded_description.csv')

neigh = NearestNeighbors(n_neighbors=5).fit(embedded_description)

def get_similar_books(title_book):
    index = 0
    
    # match the input(title_book) with title columns
    for idx, value in enumerate(data['titles']):
        if title_book in value:
            index = idx
    
    # get embedded vector of book's description
    embedded_vector =  embedded_description.iloc[index, :]

    # get Top 5 five similar embedded vectors' indices to our embedded vector
    indices = neigh.kneighbors([embedded_vector], 5, return_distance=False)

    return indices    

# set title
st.title('Recommendation book system')
st.write("This recommendation system depends on", "https://books.toscrape.com/", "website!")

# get the name of the book
title_book = st.text_input('Book title', 'Enter text')

if title_book != "Enter text":
    
    indices = get_similar_books(title_book)[0]

    st.write('The first recommended book is', data.iloc[indices[1], 0])
    st.write("link: ", data.iloc[indices[1], 2])

    st.write('The second recommended book is', data.iloc[indices[2], 0])
    st.write("link: ", data.iloc[indices[2], 2])

    st.write('The thrid recommended book is', data.iloc[indices[3], 0])
    st.write("link: ", data.iloc[indices[3], 2])

    st.write('The fourth recommended book is', data.iloc[indices[4], 0])
    st.write("link: ", data.iloc[indices[4], 2])
    