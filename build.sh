#!/usr/bin/sh

mod_dir=$(readlink -f ./lib)

for dir in ./modules/*
do
  mod_name=$(basename $dir)
  echo "Building ${mod_name}"
  go build -C ${dir} -buildmode=plugin -o ${mod_dir}/${mod_name}.so .
  echo "Finished building ${mod_name}"
done
