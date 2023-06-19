import streamlit as st
import pickle
import pandas as pd
import requests

with open('Style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = new_movie_list[new_movie_list['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommend_posters = []
    for i in movie_list:
        movie_id = new_movie_list.iloc[i[0]].id
        #fetching poster from api
        recommend_posters.append(fetch_poster(movie_id))
        recommended_movies.append(new_movie_list.iloc[i[0]].title)
    return recommended_movies,recommend_posters

movie_dict = pickle.load(open('movie_dicts.pkl','rb'))
new_movie_list = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
st.header('Movie Recommender System')

selected_movie_name = st.selectbox(label='Enter or select movie name',
                   options = new_movie_list['title'])



if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.write(names[0])
    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[2])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])
    with col5:
        st.image(posters[4])
        st.write(names[4])



