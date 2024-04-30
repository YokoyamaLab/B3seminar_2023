# このプログラムについて
このプログラムは**GPUサーバーにあるプログラムではありません**。パノラマ動画を読み込んで処理をするだけのプログラムです。

GPUサーバー上のプログラムは[こちら](https://github.com/igeeeeee/B3project2023_presen)

(TODO: GPUサーバー上のプログラムのリポジトリを横山研のところに移動する)


# 使い方

### Python version
```
python3 --version
```
Python 3.10.12

## 初回のみ(Linux or Mac 環境を想定)

### git clone から仮想環境の作成
git clone 
``` 
git clone https://github.com/YokoyamaLab/B3seminar_2023.git
```
```
cd  B3seminar_2023
```
仮想環境の作成

```
python3 -m venv .venv
```
### 仮想環境のアクティベート
```
source .venv/bin/activate
```

### ライブラリのインストール
```
pip install -r requirements.txt
```


## 2回目以降
2回目以降は仮想環境のアクティベートだけでよい
```
source .venv/bin/activate
```

## 実行方法
main.pyがあるディレクトリに
Videos/soccer.mov(パノラマ動画)があるようにする。


実行
```
python3 main.py
```


## 実行時のエラーについて
wsl環境で出たエラーは[fixbug_log.md](https://github.com/YokoyamaLab/B3seminar_2023/blob/main/fixbug_log.md)にまとめた
