#!/bin/bash -e
shopt -s nullglob

if [[ -f build.env ]]; then
   . build.env
else
   echo Error: build.env does not exist or is not a file
   exit
fi

if [[ -n $LAPACK_PATH ]]; then
   if [[ -d $LAPACK_PATH ]]; then
      flags+=("-L$LAPACK_PATH")
   else
      echo Error: $LAPACK_PATH does not exist or is not a directory
      exit
   fi
fi

if [[ $# -eq 2 ]]; then
   buildir=$(readlink -m "$1")
   libname=$2
else
   echo Error: two arguments are required
   exit
fi

if [[ ! -d $buildir ]]; then
   echo Error: $buildir does not exist
   exit
fi

if ! type "$PYTHON" &> /dev/null; then
   echo Error: Python executable not found
   exit
fi

if ! type "$F2PY" &> /dev/null; then
   echo Error: F2PY executable not found 
   exit
fi

python_script="import sys, sysconfig
name = 'OS' if sys.version_info < (3, 4) else 'EXT_SUFFIX'
print(sysconfig.get_config_var(name))"

echo Linking dynamic python library...
pushd "$buildir" > /dev/null
suffix=$("$PYTHON" <<< "$python_script")
export PYTHONWARNINGS=ignore::Warning:setuptools.command.install
"$F2PY" -h signature.pyf --overwrite-signature -m $libname *.f2py --quiet
"$F2PY" -c signature.pyf --fcompiler=gnu95 "${flags[@]}" -llapack *.tmp.o --quiet
popd > /dev/null
