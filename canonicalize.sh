#!/usr/bin/env bash
# Author: John W Carlson yottzumm@gmail.com
# Date: 3/10/2026

# Run Python centering progrma
# canonicalize files in Skeleton/ to Canonicalized/ and rename
# then difference with archive
# then package in a zip
python CenterCoordinatePoints.py
mkdir -p Canonicalized
for i in Skeleton/*.x3d
do
	# Canonicalize .x3d file to .xml
	java -jar C:/Users/jcarl/www.web3d.org/x3d/tools/canonical/dist/lib/X3dC14n.jar $i Canonicalized/`basename $i .x3d`Canonical.xml
	# rename .xml file to .x3d
	mv Canonicalized/`basename $i .x3d`Canonical.xml Canonicalized/`basename $i`
done
diff -w C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Skeleton/ Canonicalized/
zip Canonicalized.zip canonicalize.sh CenterCoordinatePoints.py Skeleton/* Canonicalized/*
