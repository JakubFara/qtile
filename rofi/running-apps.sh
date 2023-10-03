#!/usr/bin/env bash


apps=($(xlsclients))

echo ${apps[@]}

process_ids=()
process_names=()
for ((x=0; x<${#processes[@]}; x+=2));
do
    process_ids+=(${processes[$x]})
    process_names+=(${processes[$x + 1]})
done


SEL=$( gen_entries | rofi -dmenu -p "Monitor Setup:" -a 0 -no-custom  | awk '{print $1}' )
