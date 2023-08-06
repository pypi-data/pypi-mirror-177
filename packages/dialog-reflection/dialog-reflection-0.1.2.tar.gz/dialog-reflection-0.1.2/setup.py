# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialog_reflection', 'dialog_reflection.lang', 'dialog_reflection.lang.ja']

package_data = \
{'': ['*']}

install_requires = \
['katsuyo-text==0.1.2', 'spacy>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'dialog-reflection',
    'version': '0.1.2',
    'description': 'A library for dialog systems that attempt to respond to messages as Reflective Listening.',
    'long_description': '# Dialog Reflection\n\nA library for dialog systems that attempt to respond to messages as Reflective Listening.\n\n## Demo\n\nNeed `git` and `poetry` to run this demo.\n\n```console\n$ git clone git@github.com:sadahry/dialog-reflection.git\n$ cd dialog-reflection\n$ poetry install\n$ poetry run python examples/interactive_ja.py\n```\n\n## Install\n\nNeed `python` >= `3.10`\n\n```console\n$ pip install dialog-reflection\n```\n\n## How to Use (Japanese)\n\nSpaCyの日本語モデルのインストールが必要  \n* `ja_ginza==5.1.2` でテスト済\n* 他モデルの利用は可能だが推奨しない\n  * 係り受けや形態素解析によって不整合があるため利用前にテストを推奨\n\n```console\n$ pip install ja_ginza==5.1.2\n```\n\n実行例\n\n```python\nfrom dialog_reflection.lang.ja.reflector import JaSpacyReflector\n\n\nrefactor = JaSpacyReflector(model="ja_ginza")\n\nmessage = "今日は旅行へ行った"\nreflection_text = refactor.reflect(message)\n\nprint(reflection_text)\n# => 旅行へ行ったんですね。\n```\n\nBuilderを使う例\n\n```python\nfrom dialog_reflection.lang.ja.reflection_text_builder import (\n    JaSpacyPlainReflectionTextBuilder,\n)\nimport spacy\n\n\nnlp = spacy.load("ja_ginza")\nbuilder = JaSpacyPlainReflectionTextBuilder()\n\nmessage = "今日は旅行へ行った"\ndoc = nlp(message)\n# some code...\nreflection_text = builder.build(doc)\n\nprint(reflection_text)\n# => 旅行へ行ったんですね。\n```\n\n### 語尾の調整\n\n`op` を変更することで語尾を調整可能\n\n```python\nfrom dialog_reflection.lang.ja.reflector import JaSpacyReflector\nfrom dialog_reflection.lang.ja.reflection_text_builder import (\n    JaSpacyPlainReflectionTextBuilder,\n)\nfrom dialog_reflection.lang.ja.reflection_text_builder_option import (\n    JaSpacyPlainReflectionTextBuilderOption,\n)\n\n\nrefactor = JaSpacyReflector(\n    model="ja_ginza",\n    builder=JaSpacyPlainReflectionTextBuilder(\n        op=JaSpacyPlainRelflectionTextBuilderOption(\n            fn_last_token_taigen=lambda token: token.text + "なんだね。",\n            fn_last_token_yougen=lambda token: token.lemma_ + "んだね。",\n        )\n    ),\n)\n\nmessage = "今日は旅行へ行った"\nreflection_text = refactor.reflect(message)\n\nprint(reflection_text)\n# => 旅行へ行ったんだね。\n```\n\nその他設定項目は [reflection_text_builder_option.py](https://github.com/sadahry/dialog-reflection/blob/main/dialog_reflection/lang/ja/reflection_text_builder_option.py#L24) を確認してください\n\n### ロジックのカスタマイズ\n\n`JaSpacyPlainReflectionTextBuilder` を override することでロジックをカスタマイズ可能\n\n```python\nfrom dialog_reflection.reflection_cancelled import (\n    ReflectionCancelled,\n)\nfrom dialog_reflection.cancelled_reason import (\n    NoValidSentence,\n)\nfrom dialog_reflection.lang.ja.reflector import JaSpacyReflector\nfrom dialog_reflection.lang.ja.reflection_text_builder import (\n    JaSpacyPlainReflectionTextBuilder,\n)\nimport spacy\n\n\nclass CustomReflectionTextBuilder(JaSpacyPlainReflectionTextBuilder):\n    def extract_tokens(self, doc: spacy.tokens.Doc) -> spacy.tokens.Span:\n        propn_token = next(filter(lambda token: token.pos_ == "PROPN", doc), None)\n        if propn_token is None:\n            raise ReflectionCancelled(reason=NoValidSentence(doc=doc))\n        if propn_token.dep_ in ["compound", "numpound"]:\n            return doc[propn_token.i : propn_token.head.i + 1]\n        return doc[propn_token.i : propn_token.i + 1]\n\n\nrefactor = JaSpacyReflector(\n    model="ja_ginza",\n    builder=CustomReflectionTextBuilder(),\n)\n\n\nmessage = "今日は田中さんと旅行へ行った"\nreflection_text = refactor.reflect(message)\n\nprint(reflection_text)\n# => 田中さんなんですね。\n```\n',
    'author': 'Sadahiro YOSHIKAWA',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
