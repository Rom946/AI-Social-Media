import requests
from tqdm import tqdm

def download_with_progress(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(output_path, 'wb') as file:
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=output_path)
        for data in response.iter_content(1024):
            file.write(data)
            progress_bar.update(len(data))
        progress_bar.close()