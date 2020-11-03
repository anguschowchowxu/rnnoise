import os
import subprocess
from functools import partial
import numpy as np
import multiprocessing


DATA_PATH = r"D:\data\48k"
NOISE_PATH = r"D:\data\RIRS_NOISES\real_rirs_isotropic_noises"
OUTPUT_DIR = r"D:\data\output"
COUNT = 800


def get_noise_list(noise_path, cnt=10):
	
	for f in os.listdir(NOISE_PATH):
		f_path = os.path.join(NOISE_PATH, f)
		pcm_path = f_path.replace('.wav', ".pcm")
		if os.path.exists(pcm_path): 
			continue
		cmd = 'ffmpeg -y  -i ' + f_path + '  -acodec pcm_s16le -f s16le -ac 1 -ar 48000 ' + pcm_path + ' '
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	files = list(os.path.join(NOISE_PATH, f) for f in os.listdir(NOISE_PATH) 
			  if f.endswith(".pcm"))
	return np.random.choice(files, cnt, replace=False).tolist()

def gen_data_per_dir(dirname, save_dir):
	print(f'processing {dirname} {len(os.listdir(dirname))}...\n', flush=True)
	
	save_path = os.path.join(save_dir, os.path.basename(dirname))
	if os.path.exists(save_path):
		os.remove(save_path)
		
	for file in os.listdir(dirname):
		file_path = os.path.join(dirname, file)
		if (not os.path.basename(file_path).endswith(".wav")):
			continue
		
		pcm_path = file_path.replace(".wav", ".pcm")
		if not os.path.exists(pcm_path):
			cmd = 'ffmpeg -y  -i ' + file_path + '  -acodec pcm_s16le -f s16le -ac 1 -ar 48000 ' + pcm_path + ' '
			subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		noises = get_noise_list(NOISE_PATH, 10)
		
		for noise in noises:
			cmd = f'D:\\Users\\Documents\\rnnoise\\src\\denoise_training.exe {pcm_path} {noise} {COUNT} {save_path}\n'
# 			print(cmd)
			subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
# 			os.system(cmd)

dirs = [os.path.join(DATA_PATH, path) for path in os.listdir(DATA_PATH) 
		if os.path.isdir(os.path.join(DATA_PATH, path))]

# gen_data_per_dir(dirs[5], OUTPUT_DIR)




if __name__ == "__main__":
# 	pass
# 	pool = multiprocessing.Pool(4)
# 	f = partial(gen_data_per_dir, save_dir=OUTPUT_DIR)
# 	pool.map(f, dirs)
	for d in dirs:
		gen_data_per_dir(d, OUTPUT_DIR)
