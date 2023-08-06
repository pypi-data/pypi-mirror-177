Build:

python3 setup.py bdist_wheel

Install:

python3 -m pip install dist/*

Re-install:

rm -r dist

python3 setup.py bdist_whell

python3 -m pip install --force-reinstall dist/*

Alternative:

Build + Install:

python3 -m pip install .


For Deployment:

