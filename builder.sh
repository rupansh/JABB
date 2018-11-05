#!/bin/bash

. bu*/e*

if [ -z $2 ]
then
brunch $1 > log.txt

elif [ $2 == 'clean' ]
then
make clean
make clobber
brunch $1 > log.txt

elif [[ $2 == 'custom' ]] && [[ $3 != 'clean' ]]
then
lunch $1
eval '$jabbcmd' > log.txt

elif [[ $2 == 'custom' ]] && [[ $3 == 'clean' ]]
then
make clean
make clobber
lunch $1
eval '$jabbcmd' > log.txt

fi
