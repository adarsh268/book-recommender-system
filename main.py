import streamlit as st
import numpy as np
import pickle

# Load data and models
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Filter the top 50 rated books
top_rated_books = popular_df.nlargest(50, 'num_ratings')

# Streamlit UI
st.title('Book Recommender System')

st.sidebar.subheader('Recommendation Options')
recommendation_type = st.sidebar.selectbox('Select Recommendation Type',
                                           ('Popularity Based', 'Collaborative Filtering'))

if recommendation_type == 'Popularity Based':
    st.subheader('Popularity Based Recommendations')
    num_recommendations = 5
    recommendations = popular_df[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating']].head(
        num_recommendations)

    for idx, row in recommendations.iterrows():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(row['Image-URL-M'], use_column_width=True, width=100)
        with col2:
            st.write(f"**Title:** {row['Book-Title']}")
        with col3:
            st.write(f"**Author:** {row['Book-Author']}")
        with col4:
            st.write(f"**Number of Ratings:** {row['num_ratings']}")
        with col5:
            st.write(f"**Average Rating:** {row['avg_rating']}")
        st.write("---")

elif recommendation_type == 'Collaborative Filtering':
    st.subheader('Collaborative Filtering Recommendations')

    # Create a dropdown menu with the top 50 rated books
    top_rated_book_titles = top_rated_books['Book-Title'].tolist()
    selected_book_title = st.selectbox('Select a book title:', top_rated_book_titles)

    # Create a text input box for users to enter a book title
    book_name = st.text_input('Or enter a book title:')

    if st.button('Recommend'):
        if book_name:
            selected_book_title = book_name

        try:
            index = np.where(pt.index == selected_book_title)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
            st.write(f"**Recommendations for '{selected_book_title}':**")
            for i in similar_items:
                recommended_book = pt.index[i[0]]
                recommended_book_data = books[books['Book-Title'] == recommended_book].iloc[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.image(recommended_book_data['Image-URL-M'], use_column_width=True, width=100)
                with col2:
                    st.write(f"- **Title:** {recommended_book}")
        except IndexError:
            st.write(f"Book '{selected_book_title}' not found in the dataset. Please select a valid book title.")

# Display original data (for debugging purposes)
# st.subheader('Original Data')
# st.write(books)
# st.write(popular_df)
# st.write(pt)


