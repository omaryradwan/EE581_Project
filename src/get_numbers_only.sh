for i in uniform_dist/*; do
    echo $i
    base=`basename $i .txt`
    cat $i | grep Cost | less | sed 's|######BEST LOCAL Cost is  ||' | grep -oE "[0-9]+" > uniform_dist/numbers_only_$base.txt
done

for i in squared_dist/*; do
    echo $i
    base=`basename $i .txt`
    cat $i | grep Cost | less | sed 's|######BEST LOCAL Cost is  ||' | grep -oE "[0-9]+" > squared_dist/numbers_only_$base.txt
done

for i in linear_weights/*; do
    echo $i
    base=`basename $i .txt`
    cat $i | grep Cost | less | sed 's|######BEST LOCAL Cost is  ||' | grep -oE "[0-9]+" > linear_weights/numbers_only_$base.txt
done
