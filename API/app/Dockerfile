# ベースイメージ
FROM python:3.8

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY . /app

# uWSGIサーバーを起動
CMD ["uwsgi", "uwsgi.ini"]