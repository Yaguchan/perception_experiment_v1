import os
import time
import random
import datetime
import numpy as np
import soundfile as sf
import sounddevice as sd

WAVDIR = 'wav'
OUTDIR = ''

# メッセージ
def seed_message():
    print()
    print('*                   SEEDの値を設定してください. ex) 0, 1, 42... など')
    print('*                   続きからの場合は, 【同じ】SEEDの値を使用してください.')
    print('> ', end='')

def data_message():
    print()
    print('*                   データを選択してください.（1〜4）')
    print('*                   通常, 1 -> 2 -> 3 -> 4 の順で選択してください.')
    print('> ', end='')

def data_err_message():
    print()
    print('*                   1〜4 の中から選択してください.')
    print('*                   データを選択してください.（1〜4）')
    print('> ', end='')

def confirm_message():
    print()
    print('*                   音声を以下のように連続して流します.')
    print('*                   A -> B -> A -> B => A.')
    print('*                   -> と => のどちらが早いか聞き比べてください.')
    print('*                   確認ができたら,【0】を入力してください.')
    print('> ', end='')

def confirm_err_message():
    print()
    print('*                   【0】が入力されていません.')
    print('*                   確認ができたら,【0】を入力してください.')
    print('> ', end='')

def judgement_message():
    print()
    print('*                   ->の音声の発話タイミングが早ければ,【1】を入力')
    print('*                   =>の音声の発話タイミングが早ければ,【2】を入力')
    print('*                   もう一度再生したければ,【3】を入力')
    print('> ', end='')

def play_sound(path):
    data, fs = sf.read(path)
    sd.play(data, fs)
    sd.wait()


def main():
    
    # first：音声1, second：音声2
    first = [100, 200, 400, 800, 1600]
    second = [[50, 59, 71, 84, 119, 141, 168, 200], [113, 130, 150, 173, 231, 266, 307, 354], [261, 291, 323, 360, 445, 495, 550, 612], \
              [615, 657, 702, 749, 854, 912, 974, 1040], [1231, 1314, 1403, 1498, 1708, 1824, 1948, 2080]]
    
    # SEEDの設定
    seed_message()
    SEED = input()
    random.seed(SEED)
    
    # データの選択
    data_message()
    while True:
        ID = input()
        if ID in ['1', '2', '3', '4']: break
        data_err_message()
    ID = int(ID)

    # 得られた実験結果の保存場所
    output_path = os.path.join(OUTDIR, f'output_{SEED}.txt')
    log_path = os.path.join(OUTDIR, f'log_{SEED}.txt')  
    
    # 調査するデータについて
    data = []
    result = {}
    for i in range(len(first)):
        for y in second[i]:
            data.append((first[i], y))
            result[f'{first[i]}_{y}'] = -1
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            datalist = f.readlines()
        for x in datalist:
            key, val = x.split(' ')
            key = key.replace(':', '')
            result[str(key)] = int(val)
    
    # データのシャッフル
    random.shuffle(data)
    data = data[(ID-1)*10: ID*10]
    
    # DATAID をログに保存
    with open(log_path, 'a') as f:
        f.write(f'DATA:{ID}\n')

    # 聴取実験
    for i in range(len(data)):
        x, y = data[i]
        print()
        print('**************************************************************************************************')
        print(f'*                   STEP【{i+1}/{len(data)}】')     
        path = os.path.join(WAVDIR, f'{x}_{y}.wav')

        # 確認
        confirm_message()        
        while True:
            z = input()
            if z == '0': break
            confirm_err_message()
        
        # 実行
        repeat = 0
        time_start = time.time()
        play_sound(path)
        judgement_message()
        while True:
            z = input()
            if z == '1' or z == '2':
                if x < y:
                    if z == '1':
                        result[f'{x}_{y}'] = 0
                    else:
                        result[f'{x}_{y}'] = 1
                else:
                    if z == '1':
                        result[f'{x}_{y}'] = 1
                    else:
                        result[f'{x}_{y}'] = 0
                break
            elif z == '3':
                repeat += 1
                play_sound(path)
                judgement_message()
            else:
                judgement_message()
        time_end = time.time()
        output = result[f'{x}_{y}']
    
        # 出力を保存
        # 結果
        with open(output_path, 'w') as f:
            for key in result.keys():
                f.write(f'{key}: {result[key]}\n')
        # log
        with open(log_path, 'a') as f:
            f.write(f'result:{output}, timing:{x}_{y}, time:{int(time_end-time_start)}[s], repeat:{repeat}\n')


if __name__ == '__main__':
    main()