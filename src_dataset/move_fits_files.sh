#!/bin/bash
cd 20120201
find -name "*.fits" | xargs -i mv {} ../201202
cd ../20120202
find -name "*.fits" | xargs -i mv {} ../201202
cd ../20120301
find -name "*.fits" | xargs -i mv {} ../201203
cd ../20120302
find -name "*.fits" | xargs -i mv {} ../201203
cd ../20120401
find -name "*.fits" | xargs -i mv {} ../201204
cd ../20120402
find -name "*.fits" | xargs -i mv {} ../201204
cd ../20120501
find -name "*.fits" | xargs -i mv {} ../201205
cd ../20120502
find -name "*.fits" | xargs -i mv {} ../201205
cd ../20120601
find -name "*.fits" | xargs -i mv {} ../201206
cd ../20120602
find -name "*.fits" | xargs -i mv {} ../201206

