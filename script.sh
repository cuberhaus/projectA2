#!/bin/bash

g++ -o "Connex_i_Complex.x" "Connex_i_Complex".cc

i=1
while [ $i -le 2 ]; do
      if [ $i -eq 1 ]; then file="Binomial"
      else file="Geometric"
      fi
      for filename1 in $file/*; do
          name1=`basename -a $filename1`
          for filename2 in $filename1/*; do 
              name2=`basename -a $filename2`
              mkdir -p "Out$file/$name1/$name2"
              for filename3 in $filename2/*; do
                  name3=`basename -a $filename3`        
                  ./"Connex_i_Complex.x" <"$filename3" > "out$name3"
                  mv "out$name3" "Out$file/$name1/$name2"
                  done
              done
          done 
      i=$(($i + 1))
      done


