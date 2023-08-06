import os
from .settings import config
for x in ['axiom_path', 'axiom_cache', 'huggingface_cache']:
    folder = config[x]
    if not os.path.isdir(folder):
        os.mkdir(folder)
