import huggingface_hub as hh

import huggingface_hub as hh
repo_id = 'dijunluo/axiom3'
hh.create_repo(repo_id, repo_type='dataset', private=False)
ff = hh.upload_file(
    path_or_fileobj='/home/aistudio/t5.py',
    path_in_repo="obj/xxx",
    repo_id=repo_id,
    repo_type="dataset",
)

hf_hub_download('dijunluo/axiom', 'obj/xxx')
print(ff)
## curl https://huggingface.co/datasets/dijunluo/axiom3/raw/main/obj/xxx