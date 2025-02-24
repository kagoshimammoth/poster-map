## ポスティングデータをエリアごとに分割しjsonに出力する
# ポスティングマップデータ id(連番),エリア名(自治体名),エリア名(住所),トータル枚数,最近の枚数,備考
# conquerlist.csv id,area_name,subarea_name,total_posting,recently_posting,note
# ブロックデータ id(連番),エリアキー(ローマ字),エリア名(自治体名)
# conquerblock.csv area_id,area_key,area_name
# python3 bin/conquercsv2json_small.py public/data/conquerlist.csv public/data/conquerblock.csv public/data/

import pandas as pd
import sys
import os

def main(input_path, block_path, output_path):

    inputdata = pd.read_csv(input_path)
    inputdata.rename(columns={'area': 'area_name'}, inplace=True) # inputdataのareaをarea_nameに変更

    blocklist = pd.read_csv(block_path)
    blocklist = blocklist[['area_id', 'area_key', 'area_name']] # blocklistをarea_id, area_key, area_nameだけにする
    conquer_blocks = dict(zip(blocklist['area_key'], blocklist['area_name'])) # key valueの形のJSONにする

    merged_data = pd.merge(inputdata, blocklist, on='area_name', how='left', suffixes=('', '')) # left_joinでマージ
    final_data = merged_data.copy()[['id', 'area_id', 'area_key', 'subarea_name', 'total_posting', 'recently_posting', 'note']] # 必要なデータのみ取り出し
   
    for area_key, area_name in conquer_blocks.items():
        block_areas = blocklist[blocklist['area_name'] == area_name]['area_id']
        filtered_data = final_data[final_data['area_id'].isin(block_areas)]
        filtered_data = filtered_data[['subarea_name', 'total_posting', 'recently_posting', 'note']] # 地名、トータルポスティング枚数、最近のポスティング枚数、備考
        filtered_output_path = os.path.join(output_path, 'conquer', f'{area_key}.json')
        filtered_data.to_json(filtered_output_path, orient='records', force_ascii=False)
        print(f"Filtered file saved to {filtered_output_path}")

    json_output_path = os.path.join(output_path, 'conquerlist.json')
    final_data.to_json(json_output_path, orient='records', force_ascii=False)
    print(f"File saved to {json_output_path}")

    json_output_path = os.path.join(output_path, 'conquerblock.json')
    blocklist.to_json(json_output_path, orient='records', force_ascii=False)
    print(f"File saved to {json_output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_path> <block_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]  # public/data/conquerlist.csv
    block_path = sys.argv[2]  # public/data/conquerblock.csv
    output_path = sys.argv[3] # public/data/

    main(input_path, block_path, output_path)
