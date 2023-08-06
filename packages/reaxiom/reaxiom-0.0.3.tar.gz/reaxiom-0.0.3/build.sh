rm /Users/test/axiom/master/code/huggingface/dist/*
python -m build --outdir /Users/test/axiom/master/code/huggingface/dist
twine upload /Users/test/axiom/master/code/huggingface/dist/*
