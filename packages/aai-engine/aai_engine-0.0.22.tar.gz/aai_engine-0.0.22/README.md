# AAI Engine

The AAI Engine is a computer vision based automation python library, enabling easy desktop automation with legacy applications, citrix environments, webapps and regualar desktop apps.

## Installation
### Local
```python -m pip install -e c:\<>\<>\aai_engine```

or if that does not work (permission issue):

```python3 -m pip install --no-build-isolation -e /media/toto/Samsung_T5/AdAstraIndustries/aai_engine```

If on macos with an m1, create a conda environment to be able to use opencv.

brew install miniforge
conda init zsh
conda create -n aai python=3.8.6
conda activate aai
conda install -c conda-forge opencv

## Build
`python -m build`

Should you want to add files not directly under src/aai_engine_package, add them in MANIFEST.in.

### Upload to PyPi
`twine upload dist/*`


## Usage
TODO: fill with example paths
Make sure there is an img/ folder in the spec
### Take a screenshot
```python ./take_screenshot.py '/Users/toto/Documents/dev/aai_engine_example_app/rpa_challenge_1'```

### Edit a screenshot
```python ./take_screenshot.py '/Users/toto/Documents/dev/aai_engine_example_app/rpa_challenge_1' '/Users/toto/Documents/dev/aai_engine_example_app/rpa_challenge_1/img/last_name.png'```
