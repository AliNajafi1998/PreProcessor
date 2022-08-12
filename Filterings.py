import emoji
import string
from urlextract import URLExtract
import urllib
import re


class EmojiHandler:
    def __call__(self, text: str) -> str:
        return emoji.demojize(text)


class EmailHandler:
    def __init__(self) -> None:
        self.pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'

    def __call__(self, text: str, repl: str = ' ') -> str:
        match = re.findall(self.pattern, text)
        for m in match:
            text = text.replace(m, repl).strip()
        return text


class URLHandler:
    def __init__(self) -> None:
        self.url_extractor = URLExtract()

    def __call__(self, text: str, keep: bool = True) -> str:
        urls = list(self.url_extractor.gen_urls(text))
        if keep == True:
            updated_urls = [
                url if 'http' in url else f'https://{url}' for url in urls]
            domains = [urllib.parse.urlparse(
                url_text).netloc for url_text in updated_urls]
            for i in range(len(domains)):
                text = text.replace(urls[i], domains[i])
            return text
        else:
            for i in range(len(urls)):
                text = text.replace(urls[i], ' ').strip()
            return text


class HashTagHandler:
    def camel_case_split(self, text):
        pattern = '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
        matches = re.finditer(pattern, text)
        return " ".join([m.group(0) for m in matches])

    def __call__(self, text: str, keep: bool = True, camel_case_split: bool = True) -> str:
        pattern = "(#([^\s]+))"
        if keep == True and camel_case_split == False:
            return re.sub(pattern, "\\1 \\2", text)
        elif keep == True and camel_case_split == True:
            return re.sub(pattern, lambda x: f"{x.group()} {self.camel_case_split(x.group()[1:])}", text)
        elif keep == False and camel_case_split == True:
            return re.sub(pattern, lambda x: f"{self.camel_case_split(x.group()[1:])}", text)
        else:
            return re.sub(pattern, "\\2", text)


class MentionHandler:
    def __call__(self, text: str, repl: str = None, keep: bool = True) -> str:
        pattern = "(@([^\s]+))"
        if repl:
            return re.sub(pattern, repl, text)
        else:
            if keep == True:
                return re.sub(pattern, "\\1 \\2", text)
            else:
                return re.sub(pattern, "\\2", text)


class PunctuationHandler:
    def __init__(self) -> None:
        self.punct_set = set(string.punctuation + '''…'"`’”“''' + '️')

    def __call__(self, text: str) -> str:
        cleaned_text = ""
        for ch in text:
            if ch not in self.punct_set:
                cleaned_text += ch
        return cleaned_text
