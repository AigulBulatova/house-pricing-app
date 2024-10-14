import streamlit as st


pred_page = st.Page(
    page='views/prediction.py',
    title='Prediction',
    default=True
)

info_page = st.Page(
    page='views/info.py',
    title='Analysis'
)

pg = st.navigation(pages=[pred_page, info_page])
pg.run()


