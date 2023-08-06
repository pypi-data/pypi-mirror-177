# CtrlF-TF

CtrlF-TF is a python library and command line tool that calls transcription factor binding sites in DNA sequences. It does this by taking in high-throughput k-mer data and compiling them into ranked aligned sequences containing binding sites. These sequences are then searched in a given string (ctrl-f) for matches.

This program has not yet completed peer-review and is currently designated as a beta version, with a 1.0 release afterwards.

### Installation

CtrlF-TF can be installed from pypi with the following command:

`pip install ctrlf_tf`

This installs the `ctrlf_tf` python module and the `ctrlf` command line tool. The package is compatible with Linux and macOS. It has not been tested on Windows.
