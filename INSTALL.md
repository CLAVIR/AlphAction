## Installation

**Requirements**

- Python >= 3.5
- [Pytorch](https://pytorch.org/) >= 1.3.0
- [PyAV](https://github.com/mikeboers/PyAV) >= 6.2.0
- [yacs](https://github.com/rbgirshick/yacs)
- [OpenCV](https://opencv.org/)
- [tensorboardX](https://github.com/lanpa/tensorboardX)
- [tqdm](https://github.com/tqdm/tqdm)
- [FFmpeg](https://www.ffmpeg.org/)
- [Cython](https://cython.org/), [cython_bbox](https://github.com/samson-wang/cython_bbox), [SciPy](https://scipy.org/scipylib/), [matplotlib](https://matplotlib.org/), [easydict](https://github.com/makinacorpus/easydict) (for running demo)
- Linux + Nvidia GPUs

We recommend to setup the environment with Anaconda, 
the step-by-step installation script is shown below.

```bash
python3.8 -m venv venv
source venv/bin/activate

pip3 install cython
pip3 install wheel

# install pytorch with the similar cuda version as in your environment
# go to pytorch site to find the install link, for example cu113
# it seems we can only use pytorch 1.10.0 for now
pip3 install torch==1.10.0 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/<cuda_version>
pip3 install av

# download AlphAction code
cd AlphAction
pip install -e .    # Other dependicies will be installed here
```
