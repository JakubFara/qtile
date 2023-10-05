#!/usr/bin/env bash

# dmenu theming
# lines="-l 20"
# font="-fn Inconsolata-13"
# colors="-nb #2C323E -nf #9899a0 -sb #BF616A -sf #2C323E"

# selected="$(ps -a -u $USER | \
#             dmenu -i -p "Type to search and select process to kill" \
#             $lines $colors $font | \
#             awk '{print $1" "$4}')";

# if [[ ! -z $selected ]]; then

#     answer="$(echo -e "Yes\nNo" | \
#             dmenu -i -p "$selected will be killed, are you sure?" \
#             $lines $colors $font )"

#     if [[ $answer == "Yes" ]]; then
#         selpid="$(awk '{print $1}' <<< $selected)";
#         kill -9 $selpid
#     fi
# fi

# exit 0

# SEL=$( gen_entries | rofi -dmenu -p "Kill Process:" -a 0 -no-custom  | awk '{print $1}' )
# kill $SEL

processes=($(ps -a -u $USER))

echo ${#processes[@]}

process_ids=()
process_names=()
for ((x=4; x<${#processes[@]}; x+=4));
do
    process_ids+=(${processes[$x]})
    process_names+=(${processes[$x + 3]})
done

function gen_entries()
{
    for a in $(seq 0 $(( ${#process_names[@]} -1 )))
    do
        echo $a ${process_names[a]}
    done
}

SEL=$( gen_entries | rofi -dmenu -p "Kill Process:" -a 0 -no-custom  | awk '{print $1}' )

echo process ${process_ids[$SEL]}
kill ${process_ids[$SEL]}
