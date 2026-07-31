import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Mini Agentic Pipeline",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Mini Agentic Pipeline")
st.markdown("Ask questions about policies, plans, pricing, support, and more.")

# User Input
query = st.text_input(
    "Ask a question",
    placeholder="Example: What is the price of Pro Plan?"
)

# Submit Button
if st.button("Submit"):

    if not query.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"query": query}
            )

            if response.status_code == 200:

                result = response.json()

                st.subheader("Answer")
                st.success(result["answer"])

            else:
                st.error(
                    f"Server Error ({response.status_code})"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI backend. "
                "Make sure the server is running."
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")