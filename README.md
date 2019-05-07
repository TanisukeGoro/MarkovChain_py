# マルコフ連鎖文章生成プログラム  
入力した文字列を元に、形態要素解析を行いマルコフ連鎖を用いて文章を生成します。
https://github.com/TanisukeGoro/MarkovChain_py

## GETTING STATED
実際に実行するまでを説明します。
### インストールと実行
【実行環境】
varsion : Python3.7
installer : Homebrew, pip

#### 1.インストール・準備  
githubのリポジトリからzipファイルでダウンロードして展開するか、任意のディレクトリで以下のコマンドを実行します。  
```
$ git clone https://github.com/TanisukeGoro/MarkovChain_py.git  
```
取得したテキストの形態要素解析からのマルコフ連鎖を行っているので、形態要素解析用のライブラリをインストールする必要があります。  
```  
$ brew install mecab
$ brew install mecab-ipadic
$ pip install mecab-python3
```
これで大丈夫なはずです。エラーが生じた場合は適宜提案されたコマンドを実行すれば大丈夫です。

#### 2.getTweetsById.pyの実行  
実行すると取得したいアカウントのIDを聞かれるので入力します。  
```
$ python getTweetsById.py
input Twitter ID without @ mark >> ここにIDを入力
```

#### 3.markov.pyの実行  
これで取得したツイートを元にした文章が生成されるはずです。
```
$ python markov.py

// 今日俺展最終回！。福岡写真載せます
// よろしくお願いしてます。大阪でみんな名残惜しくてないの
// 令和という新たな元号の方は初日です。今日は違う雰囲気ですね
```
