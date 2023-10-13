# perception_experiment_v1
谷口友紀, 藤江真也, 小坂直敏, 小林哲則, “発話タイミング推定における時間心理尺度の考慮,” 日本音響学会 秋季研究発表会 3-Q-21, 2023.

## データ作成
```
python make_wav.py
```

## 知覚実験
二つの純音S<sub>A</sub>,S<sub>B</sub>を間隔P1で二度ずつ繰り返し提示した後,
再度S<sub>A</sub>を間隔P<sub>2</sub>で提示し,このP<sub>2</sub>がP<sub>1</sub>に比べ短いか, ⻑いかを強制判断する
```
python test40.py
```
![exp_condition](https://github.com/Yaguchan/perception_experiment_v1/assets/139691814/1aa87ac7-1d9a-4db5-82fa-3c3ee16a297c)

## 弁別閾グラフ化
```
python plot_dl.py
```

## 物理時間と感覚時間の関係グラフ化
```
python plot_transform_time.py
```