#!/bin/bash -e
shopt -s nullglob

if [[ -f build.env ]]; then
   . build.env
else
   echo Error: build.env does not exist or is not a file
   exit
fi

all=false
pic=false
debug=false
real=8

options=$(getopt -o '' -al all,pic,debug,r4,r8 -- "$@") || exit
eval set -- "$options"

while true; do
   case "$1" in
   --all) all=true; shift ;;
   --pic) pic=true; shift ;;
   --debug) debug=true; shift ;;
   --r4) real=4; shift ;;
   --r8) real=8; shift ;;
   --) shift; break ;;
   *) exit
   esac
done

if [[ $# -eq 2 ]]; then
   srcdir=$PWD/$1
   buildir=$PWD/$2
else
   echo Error: two arguments are required
   exit
fi

if [[ ! -d $srcdir ]]; then
   echo Error: $srcdir does not exist
   exit
fi

if [[ ! -d $buildir ]]; then
   mkdir "$buildir"
fi

flags=("${BASE_FLAGS[@]}")

if $pic; then
   flags+=(-fPIC)
fi

if $debug; then
   comptype=debug
   flags+=(-O0 "${DEBUG_FLAGS[@]}")
else
   comptype=optimized
   flags+=(-Ofast)
fi

case "$real" in
4)
   echo '{"real":{"":"float"}}' > "$buildir/.f2py_f2cmap"
   shift
   ;;
8)
   flags+=("${REAL8_FLAGS[@]}")
   echo '{"real":{"":"double"}}' > "$buildir/.f2py_f2cmap"
   shift
   ;;
*)
   echo Invalid precision type: $real
   exit
   ;;
esac

pushd "$buildir" > /dev/null

while IFS= read -r file; do
   objfile=${file%.f*}.tmp.o
   srcfile=${file%.f*}.tmp.f
   if $all || ! test -e "$objfile" || ! test -e "$file" || ! diff -q "$srcdir/$file" "$srcfile" > /dev/null; then
      rm -f "$objfile"
      cp -f "$srcdir/$file" "$srcfile"
      echo Compiling "$file"
      "$F90" "${flags[@]}" -c "$srcfile" -o "$objfile"
   fi
done < <(grep -v '^#' "$srcdir/fortran_files")

if test -f "$srcdir/f2py_files"; then
   while IFS= read -r file; do
      f2pyfile=${file%.f*}.f2py
      cp -f "$srcdir/$file" "$f2pyfile"
   done < <(grep -v '^#' "$srcdir/f2py_files")
fi

popd > /dev/null
