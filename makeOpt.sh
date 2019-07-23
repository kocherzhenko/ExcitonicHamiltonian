for f in *.fchk
do
  echo 18 > ${f%fchk}opt
  echo 1 >> ${f%fchk}opt
  echo ${f%fchk}log2 >> ${f%fchk}opt
  echo 1 >> ${f%fchk}opt
  echo 1 >> ${f%fchk}opt
  echo 1 >> ${f%fchk}opt #2
  echo 13 >> ${f%fchk}opt
done

#for f in monomer_00*.fchk
#do
#  Multiwfn $f < ${f%fchk}opt
#  mv transdens.cub ${f%fchk}_trans1.cub
#done

