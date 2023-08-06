import re

from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    replaced_text = '\n'.join(s.strip() for s in text.splitlines() if s != '')
    replaced_text = replaced_text.lower()
    replaced_text = re.sub(r'[【】]', ' ', replaced_text)       # 【】の除去
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)     # （）の除去
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)   # ［］の除去
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)      # メンションの除去
    replaced_text = re.sub(r'[■]', ' ', replaced_text)          # ■ の除去
    replaced_text = re.sub(r'[▼]', ' ', replaced_text)          # ▼ の除去
    replaced_text = re.sub(r'[=]', ' ', replaced_text)          # = の除去
    replaced_text = re.sub(r'[:]', ' ', replaced_text)          # : の除去
    replaced_text = re.sub(r'[/]', ' ', replaced_text)          # / の除去
    replaced_text = re.sub(r'[:]', ' ', replaced_text)          # : の除去
    replaced_text = re.sub(r'[※]', ' ', replaced_text)          # ※ の除去
    replaced_text = re.sub(r'[！]', ' ', replaced_text)         # ！ の除去
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)  # URLの除去
    replaced_text = re.sub(r'　', ' ', replaced_text)  # 全角空白の除去
    return replaced_text


def clean_html_tags(html_text: str) -> str:
    """HTMLタグを取り除き、テキストのみを抽出."""
    soup = BeautifulSoup(html_text, 'html.parser')
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text


def clean_html_and_js_tags(html_text: str) -> str:
    """HTMLタグとJSタグを取り除き、テキストのみを抽出."""
    soup = BeautifulSoup(html_text, 'html.parser')
    [x.extract() for x in soup.findAll(['script', 'style'])]
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text


def clean_url(html_text: str) -> str:
    """テキスト指定でテキスト中のURLを取り除く."""
    return re.sub(r'http\S+', '', html_text)


def clean_code(html_text: str) -> str:
    """テキスト指定でテキスト中のコード(preタグ)を取り除きます。"""
    soup = BeautifulSoup(html_text, 'html.parser')
    [x.extract() for x in soup.findAll("pre")]
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text
