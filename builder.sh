#!/bin/bash

. bu*/e*

if [ $2 != 'clean' ]
then
brunch $1

else
make clean
make clobber
brunch $1

fi
