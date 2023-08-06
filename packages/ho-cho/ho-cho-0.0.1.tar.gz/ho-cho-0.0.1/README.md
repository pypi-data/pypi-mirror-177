# Ho-Cho
## Install
<details><summary>Mac</summary>

```shell
# Install MeCab
brew install mecab mecab-ipadic

# Install mecab-ipadic-neologd
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && bin/install-mecab-ipadic-neologd -n -a -y
    && cd ..

pip install hocho
```
</details>

<details><summary>Ubuntu</summary>

```shell
# Install MeCab and mecab-ipadic-neologd
apt-get update && apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8

# Install mecab-ipadic-neologd
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && bin/install-mecab-ipadic-neologd -n -a -y
    && cd ..

pip install hocho
```
</details>

<details><summary>Window</summary>

coming soon ...

</details>

## Usage
### 1. cleaning
テキストのクリーニング

[hocho/cleaning.py](https://github.com/gtaiyou24/hocho/blob/main/src/hocho/cleaning.py)

### 2. tokenizing
単語の分割

[hocho/tokenizer/impl/mecab_tokenizer.py](https://github.com/gtaiyou24/hocho/blob/main/src/hocho/tokenizer/impl/mecab_tokenizer.py)

### 3. normalization
単語の正規化

 - 文字種の統一
 - 数字の置き換え
 - 辞書を用いた単語の統一

[hocho/normalization.py](https://github.com/gtaiyou24/hocho/blob/main/src/hocho/normalization.py)

### 4. stopwords
ストップワードの除去

 - 辞書による方法
 - 出現頻度による方法
 - 有名なストップワードを用いた除去方法

[hocho/stopwords.py](https://github.com/gtaiyou24/hocho/blob/main/src/hocho/stopwords.py)

## Development
### How to develop
```shell
git pull origin main

git checkout -b feature/xxxx

git add .
git commit -m "xxx"

git push origin feature/xxx
```

### Run test
```shell
pytest -v tests
```

### Set up
```shell
pip install -e .
```

### Publish to TestPyPI
```shell
# Install dependencies
pip install setuptools wheel twine

# Build
python setup.py sdist bdist_wheel

# Publish to TestPyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### Publish to PyPI
```shell
# Install dependencies
pip install setuptools wheel twine

# Build
python setup.py sdist bdist_wheel

# Publish to PyPI
twine upload dist/*
```