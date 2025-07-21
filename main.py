import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Set up the page
st.set_page_config(page_title="Cold Email Generator", page_icon="📧", layout="wide")

# Minimal Styling
st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 10px;
    }
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
        transform: scale(1.03);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.title("📧 Cold Mail Generator")
st.markdown("### Paste a job posting URL and generate a personalized cold email.")
st.markdown("---")

# Input
url_input = st.text_input(
    "🔗 Enter a Job URL:",
    value="https://amazon.jobs/en/jobs/2926179/real-estate-development-manager-strategy-and-investment-data-center-supply-solutions",
    help="Paste the job posting URL from any company career page.",
)

# Button with Sparkles
submit_button = st.button("✨ Generate Email")

# Logic
if submit_button:
    if url_input.strip() == "":
        st.warning("⚠️ Please enter a valid job URL.")
    else:
        try:
            with st.spinner("⏳ Generating your cold email..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                portfolio = Portfolio()
                portfolio.load_portfolio()

                chain = Chain()
                jobs = chain.extract_jobs(data)

                if not jobs:
                    st.info("ℹ️ No jobs found in the provided link.")
                else:
                    for i, job in enumerate(jobs):
                        skills = job.get("skills", [])
                        links = portfolio.query_links(skills)
                        email = chain.write_mail(job, links)

                        with st.expander(
                            f"📨 Generated Cold Email {i + 1}", expanded=True
                        ):
                            st.code(email, language="markdown")

        except Exception as e:
            st.error(f"❌ Error: {e}")
