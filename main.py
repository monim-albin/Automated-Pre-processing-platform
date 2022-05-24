import streamlit as st
import functions as alt_fun
import nltk
nltk.download('punkt')
import copy

prepro = alt_fun.Preprocessing()
prepro.emoji_loca = "./emojis.csv"
prepro.dataset_try = "./hotel-reviews.txt"
prepro.emoji_list()

# <!------------------------------------------->
header_title = st.container()
content_title = st.container()

with header_title:
    st.title("Automated Arabic Pre-processing")
    st.write("Arabic NLP projects suffer from the lack of "
            "scientific research/scripting resources along with"
            " linguistic complexity. To leverage the load carried on"
            " their shoulder, I have decided to build an automated "
            "tool/platform to pre-process arabic records.")
    st.markdown(prepro.download(
                        prepro.read_file_return(prepro.dataset_try),
                        "DOWNLOAD THE ARABIC HOTEL REVIEW DATASET FROM HERE FOR DEMO",
                        "file/Text", prepro.dataset_try, "Text")
                ,unsafe_allow_html=True)
    file = st.file_uploader("Upload your CSV/TXT file here:", type=["csv","txt"])
if not file is None:
    with st.form(key="form1"):
        with header_title:
            st.subheader("Data Before Processing")
            prepro.read_file(file)
            prepro.ff = copy.deepcopy(prepro.df)
            st.dataframe(data=prepro.ff.head())

        with st.sidebar:
            # Select your column to apply the pre-processing on
            st.header("Select your column with arabic text to pre-process: ")
            prepro.col_selected = st.selectbox("Columns :", options=prepro.col_names_string_type())
            # side bar components

            # New Columns/Features to add
            st.header("New Columns/Features to add: ")
            word_count = st.checkbox("Word Count")
            char_count = st.checkbox("character Count")
            avg_char_per_word = st.checkbox("Average Character per Word")
            stop_word = st.checkbox("Stop Word Count")
            emoji_count = st.checkbox("Emoji Count")

            # <--------------- fitlers ----------------->
            st.header("Filtering the arabic text column selected to pre-process: ")
            remove_english = st.checkbox("Remove records with English")
            remove_url = st.checkbox("Remove URLs")
            remove_emoji = st.checkbox("Remove emoji")
            translate_emoji = st.checkbox("Translate emojis into their arabic counterpart word")
            remove_punc = st.checkbox("Remove punctuations")
            remove_extra_whitespace = st.checkbox("Remove extra whitespace")
            remove_stopword = st.checkbox("Remove arabic stop words")
            remove_number = st.checkbox("Remove numbers")
            remove_tashkeel = st.checkbox("Remove arabic Tashkeel")
            stem = st.checkbox("Replace words with their stem")
            file_type_save = st.selectbox("Export Format:", options=['Text', 'CSV'])
            btn = st.form_submit_button("Apply")

            # btn_save = st.form_submit_button("Save")


        with content_title:
            if btn:
                prepro.add_features_selected([word_count, char_count, avg_char_per_word,
                                              stop_word, emoji_count])
                prepro.apply_filters_selected([remove_english, remove_url, remove_emoji,
                                               translate_emoji, remove_punc, remove_extra_whitespace,
                                               remove_stopword, remove_number, remove_tashkeel,
                                               stem])
                st.subheader("Data after adding the additional desired features")
                st.dataframe(data=prepro.df)
                st.markdown(prepro.download(prepro.df, "Download Your New Data", file.type, "new_data."+file_type_save, file_type_save), unsafe_allow_html=True)

