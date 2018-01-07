file_name=$(basename $1)
head -620 $1 > $2/$file_name.test
