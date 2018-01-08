file_name=$(basename $1)
sed 's/\/[1-3]$//g' $1 > $2/$file_name
