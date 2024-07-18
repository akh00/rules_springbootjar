#!/bin/bash

version=$(head -1 MODULE.bazel | sed -r 's/(^.*version[ \t]*=[^\"]*\")([^\"]+)(.*$)/\2/')

rm -rf ./bazel-*
zipfile="rules-springbootjar-${version}.zip"
zip  -x ".git*" -x ".ijwb*" -x "release_maker.sh" -r "${zipfile}" .

echo "sha256 for ${zipfil} is: $(shasum -a 256 "${zipfile}")"
