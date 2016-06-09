#!/bin/bash

for f in js/*; do
	browserify $f | uglifyjs > static/$f;
done
