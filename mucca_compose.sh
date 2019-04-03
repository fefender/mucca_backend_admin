#!/bin/bash
rm -rf vendor &&
mkdir vendor &&
cd vendor &&
git clone https://github.com/fefender/mucca_logging.git &&
cd mucca_logging && git checkout -b develop && git pull origin develop && cd ..
