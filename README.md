# bedrock-reel-canvas-test

2024年のre:Inventで発表されたAmazon NovaシリーズのCanvasとReelを使ったデモアプリ

空港のトランジットで寝落ちしないように無理やりコードを書いていたときに作ったやつなので全体的にコードが汚いよ。

## preparation

- Python 3.11.5

```
pip install poetry

poetry install
```

### コード修正

- アプリ起動前に画像出力用S3を修正する
- REGIONは今のところus-east-1のみ

```python
S3_DESTINATION_BUCKET = "FIXME"
REGION = "us-east-1"
REEL_MODEL_ID = "amazon.nova-reel-v1:0"
CANVAS_MODEL_ID = "amazon.nova-canvas-v1:0"
SLEEP_TIME = 30
```

### モデルアクセス有効化

Bedrockコンソールのモデルアクセスから下記モデルを有効化

- Nova Reel
- Nova Canvas

## ローカル起動

```
poetry run streamlit run src/app.py
```

http://localhost:8501　で起動するはず。
