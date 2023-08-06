# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katsuyo_text']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'katsuyo-text',
    'version': '0.1.2',
    'description': 'A Japanese conjugation form converter',
    'long_description': '# Katsuyo Text\n\n日本語の活用変換器  \nA Japanese conjugation form converter\n\n## Motivation\n\n日本語文法における活用変形をロジックに落とし込めるかの試み\n\n## ⚠CAUTION\n\n現状、挙動は不安定です。必要に応じてアップデートしたいです。\n\n## How to Use\n### 追加\n\n```python\nfrom katsuyo_text.katsuyo_text_helper import (\n    Hitei,\n    KakoKanryo,\n    DanteiTeinei,\n)\nfrom katsuyo_text.spacy_katsuyo_text_detector import SpacyKatsuyoTextSourceDetector\nimport spacy\n\n\nnlp = spacy.load("ja_ginza")\nsrc_detector = SpacyKatsuyoTextSourceDetector()\n\n\ndoc = nlp("今日は旅行に行く")\nsent = next(doc.sents)\nkatsuyo_text = src_detector.try_detect(sent[-1])\n\nkatsuyo_text\n# => KatsuyoText(gokan=\'行\', katsuyo=GodanKatsuyo(renyo_ta=\'っ\', mizen_u=\'こ\', meirei=\'け\', katei=\'け\', rentai=\'く\', shushi=\'く\', renyo=\'き\', mizen=\'か\'))\n\nprint(katsuyo_text + Hitei())\n# => 行かない\nprint(katsuyo_text + Hitei() + KakoKanryo())\n# => 行かなかった\nprint(katsuyo_text + Hitei() + KakoKanryo() + DanteiTeinei())\n# => 行かなかったです\n```\n\n### 変換\n\n```python\nfrom katsuyo_text.katsuyo_text_helper import (\n    Teinei,\n    Dantei,\n    DanteiTeinei,\n)\nfrom katsuyo_text.spacy_sentence_converter import SpacySentenceConverter\nimport spacy\n\n\nnlp = spacy.load("ja_ginza")\nconverter = SpacySentenceConverter(\n    conversions_dict={\n        Teinei(): None,\n        DanteiTeinei(): Dantei(),\n    }\n)\n\n\ndoc = nlp("今日は旅行に行きました")\nsent = next(doc.sents)\nprint(converter.convert(sent))\n# => 今日は旅行に行った\n\ndoc = nlp("今日は最高の日でした")\nsent = next(doc.sents)\nprint(converter.convert(sent))\n# => 今日は最高の日だった\n```\n\n### カスタマイズ\n\n文法的に成立しない活用変形を `bridge` で実現している\n```python\nfrom katsuyo_text.katsuyo_text import TaigenText, JODOUSHI_NAI\n\nTaigenText("大丈夫") + JODOUSHI_NAI\n# error => katsuyo_text.katsuyo_text.KatsuyoTextError: Unsupported katsuyo_text in merge of <class \'katsuyo_text.katsuyo_text.Nai\'>: 大丈夫 type: <class \'katsuyo_text.katsuyo_text.TaigenText\'>\n\nfrom katsuyo_text.katsuyo_text_helper import Hitei\nTaigenText("大丈夫") + Hitei()\n# => KatsuyoText(gokan=\'大丈夫ではな\', katsuyo=KeiyoushiKatsuyo(katei=\'けれ\', rentai=\'い\', shushi=\'い\', renyo_ta=\'かっ\', renyo=\'く\', mizen=\'かろ\'))\n\nTaigenText("大丈夫") + Hitei() == Hitei().bridge(TaigenText("大丈夫"))\n# => True\n```\n\n`bridge` はカスタマイズ可能\n```python\nfrom katsuyo_text.katsuyo_text import KatsuyoText, TaigenText, KAKUJOSHI_GA\nfrom katsuyo_text.katsuyo import KEIYOUSHI\n\nnai = KatsuyoText(gokan="な", katsuyo=KEIYOUSHI)\ncustom_hitei = Hitei(bridge=lambda src: src + KAKUJOSHI_GA + nai)\n\nTaigenText("耐性") + custom_hitei\n# => KatsuyoText(gokan=\'耐性がな\', katsuyo=KeiyoushiKatsuyo(katei=\'けれ\', rentai=\'い\', shushi=\'い\', renyo_ta=\'かっ\', renyo=\'く\', mizen=\'かろ\'))\n```\n\n`IKatsuyoTextHelper` で独自の活用変形を実装可能\n```python\nfrom typing import Optional\nfrom katsuyo_text.katsuyo_text_helper import IKatsuyoTextHelper\nfrom katsuyo_text.katsuyo_text import (\n    TaigenText,\n    KatsuyoTextError,\n    IKatsuyoTextSource,\n    SetsuzokujoshiText,\n    KURU,\n    SETSUZOKUJOSHI_KARA,\n    JUNTAIJOSHI_NO,\n    JODOUSHI_DA_DANTEI,\n)\n\n\nclass JunsetsuKakutei(IKatsuyoTextHelper[SetsuzokujoshiText]):\n    def try_merge(self, pre: IKatsuyoTextSource) -> Optional[SetsuzokujoshiText]:\n        try:\n            pre + SETSUZOKUJOSHI_KARA\n        except KatsuyoTextError as e:\n            # Handle error\n            return None\n\n\nKURU\n# => KatsuyoText(gokan=\'\', katsuyo=KaGyoHenkakuKatsuyo(meirei=\'こい\', katei=\'くれ\', rentai=\'くる\', shushi=\'くる\', renyo=\'き\', mizen=\'こ\'))\nKURU + JunsetsuKakutei()\n# => SetsuzokujoshiText(gokan=\'くるから\', katsuyo=None)\n\ncustom_junsetsu_kakutei = JunsetsuKakutei(bridge=lambda src: src + JODOUSHI_DA_DANTEI + SETSUZOKUJOSHI_KARA)\n\nTaigenText("症状") + JunsetsuKakutei()\n# error => katsuyo_text.katsuyo_text.KatsuyoTextError: Unsupported katsuyo_text in merge of <class \'__main__.JunsetsuKakutei\'>: 症状 type: <class \'katsuyo_text.katsuyo_text.TaigenText\'> katsuyo: <class \'NoneType\'>\nTaigenText("症状") + custom_junsetsu_kakutei\n# => SetsuzokujoshiText(gokan=\'症状だから\', katsuyo=None)\n```\n',
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
