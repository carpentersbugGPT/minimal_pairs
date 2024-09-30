import streamlit as st

# Title and Header
st.title("Hello, Streamlit!")
st.header("This is a simple test app")

# Body Text
st.write("If you're seeing this, your Streamlit app is working correctly!")

# Add a simple number input
number = st.number_input("Pick a number", min_value=0, max_value=100)
st.write(f"The number you picked is: {number}")

# Add a button
if st.button("Click me"):
    st.write("Button clicked!")

# Display an image from URL
st.image("https://via.placeholder.com/150", caption="Test Image")

