import os

from surprise import Reader, Dataset, KNNBaseline

from TTMS.settings import BASE_DIR

file_path = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'recmmond_data.txt')

reader = Reader(line_format='user item rating', sep='\t')
data = Dataset.load_from_file(file_path, reader=reader)

trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}

algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)

path = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'play_id.txt')

f = open(path)
cur_play_id = f.read()
f.close()
# print(cur_play_id,'===========')
cur_play_inner_id = algo.trainset.to_inner_iid(cur_play_id)
cur_play_neighbors = algo.get_neighbors(cur_play_inner_id, k=6)
# print(cur_play_neighbors)
cur_play_neighbors = (algo.trainset.to_raw_iid(inner_id) for inner_id in cur_play_neighbors)

path = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'recmmond_play_result.txt')

f = open(path, 'w')
f.write(','.join(cur_play_neighbors))
f.close()
# for play_id in cur_play_neighbors:
#     print(play_id, '----------')

