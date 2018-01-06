
#sed 's/^@@/@/g' $1 | sed 's/[[:space:]]1:N:0:0/\\2/g' 

sed 's/..$/\\1/g' $1 
