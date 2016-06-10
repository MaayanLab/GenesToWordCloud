#!/bin/bash

# browserify: node.js style includes for browser javascript
# uglifyjs: compress and modularize

for f in js/*; do
	browserify $f | uglifyjs > static/$f;
done
