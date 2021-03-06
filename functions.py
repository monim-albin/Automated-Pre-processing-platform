import base64
import emoji
import arabicstopwords.arabicstopwords as stp
from tashaphyne.stemming import ArabicLightStemmer
from textblob import TextBlob
import re
import pyarabic.araby as araby
import pandas as pd
import streamlit as st
from io import StringIO

class Preprocessing:
    def __init__(self):
    # variables
        self.df = None
        self.ff = None
        self.emoji_loca = None
        self.dataset_try = None
        self.col_selected = None
        self.stop_word_comp = {"،","آض","آمينَ","آه","آهاً","آي","أ","أب","أجل","أجمع","أخ","أخذ","أصبح","أضحى","أقبل","أقل","أكثر","ألا","أم","أما","أمامك","أمامكَ","أمسى","أمّا","أن","أنا","أنت","أنتم","أنتما","أنتن","أنتِ","أنشأ","أنّى","أو","أوشك","أولئك","أولئكم","أولاء","أولالك","أوّهْ","أي","أيا","أين","أينما","أيّ","أَنَّ","أََيُّ","أُفٍّ","إذ","إذا","إذاً","إذما","إذن","إلى","إليكم","إليكما","إليكنّ","إليكَ","إلَيْكَ","إلّا","إمّا","إن","إنّما","إي","إياك","إياكم","إياكما","إياكن","إيانا","إياه","إياها","إياهم","إياهما","إياهن","إياي","إيهٍ","إِنَّ","ا","ابتدأ","اثر","اجل","احد","اخرى","اخلولق","اذا","اربعة","ارتدّ","استحال","اطار","اعادة","اعلنت","اف","اكثر","اكد","الألاء","الألى","الا","الاخيرة","الان","الاول","الاولى","التى","التي","الثاني","الثانية","الذاتي","الذى","الذي","الذين","السابق","الف","اللائي","اللاتي","اللتان","اللتيا","اللتين","اللذان","اللذين","اللواتي","الماضي","المقبل","الوقت","الى","اليوم","اما","امام","امس","ان","انبرى","انقلب","انه","انها","او","اول","اي","ايار","ايام","ايضا","ب","بات","باسم","بان","بخٍ","برس","بسبب","بسّ","بشكل","بضع","بطآن","بعد","بعض","بك","بكم","بكما","بكن","بل","بلى","بما","بماذا","بمن","بن","بنا","به","بها","بي","بيد","بين","بَسْ","بَلْهَ","بِئْسَ","تانِ","تانِك","تبدّل","تجاه","تحوّل","تلقاء","تلك","تلكم","تلكما","تم","تينك","تَيْنِ","تِه","تِي","ثلاثة","ثم","ثمّ","ثمّة","ثُمَّ","جعل","جلل","جميع","جير","حار","حاشا","حاليا","حاي","حتى","حرى","حسب","حم","حوالى","حول","حيث","حيثما","حين","حيَّ","حَبَّذَا","حَتَّى","حَذارِ","خلا","خلال","دون","دونك","ذا","ذات","ذاك","ذانك","ذانِ","ذلك","ذلكم","ذلكما","ذلكن","ذو","ذوا","ذواتا","ذواتي","ذيت","ذينك","ذَيْنِ","ذِه","ذِي","راح","رجع","رويدك","ريث","رُبَّ","زيارة","سبحان","سرعان","سنة","سنوات","سوف","سوى","سَاءَ","سَاءَمَا","شبه","شخصا","شرع","شَتَّانَ","صار","صباح","صفر","صهٍ","صهْ","ضد","ضمن","طاق","طالما","طفق","طَق","ظلّ","عاد","عام","عاما","عامة","عدا","عدة","عدد","عدم","عسى","عشر","عشرة","علق","على","عليك","عليه","عليها","علًّ","عن","عند","عندما","عوض","عين","عَدَسْ","عَمَّا","غدا","غير","ـ","ف","فان","فلان","فو","فى","في","فيم","فيما","فيه","فيها","قال","قام","قبل","قد","قطّ","قلما","قوة","كأنّما","كأين","كأيّ","كأيّن","كاد","كان","كانت","كذا","كذلك","كرب","كل","كلا","كلاهما","كلتا","كلم","كليكما","كليهما","كلّما","كلَّا","كم","كما","كي","كيت","كيف","كيفما","كَأَنَّ","كِخ","لئن","لا","لات","لاسيما","لدن","لدى","لعمر","لقاء","لك","لكم","لكما","لكن","لكنَّما","لكي","لكيلا","للامم","لم","لما","لمّا","لن","لنا","له","لها","لو","لوكالة","لولا","لوما","لي","لَسْتَ","لَسْتُ","لَسْتُم","لَسْتُمَا","لَسْتُنَّ","لَسْتِ","لَسْنَ","لَعَلَّ","لَكِنَّ","لَيْتَ","لَيْسَ","لَيْسَا","لَيْسَتَا","لَيْسَتْ","لَيْسُوا","لَِسْنَا","ما","ماانفك","مابرح","مادام","ماذا","مازال","مافتئ","مايو","متى","مثل","مذ","مساء","مع","معاذ","مقابل","مكانكم","مكانكما","مكانكنّ","مكانَك","مليار","مليون","مما","ممن","من","منذ","منها","مه","مهما","مَنْ","مِن","نحن","نحو","نعم","نفس","نفسه","نهاية","نَخْ","نِعِمّا","نِعْمَ","ها","هاؤم","هاكَ","هاهنا","هبّ","هذا","هذه","هكذا","هل","هلمَّ","هلّا","هم","هما","هن","هنا","هناك","هنالك","هو","هي","هيا","هيت","هيّا","هَؤلاء","هَاتانِ","هَاتَيْنِ","هَاتِه","هَاتِي","هَجْ","هَذا","هَذانِ","هَذَيْنِ","هَذِه","هَذِي","هَيْهَاتَ","و","و6","وا","واحد","واضاف","واضافت","واكد","وان","واهاً","واوضح","وراءَك","وفي","وقال","وقالت","وقد","وقف","وكان","وكانت","ولا","ولم","ومن","مَن","وهو","وهي","ويكأنّ","وَيْ","وُشْكَانََ","يكون","يمكن","يوم","ّأيّان"}
        self.ArListem = ArabicLightStemmer()
        self.emojis_ar = {}
        self.emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)

    def download(self, dff, text_to_view, type, location, save_type):
        if save_type == "Text":
            csv = dff.to_csv(index=False, sep='\t')
        else:
            csv = dff.to_csv(index=False, sep=',')

        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:{type};base64,{b64}" download="{location}">{text_to_view}</a>'
        return href

    def read_file(self, file):
        sep = "\t" if file.type == "text/plain" else ","
        bytes_data = file.read()
        try:
            encoding = 'UTF-16'
            s = str(bytes_data, encoding)
        except:
            encoding = 'UTF-8'
            s = str(bytes_data, encoding)

        data = StringIO(s)
        s = pd.read_csv(data, delimiter=sep)
        self.df = s

    @st.cache
    def read_file_return(self, file):
        s = pd.read_csv(file, delimiter="\t", encoding="UTF-8")
        return s


    # <--------- Adding new features ------------>
    # return string columns
    def col_names_string_type(self):
        cols = self.df.select_dtypes(include=['object']).columns
        string_cols = [c for c in cols]
        return string_cols

    # Return average character per word
    def avg_word(self, sentence):
        words = sentence.split()
        if len(words) == 0:
            return 0
        return (sum(len(word) for word in words)/len(words))

    # Return emoji count
    def emoji_counter(self, sentence):
        return emoji.emoji_count(sentence)

    # Add all new selected features
    # @st.cache
    def add_features_selected (self, bool_selected_additional_features):
        if bool_selected_additional_features[0] : self.df['word_count'] = self.df[self.col_selected].apply(lambda x: len(str(x).split(" ")))
        if bool_selected_additional_features[1] : self.df['char_count'] = self.df[self.col_selected].str.len()  ## this also includes spaces
        if bool_selected_additional_features[2] : self.df['avg_char_per_word'] = self.df[self.col_selected].apply(lambda x: self.avg_word(x))
        if bool_selected_additional_features[3] : self.df['stopwords'] = self.df[self.col_selected].apply(lambda x: len([x for x in x.split() if stp.is_stop(x)]))
        if bool_selected_additional_features[4] : self.df['emoji_count'] = self.df[self.col_selected].apply(lambda x: self.emoji_counter(x))
        # df = df.sort_values(by='word_count', ascending=[0])


    # <--------- Pre-processing ------------>
    def stemming(self, word):
        self.ArListem.light_stem(word.group())
        return self.ArListem.get_root()

    def stem(self, text):
        text = re.sub(r"[\u0600-\u06FF]+", self.stemming, text)
        return text

    # remove tashkal
    def normalizeArabic(self, text):
        text = text.strip()
        text = re.sub(re.compile(r"[إأٱآا]"), "ا", text)
        text = re.sub(re.compile(r"ى"), "ي", text)
        text = re.sub(re.compile(r"ؤ"), "ء", text)
        text = re.sub(re.compile(r"ئ"), "ء", text)
        text = re.sub(re.compile(r"ة"), "ه", text)
        noise = re.compile(""" ّ    | # Tashdid
                                 َ    | # Fatha
                                 ً    | # Tanwin Fath
                                 ُ    | # Damma
                                 ٌ    | # Tanwin Damm
                                 ِ    | # Kasra
                                 ٍ    | # Tanwin Kasr
                                 ْ    | # Sukun
                                 ـ     # Tatwil/Kashida
                             """, re.VERBOSE)
        text = re.sub(noise, '', text)
        text = re.sub(re.compile(r'(.)\1+'), r"\1\1", text)  # Remove longation
        return araby.strip_diacritics(text)


    def remove_stop_words(self, text):
        zen = TextBlob(text)
        words = zen.split()
        return " ".join([w for w in words if not stp.is_stop(w) and not w in self.stop_word_comp and len(w) >= 2])

    # Read all emojis from files
    # @st.cache
    def emoji_list(self):
        with open(self.emoji_loca, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n').split(';')
                self.emojis_ar[line[0].strip()]= line[1].strip()

    def remove_emoji(self, text):
        text = self.emoji_pattern.sub(r'', text)
        return text

    def translate_emojis(self, word):
        return self.emojis_ar.get(word.group(), "None").replace(':','').replace('_',' ')

    def emoji_unicode_translation(self, text):
        text = self.emoji_pattern.sub(self.translate_emojis, text)
        return text

    def translate_emoji(self, text):
        text = self.emoji_unicode_translation(text)
        return text

    def remove_urls(self, text):
        text = re.sub('http\S+\s*', '', text)  # remove URLs
        return text

    def remove_number(self, text):
        text = re.sub("\d+", " ", text)
        return text

    def remove_row_with_English(self):
        filter = self.df[self.col_selected].str.contains('[A-Za-z]+')
        text =self.df[~filter] # remove English records
        return text

    def remove_punc(self, text):
        text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~“”"""), ' ', text)
        return text

    def remove_whitespace(self, text):
        text = re.sub('\s+', ' ', text)
        return text

    # Apply the selected filters
    # @st.cache
    def apply_filters_selected(self, bool_selected_filters):
        if bool_selected_filters[0]:
            self.remove_row_with_English()
        if bool_selected_filters[1]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_urls(x))
        if bool_selected_filters[2]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_emoji(x))
        if bool_selected_filters[3]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.translate_emoji(x))
        if bool_selected_filters[4]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_punc(x))
        if bool_selected_filters[5]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_whitespace(x))
        if bool_selected_filters[6]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_stop_words(x))
        if bool_selected_filters[7]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.remove_number(x))
        if bool_selected_filters[8]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.normalizeArabic(x))
        if bool_selected_filters[9]: self.df[self.col_selected] = self.df[self.col_selected].apply(
            lambda x: self.stem(x))
