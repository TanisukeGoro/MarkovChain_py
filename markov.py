import MeCab
import os
import random
import re
def Mecab_file():
    f = open("tweet.txt","rb")
    data = f.read().decode('utf-8')
    f.close()

    mt = MeCab.Tagger("-Owakati")

    wordlist = mt.parse(data)
    wordlist = wordlist.rstrip(" \n").split(" ")

    markov = {}
    w = ""

    for x in wordlist:
        if w:
            if w in markov:
                new_list = markov[w]
            else:
                new_list =[]

            new_list.append(x)
            markov[w] = new_list
        w = x

    choice_words = wordlist[0]
    sentence = ""
    count = 0

    while count < 50:
        sentence += choice_words
        choice_words = random.choice(markov[choice_words])
        count += 1

        sentence = sentence.split(" ", 1)[0]
        p = re.compile("[!-/:-@[-`{-~]")
        sus = p.sub("", sentence)

    words = re.sub(re.compile("[!-~]"),"",sus)
    return words




# マルコフ連鎖で生成した文字列を出力
print(Mecab_file())
