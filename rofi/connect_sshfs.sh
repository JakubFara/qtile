#!/usr/bin/env bash

# prefix="/home/jakub/.password-store"
ssh_files=($(ls "/home/jakub/.password-store/ssh/"))
ssh_files=( "${ssh_files[@]%.gpg}" )

ssh=$(printf '%s\n' "${ssh_files[@]}" | rofi -dmenu "$@")
[[ -n $ssh ]] || exit

pass=$(pass show "ssh/$ssh" | head -n1)

umount -l /home/jakub/remote
sshfs -o password_stdin $ssh: /home/jakub/remote <<< $pass
