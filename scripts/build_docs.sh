pip install -r doc_requirements.txt
cd docs
make html
touch _build/html/.nojekyll
