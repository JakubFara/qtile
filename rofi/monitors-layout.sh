#!/bin/bash

XRANDR=$(which xrandr)

MONITORS=( $( ${XRANDR} | awk '( $2 == "connected" ){ print $1 }' ) )
# MONITORS=("DP-1" "HDMI-1" "eDP-1")
NUM_MONITORS=${#MONITORS[@]}

TITLES=()
COMMANDS=()


function gen_xrandr_only()
{
    selected=("$@")

    previous=${MONITORS[${selected[0]}]}
    cmd="xrandr --output $previous --auto "

    for ((x=1; x<${#selected[@]}; x++));
    do
        entry=${selected[x]}
        cmd="$cmd --output ${MONITORS[$entry]} --auto --left-of $previous"
        previous=${MONITORS[$entry]}
    done

    for entry in $(seq 0 $((${NUM_MONITORS}-1)))
    do
        # if [[ ! " ${selected[*]} " =~ " ${entry} " ]]
        if [[ ! ${selected[*]} =~ $entry ]]
        then
            cmd="$cmd --output ${MONITORS[$entry]} --off"
        fi
    done

    echo $cmd
}



declare -i index=0
TILES[$index]="Cancel"
COMMANDS[$index]="true"
index+=1


for entry in $(seq 0 $((${NUM_MONITORS}-1)))
do
    array=($entry)
    TILES[$index]="Only ${MONITORS[$entry]}"
    COMMANDS[$index]=$(gen_xrandr_only ${array[@]} )
    echo $(gen_xrandr_only ${array[@]} )
    index+=1
done

##
# Dual screen options
##
for entry_a in $(seq 0 $((${NUM_MONITORS}-1)))
do
    for entry_b in $(seq 0 $((${NUM_MONITORS}-1)))
    do
        if [ $entry_a != $entry_b ]
        then
            TILES[$index]=" ${MONITORS[$entry_b]} -> ${MONITORS[$entry_a]}"
            # COMMANDS[$index]="xrandr --output ${MONITORS[$entry_a]} --auto \
            #                   --output ${MONITORS[$entry_b]} --auto --left-of ${MONITORS[$entry_a]}"

            array=($entry_a $entry_b)
            COMMANDS[$index]=$(gen_xrandr_only ${array[@]} )
            echo $(gen_xrandr_only ${array[@]} )
            index+=1
        fi
    done
done


##
# Clone monitors
##
for entry_a in $(seq 0 $((${NUM_MONITORS}-1)))
do
    for entry_b in $(seq 0 $((${NUM_MONITORS}-1)))
    do
        if [ $entry_a != $entry_b ]
        then
            TILES[$index]="Clone ${MONITORS[$entry_b]} -> ${MONITORS[$entry_a]}"
            COMMANDS[$index]="xrandr --output ${MONITORS[$entry_a]} --auto \
                              --output ${MONITORS[$entry_b]} --auto --same-as ${MONITORS[$entry_a]}"

            index+=1
        fi
    done
done



##
# Thre screen options
##
for entry_a in $(seq 0 $((${NUM_MONITORS}-1)))
do
    for entry_b in $(seq 0 $((${NUM_MONITORS}-1)))
    do

        for entry_c in $(seq 0 $((${NUM_MONITORS}-1)))
        do
            if [ $entry_a != $entry_b ] && [ $entry_a != $entry_c ] && [ $entry_b != $entry_c ]
            then
                TILES[$index]=" ${MONITORS[$entry_c]} -> ${MONITORS[$entry_b]} -> ${MONITORS[$entry_a]}"
                COMMANDS[$index]="xrandr --output ${MONITORS[$entry_a]} --auto \
                    --output ${MONITORS[$entry_b]} --auto --left-of ${MONITORS[$entry_a]} \
                    --output ${MONITORS[$entry_c]} --auto --left-of ${MONITORS[$entry_b]}"

                index+=1
            fi
        done
    done
done

##
#  Generate entries, where first is key.
##
function gen_entries()
{
    for a in $(seq 0 $(( ${#TILES[@]} -1 )))
    do
        echo $a ${TILES[a]}
    done
}

# Call menu
SEL=$( gen_entries | rofi -dmenu -p "Monitor Setup:" -a 0 -no-custom  | awk '{print $1}' )

# Call xrandr
$( ${COMMANDS[$SEL]} )
