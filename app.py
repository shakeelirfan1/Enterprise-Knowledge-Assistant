import streamlit as st
from rag import ask_question

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Knowledge Assistant")
st.write("Ask questions about the uploaded enterprise documents.")

question = st.text_input("💬 Ask a question")

if st.button("🔍 Search"):

    if question.strip():

        with st.spinner("Searching documents..."):

            result = ask_question(question)

        st.success("Answer Generated Successfully!")

        st.subheader("📌 Answer")
        st.write(result["answer"])

        st.subheader("📚 Sources")

        for i, doc in enumerate(result["sources"], start=1):

            source = doc.metadata.get("source", "Unknown Document")
            page = doc.metadata.get("page", "Unknown")

            st.markdown(
                f"**{i}. Document:** `{source}`  \n"
                f"**Page:** {page + 1 if isinstance(page, int) else page}"
            )