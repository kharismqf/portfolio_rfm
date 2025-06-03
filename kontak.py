import streamlit as st

def link():
    st.title("👋 Hi, I'm Kharisma Qaulam Fadhila")
    
    with st.container():
        st.markdown("""
        <div style='text-align: justify; font-size: 16px;'>
            I’m a detail-oriented Geodetic Engineering graduate with a strong foundation in analytical thinking and problem-solving, 
            currently specializing in marketing data analysis and business insights. I have hands-on experience in customer segmentation, 
            A/B testing, and channel performance analysis to support data-driven decision-making.<br><br>
            Proficient in <b>Power BI</b>, <b>SQL</b>, <b>Excel</b>, and <b>Python</b>, I enjoy building dashboards, processing large datasets, 
            and uncovering actionable insights. I'm known for my accuracy, adaptability, and proactive mindset in fast-paced, 
            data-driven environments.
        </div>
        """, unsafe_allow_html=True)

    st.write("📫 Let's connect!")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("[📧 Email](mailto:qaulamk@gmail.com)", unsafe_allow_html=True)
    with col2:
        st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/kharismaqaulam)", unsafe_allow_html=True)
    with col3:
        st.markdown("[✍️ Medium](https://medium.com/@qaulamk)", unsafe_allow_html=True)
