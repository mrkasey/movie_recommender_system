import streamlit as st
import pandas as pd
import pickle

movies = pickle.load(open("moviesnew.pkl",'rb'))

def get_index(movie_name):
    idx = movies[movies['movie title'] == movie_name].index[0]
    return idx


def recommend_1(movie_list, similarity1):
    similarity = similarity1
    movie = movie_list[0]
    index = get_index(movie)
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommended_list = []
    recommended_poster = []
    ratings = []
    for i in distances[1:11]:
        recommended_list.append(movies.iloc[i[0]]['movie title'])
        recommended_poster.append(movies.iloc[i[0]]['poster_path'])
        ratings.append(movies.iloc[i[0]]['vote_average'])
    return recommended_list, recommended_poster, ratings


def recommend_2(movie_list, similarity1):
        similarity = similarity1
        index1= get_index(movie_list[0])
        index2= get_index(movie_list[1])
        pd1 = pd.DataFrame(list(enumerate(similarity[index1])),columns=['index number','distance'])
        pd2 = pd.DataFrame(list(enumerate(similarity[index2])),columns=['index number','distance'])
        pd4=pd.merge(pd1, pd2, on='index number', how='outer')
        pd4['average_dist'] = (pd4['distance_y'] + pd4['distance_x'])/2
        pd4 = pd4.sort_values(by = 'average_dist',ascending = False)

        recommended_list = []
        recommended_poster = []
        ratings = []
        for i in pd4['index number'][2:12].index:
            recommended_list.append(movies.iloc[i]['movie title'])
            recommended_poster.append(movies.iloc[i]['poster_path'])
            ratings.append(movies.iloc[i]['vote_average'])
        return recommended_list, recommended_poster, ratings

def recommend_3(movie_list, similarity1):
        similarity = similarity1
        index1= get_index(movie_list[0])
        index2= get_index(movie_list[1])
        index3= get_index(movie_list[2])
        pd1 = pd.DataFrame(list(enumerate(similarity[index1])),columns=['index number','distance'])
        pd2 = pd.DataFrame(list(enumerate(similarity[index2])),columns=['index number','distance'])
        pd3 = pd.DataFrame(list(enumerate(similarity[index3])),columns=['index number','distance'])
        pd4=pd.merge(pd1, pd2, on='index number', how='outer').merge(pd3, on='index number', how='outer')
        pd4['average_dist'] = (pd4['distance'] + pd4['distance_x'] + pd4['distance_y'])/3
        pd4 = pd4.sort_values(by = 'average_dist',ascending = False)

        recommended_list = []
        recommended_poster = []
        ratings=[]
        for i in pd4['index number'][3:13].index:
            recommended_list.append(movies.iloc[i]['movie title'])
            recommended_poster.append(movies.iloc[i]['poster_path'])
            ratings.append(movies.iloc[i]['vote_average'])
        return recommended_list, recommended_poster, ratings
@st.cache_data(show_spinner=False)
def recommend(movie_list):
    similarity1 = pickle.load(open("similarity_16_new.pkl", 'rb'))
    if len(movie_list) == 1:
        return recommend_1(movie_list, similarity1)
    elif len(movie_list) == 2:
        return recommend_2(movie_list, similarity1)
    elif len(movie_list) == 3:
        return recommend_3(movie_list, similarity1)

## Webapp
st.title("Movie Recommender"+":clapper:")


x = st.multiselect( label="Select Movies", label_visibility="hidden",options= movies['movie title'].values,max_selections=3, placeholder="SELECT UPTO 3 MOVIES")

# Define a function to handle null values in the recommended_poster list
def get_image_url(url):
    url = str(url)
    if len(url)<5:
        return "https://static.displate.com/857x1200/displate/2022-04-15/7422bfe15b3ea7b5933dffd896e9c7f9_46003a1b7353dc7b5a02949bd074432a.jpg"
    else:
        return "https://image.tmdb.org/t/p/original" + str(url)

if st.button("Find Movies"+":movie_camera:"):
    st.header("Recommended Movies:")
    with (st.spinner("Finding Movies...")):
        recommended_list, recommended_poster, ratings = recommend(x)
        col1, col2, col3, col4, col5 = st.columns(5)
        # Column 1
        with col1:
            st.image(get_image_url(recommended_poster[0]))
            st.write(recommended_list[0])
            st.write((round(ratings[0],1)))
            st.divider()
            st.image(get_image_url(recommended_poster[1]))
            st.write(recommended_list[1])
            st.write((round(ratings[1], 1)))

        # Column 2
        with col2:
            st.image(get_image_url(recommended_poster[2]))
            st.write(recommended_list[2])
            st.write((round(ratings[2], 1)))
            st.divider()
            st.image(get_image_url(recommended_poster[3]))
            st.write(recommended_list[3])
            st.write((round(ratings[3], 1)))

        # Column 3
        with col3:
            st.image(get_image_url(recommended_poster[4]))
            st.write(recommended_list[4])
            st.write((round(ratings[4], 1)))
            st.divider()
            st.image(get_image_url(recommended_poster[5]))
            st.write(recommended_list[5])
            st.write((round(ratings[5], 1)))

        # Column 4
        with col4:
            st.image(get_image_url(recommended_poster[6]))
            st.write(recommended_list[6])
            st.write((round(ratings[6], 1)))
            st.divider()
            st.image(get_image_url(recommended_poster[7]))
            st.write(recommended_list[7])
            st.write((round(ratings[7], 1)))

        # Column 5
        with col5:
            st.image(get_image_url(recommended_poster[8]))
            st.write(recommended_list[8])
            st.write((round(ratings[8], 1)))
            st.divider()
            st.image(get_image_url(recommended_poster[9]))
            st.write(recommended_list[9])
            st.write((round(ratings[9], 1)))


