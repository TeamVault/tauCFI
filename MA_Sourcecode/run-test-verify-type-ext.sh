#!/bin/bash

LLVMDIR=$HOME/typearmor/build_llvm
BINUTILS=$HOME/binutils_build
SOURCEDIR=$HOME/typearmor/src_tests/
TESTDIR=$HOME/typearmor/tests
ANALYSIS=$HOME/typearmor/run-app.sh

mkdir $TESTDIR -p

python src/py/test_verify_classification_type_ext.py --analysis-script=$ANALYSIS --binutils-dir=$BINUTILS --llvm-build-dir=$LLVMDIR --source-dir=$SOURCEDIR --test-dir=$TESTDIR

