import unicodedata
import re
import pandas as pd

class LyricsProcessor:
	lang_map = {
		'en': 'english', 'fr': 'french', 'de': 'german', 'pt': 'portuguese', 'es': 'spanish', 'zh': 'chinese',
		'ru': 'russian', 'it': 'italian', 'ja': 'japanese', 'ro': 'romanian', 'nl': 'dutch', 'pl': 'polish',
		'fi': 'finnish', 'ko': 'korean', 'ar': 'arabic', 'sv': 'swedish', 'tr': 'turkish', 'da': 'danish',
		'cs': 'czech', 'no': 'norwegian', 'is': 'icelandic', 'fil': 'filipino', 'bg': 'bulgarian', 'hr': 'croatian',
		'fa': 'persian', 'vi': 'vietnamese', 'he': 'hebrew', 'ga': 'irish', 'sk': 'slovak', 'hu': 'hungarian',
		'la': 'latin', 'id': 'indonesian', 'hi': 'hindi', 'mk': 'macedonian', 'sl': 'slovenian', 'sr': 'serbian',
		'ne': 'nepali', 'lt': 'lithuanian', 'el': 'greek', 'lv': 'latvian', 'sq': 'albanian', 'et': 'estonian',
		'af': 'afrikaans', 'ca': 'catalan', 'ku': 'kurdish', 'kk': 'kazakh', 'si': 'sinhala', 'bn': 'bengali',
		'ka': 'georgian', 'az': 'azerbaijani', 'ms': 'malay', 'eo': 'esperanto', 'th': 'thai', 'ta': 'tamil',
		'cy': 'welsh', 'mn': 'mongolian', 'eu': 'basque', 'sw': 'swahili', 'gl': 'galician', 'pa': 'punjabi',
		'gd': 'scots gaelic', 'yi': 'yiddish', 'fy': 'frisian', 'bs': 'bosnian', 'be': 'belarusian', 'uk': 'ukrainian',
		'hy': 'armenian', 'mt': 'maltese', 'ceb': 'cebuano', 'lb': 'luxembourgish', 'my': 'burmese', 'kn': 'kannada',
		'ur': 'urdu', 'te': 'telugu', 'am': 'amharic', 'ml': 'malayalam', 'km': 'khmer', 'mr': 'marathi',
		'ky': 'kyrgyz', 'ps': 'pashto', 'gu': 'gujarati', 'mg': 'malagasy', 'tg': 'tajik', 'uz': 'uzbek'
	}

	def __init__(self, language='english', keep_accents=False):
		self.language = self.lang_map.get(language, language) if language is not None else 'english'
		self.keep_accents = keep_accents
		self._setup_nlp()

	def _setup_nlp(self):
		try:
			import nltk
			from nltk.corpus import stopwords
			nltk.data.find('corpora/stopwords')
		except LookupError:
			import nltk
			nltk.download('stopwords', quiet=True)
		from nltk.stem.snowball import SnowballStemmer
		from nltk.tokenize import TweetTokenizer
		# Try to get stopwords for the requested language, fallback to English, then empty set
		try:
			self.stopword_set = set(stopwords.words(self.language))
		except (OSError, LookupError, TypeError):
			try:
				self.stopword_set = set(stopwords.words('english'))
			except Exception:
				self.stopword_set = set()
		try:
			self.stemmer = SnowballStemmer(self.language)
		except ValueError:
			self.stemmer = SnowballStemmer('english')
		self.tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

	def strip_accents(self, text):
		text = unicodedata.normalize('NFD', text)
		return ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')

	def clean_text(self, text):
		if not isinstance(text, str):
			return ''
		text = unicodedata.normalize('NFKC', text)
		text = text.lower()
		# Remove URLs and handles
		text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
		text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
		if not self.keep_accents:
			text = self.strip_accents(text)
		text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
		text = re.sub(r"\s+", " ", text).strip()
		return text

	def tokenize(self, text):
		tokens = self.tokenizer.tokenize(text)
		tokens = [t for t in tokens if re.match(r'^[\w]+$', t, flags=re.UNICODE)]
		tokens = [t for t in tokens if t not in self.stopword_set]
		tokens = [self.stemmer.stem(t) for t in tokens]
		tokens = [t for t in tokens if t not in self.stopword_set]
		return tokens

	def process_dataframe(self, df, lyrics_col='lyrics'):
		cleaned = []
		token_counts = []
		for txt in df[lyrics_col].astype(str):
			c = self.clean_text(txt)
			toks = self.tokenize(c)
			cleaned.append(' '.join(toks))
			token_counts.append(len(toks))
		df_out = df.copy()
		df_out['clean_text'] = cleaned
		df_out['token_count'] = token_counts
		return df_out
