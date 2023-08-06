import os
__home = os.environ['HOME']
config = {
    'home': __home,
    'axiom_path': os.path.join(__home, '.axiom'),
    'axiom_cache': os.path.join(__home, '.axiom', 'cache'),
    'huggingface_cache': os.path.join(__home, '.axiom', 'huggingface_cache'),
}
