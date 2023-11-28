# Controller placement problem Algorithm Implementation

This repository contains the implementation of the algorithm proposed in the latest research to address the Controller Placement Problem.
## Algorithms
- `k_center.py` contains implementation of standard k center algorithm.
- `optimized-k-means.py` contains implementation of optimized k means algorithm proposed by [G. Wang, Y. Zhao](https://ieeexplore.ieee.org/document/7511441) 
- `density-cluster.py` contains implementation of proposed algorithm suggested by [J. Liaoa, H. Sun, J. Wang, Q. Qi, K. Li](https://dl.acm.org/doi/10.1016/j.comnet.2016.10.014)

## Installation
This is a pure python project hence you need to have `Python 3.8` or above in your system

To check your python installation and python3 command working properly run
```bash
python3 --version
```

Install virtual env if you do not have it already.

```bash
pip install virtualenv
```

Now create a virtual env and install dependency run following commands. First go to the project directory.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

## Running the code

```bash
python3 k_center.py
```

```bash
python3 density-cluster.py
```
```bash
python3 optimized-k-menas.py
```

**The project is tested on linux and macos**