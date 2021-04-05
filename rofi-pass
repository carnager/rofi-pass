#!/usr/bin/env bash

# rofi-pass
# (c) 2015 Rasmus Steinke <rasi@xssn.at>
basecommand="$0"

# set default settings
_rofi () {
	rofi -no-auto-select -i "$@"
}

_pwgen () {
	pwgen -y "$@"
}

_image_viewer () {
	feh -
}

_clip_in_primary() {
	xclip
}

_clip_in_clipboard() {
	xclip -selection clipboard
}

_clip_out_primary() {
	xclip -o
}

_clip_out_clipboard() {
	xclip --selection clipboard -o
}


config_dir=${XDG_CONFIG_HOME:-$HOME/.config}
cache_dir=${XDG_CACHE_HOME:-$HOME/.cache}

# We expect to find these fields in pass(1)'s output
URL_field='url'
USERNAME_field='user'
AUTOTYPE_field='autotype'
OTPmethod_field='otp_method'

default_autotype="user :tab pass"
delay=2
wait=0.2
xdotool_delay=12
default_do='menu' # menu, copyPass, typeUser, typePass, copyUser, copyUrl, viewEntry, typeMenu, actionMenu, copyMenu, openUrl
auto_enter='false'
notify='false'
help_color=""
clip=primary
clip_clear=45
default_user="${ROFI_PASS_DEFAULT_USER-$(whoami)}"
default_user2=john_doe
password_length=12
fix_layout=false

# default shortcuts
autotype="Alt+1"
type_user="Alt+2"
type_pass="Alt+3"
open_url="Alt+4"
copy_name="Alt+u"
copy_url="Alt+l"
copy_pass="Alt+p"
show="Alt+o"
copy_menu="Alt+c"
action_menu="Alt+a"
type_menu="Alt+t"
help="Alt+h"
switch="Alt+x"
insert_pass="Alt+n"
qrcode="Alt+q"
previous_root="Shift+Left"
next_root="Shift+Right"

# Safe permissions
umask 077

has_qrencode() {
	command -v qrencode >/dev/null 2>&1
}

listgpg () {
	mapfile -d '' pw_list < <(find -L . -name '*.gpg' -print0)
	pw_list=("${pw_list[@]#./}")
	printf '%s\n' "${pw_list[@]}" | sort -n
}

# get all password files and output as newline-delimited text
list_passwords() {
	cd "${root}" || exit
	mapfile -t pw_list < <(listgpg)
	printf '%s\n' "${pw_list[@]%.gpg}" | sort -n
}

doClip () {
	case "$clip" in
		"primary") _clip_in_primary ;;
		"clipboard") _clip_in_clipboard ;;
		"both") _clip_in_primary; _clip_out_primary | _clip_in_clipboard;;
	esac
}

checkIfPass () {
	printf '%s\n' "${root}: $selected_password" >| "$cache_dir/rofi-pass/last_used"
}


autopass () {
	x_repeat_enabled=$(xset q | awk '/auto repeat:/ {print $3}')
	xset r off

	rm -f "$cache_dir/rofi-pass/last_used"
	printf '%s\n' "${root}: $selected_password" > "$cache_dir/rofi-pass/last_used"
	for word in ${stuff["$AUTOTYPE_field"]}; do
		case "$word" in
			":tab") xdotool key Tab;;
			":space") xdotool key space;;
			":delay") sleep "${delay}";;
			":enter") xdotool key Return;;
			":otp") printf '%s' "$(generateOTP)" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -;;
			"pass") printf '%s' "${password}" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -;;
			"path") printf '%s' "${selected_password}" | rev | cut -d'/' -f1 | rev | xdotool type --clearmodifiers --file -;;
			*) printf '%s' "${stuff[${word}]}" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -;;
		esac
	done

	if [[ ${auto_enter} == "true" ]]; then
		xdotool key Return
	fi

	xset r "$x_repeat_enabled"
	unset x_repeat_enabled
	clearUp
}

generateQrCode() {
	has_qrencode

	if [[ $? -eq "1" ]]; then
		printf '%s\n' "qrencode not found" | _rofi -dmenu
		exit_code=$?
		if [[ $exit_code -eq "1" ]]; then
			exit
		else
			"${basecommand}"
		fi
	fi

	checkIfPass
	pass "$selected_password" | head -n 1 | qrencode -d 300 -v 8 -l H -o - | _image_viewer
	if [[ $? -eq "1" ]]; then
		printf '%s\n' "" | _rofi -dmenu -mesg "Image viewer not defined or cannot read from pipe"
		exit_value=$?
		if [[ $exit_value -eq "1" ]]; then
			exit
		else
			"${basecommand}"
		fi
	fi
	clearUp
}

openURL () {
	checkIfPass
	$BROWSER "$(PASSWORD_STORE_DIR="${root}" pass "$selected_password" | grep "${URL_field}: " | gawk '{sub(/:/,"")}{print $2}1' | head -1)"; exit;
	clearUp
}

typeUser () {
	checkIfPass

	x_repeat_enabled=$(xset q | awk '/auto repeat:/ {print $3}')
	xset r off

	printf '%s' "${stuff[${USERNAME_field}]}" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -

	xset r "$x_repeat_enabled"
	unset x_repeat_enabled

	clearUp
}

typePass () {
	checkIfPass

	x_repeat_enabled=$(xset q | awk '/auto repeat:/ {print $3}')
	xset r off

	printf '%s' "${password}" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -

	if [[ $notify == "true" ]]; then
		if [[ "${stuff[notify]}" == "false" ]]; then
			:
		else
			notify-send "rofi-pass" "finished typing password";
		fi
	elif [[ $notify == "false" ]]; then
		if [[ "${stuff[notify]}" == "true" ]]; then
			notify-send "rofi-pass" "finished typing password";
		else
			:
		fi
	fi

	xset r "$x_repeat_enabled"
	unset x_repeat_enabled
	clearUp
}

typeField () {
	checkIfPass
	local to_type

	x_repeat_enabled=$(xset q | awk '/auto repeat:/ {print $3}')
	xset r off

	case $typefield in
		"OTP") to_type="$(generateOTP)" ;;
		*) to_type="${stuff[${typefield}]}" ;;
	esac

	printf '%s' "$to_type" | xdotool type --delay ${xdotool_delay} --clearmodifiers --file -

	xset r "$x_repeat_enabled"
	unset x_repeat_enabled
	unset to_type

	clearUp
}

generateOTP () {
	checkIfPass

	# First, we check if there is a non-conventional OTP command in the pass file
	if PASSWORD_STORE_DIR="${root}" pass "$selected_password" | grep -q "${OTPmethod_field}: "; then
		# We execute the commands after otp_method: AS-IS
		bash -c "$(PASSWORD_STORE_DIR="${root}" pass "$selected_password" | grep "${OTPmethod_field}: " | cut -d' ' -f2-)"
	else
		# If there is no method defined, fallback to pass-otp
		PASSWORD_STORE_DIR="${root}" pass otp "$selected_password"
	fi

	clearUp
}

copyUser () {
	checkIfPass
	printf '%s' "${stuff[${USERNAME_field}]}" | doClip
	clearUp
}

copyField () {
	checkIfPass
	printf '%s' "${stuff[${copyfield}]}" | doClip
	clearUp
}

copyURL () {
	checkIfPass
	printf '%s' "${stuff[${URL_field}]}" | doClip
	clearUp
}

copyPass () {
	checkIfPass
	printf '%s' "$password" | doClip
	if [[ $notify == "true" ]]; then
		notify-send "rofi-pass" "Copied Password\\nClearing in $clip_clear seconds"
	fi

	if [[ $notify == "true" ]]; then
		(sleep $clip_clear; printf '%s' "" | _clip_in_primary; printf '%s' "" | _clip_in_clipboard | notify-send "rofi-pass" "Clipboard cleared") &
	elif [[ $notify == "false" ]]; then
		(sleep $clip_clear; printf '%s' "" | _clip_in_primary; printf '%s' "" | _clip_in_clipboard) &
	fi
}

viewEntry () {
	checkIfPass
	showEntry "${selected_password}"
}

generatePass () {
	askmenu_content=(
		"Yes"
		"No"
	)

	askGenMenu=$(printf '%s\n' "${askmenu_content[@]}" | _rofi -dmenu -p "Generate new Password for ${selected_password}? > ")
	askgen_exit=$?

	if [[ $askgen_exit -eq 1 ]]; then
		exit
	fi
	if [[ $askGenMenu == "Yes" ]]; then
		true
	elif [[ $askGenMenu == "No" ]]; then
		actionMenu
	fi

	checkIfPass

	symbols_content=(
		"0  Cancel"
		"1  Yes"
		"2  No"
	)

	symbols=$(printf '%s\n' "${symbols_content[@]}" | _rofi -dmenu -p "Use Symbols? > ")
	symbols_val=$?

	if [[ $symbols_val -eq 1 ]]; then
		exit
	fi
	if [[ $symbols == "0  Cancel" ]]; then
		mainMenu;
	elif [[ $symbols == "1  Yes" ]]; then
		symbols="";
	elif [[ $symbols == "2  No" ]]; then
		symbols="-n";
	fi

	HELP="<span color='$help_color'>Enter Number or hit Enter to use default length</span>"
	length=$(printf '%s' "" | _rofi -dmenu -mesg "${HELP}" -p "Password length? (Default: ${password_length}) > ")
	length_exit=$?

	if [[ $length_exit -eq 1 ]]; then
		exit
	fi
	if [[ $length == "" ]]; then
		PASSWORD_STORE_DIR="${root}" pass generate ${symbols} -i "$selected_password" "${password_length}" > /dev/null;
	else
		PASSWORD_STORE_DIR="${root}" pass generate ${symbols} -i "$selected_password" "${length}" > /dev/null;
	fi
}

# main Menu
mainMenu () {
	if [[ $1 == "--bmarks" ]]; then
		selected_password="$(list_passwords 2>/dev/null \
			| _rofi -mesg "Bookmarks Mode. ${switch} to switch" \
			-dmenu \
			-kb-custom-10 "${switch}" \
			-select "$entry" \
			-p "rofi-pass > ")"

		rofi_exit=$?

		if [[ $rofi_exit -eq 1 ]]; then
			exit
		elif [[ $rofi_exit -eq 19 ]]; then
			${basecommand}
		elif [[ $rofi_exit -eq 0 ]]; then
			openURL
		fi
	else
		unset selected_password

		args=( -dmenu
			-kb-custom-1 "${autotype}"
			-kb-custom-2 "${type_user}"
			-kb-custom-3 "${type_pass}"
			-kb-custom-4 "${open_url}"
			-kb-custom-5 "${copy_name}"
			-kb-custom-6 "${copy_pass}"
			-kb-custom-7 "${show}"
			-kb-custom-8 "${copy_url}"
			-kb-custom-9 "${type_menu}"
			-kb-custom-10 "${previous_root}"
			-kb-custom-11 "${next_root}"
			-kb-custom-14 "${action_menu}"
			-kb-custom-15 "${copy_menu}"
			-kb-custom-16 "${help}"
			-kb-custom-17 "${switch}"
			-kb-custom-18 "${insert_pass}"
			-kb-custom-19 "${qrcode}"
		)
		args+=( -kb-mode-previous ""    # These keyboard shortcut options are needed, because
		-kb-mode-next ""            # Shift+<Left|Right> are otherwise taken by rofi.
		-select "$entry"
		-p "> "	)

		if [[ ${#roots[@]} -gt "1" || $custom_root == "true" ]]; then
			args+=(-mesg "PW Store: ${root}")
		fi

		selected_password="$(list_passwords 2>/dev/null | _rofi "${args[@]}")"

		rofi_exit=$?
		if [[ $rofi_exit -eq 1 ]]; then
			exit
		fi

		# Actions based on exit code, which do not need the entry.
		# The exit code for -kb-custom-X is X+9.
		case "${rofi_exit}" in
			19) roots_index=$(( (roots_index-1+roots_length) % roots_length)); root=${roots[$roots_index]}; mainMenu; return;;
			20) roots_index=$(( (roots_index+1) % roots_length)); root=${roots[$roots_index]}; mainMenu; return;;
			25) helpMenu; return;;
			26) ${basecommand} --bmarks; return;;
		esac

		mapfile -t password_temp < <(PASSWORD_STORE_DIR="${root}" pass show "$selected_password")
		password=${password_temp[0]}

		if [[ ${password} == "#FILE="* ]]; then
			pass_file="${password#*=}"
			mapfile -t password_temp2 < <(PASSWORD_STORE_DIR="${root}" pass show "${pass_file}")
			password=${password_temp2[0]}
		fi

		fields=$(printf '%s\n' "${password_temp[@]:1}" | awk '$1 ~ /:$/ || /otpauth:\/\// {$1=$1;print}')
		declare -A stuff
		stuff["pass"]=${password}

		if [[ -n $fields ]]; then
			while read -r LINE; do
				unset _id _val
				case "$LINE" in
					"otpauth://"*|"${OTPmethod_field}"*)
						_id="OTP"
						_val=""
						;;
					*)
						_id="${LINE%%: *}"
						_val="${LINE#* }"
						;;
				esac

				if [[ -n "$_id" ]]; then
					stuff["${_id}"]=${_val}
				fi
			done < <(printf '%s\n' "${fields}")

			if test "${stuff['autotype']+autotype}"; then
				:
			else
				stuff["autotype"]="${USERNAME_field} :tab pass"
			fi
		fi
	fi

	if [[ -z "${stuff["${AUTOTYPE_field}"]}" ]]; then
		if [[ -n $default_autotype ]]; then
			stuff["${AUTOTYPE_field}"]="${default_autotype}"
		fi
	fi
	if [[ -z "${stuff["${USERNAME_field}"]}" ]]; then
		if [[ -n $default_user ]]; then
			if [[ "$default_user" == ":filename" ]]; then
				stuff["${USERNAME_field}"]="$(basename "$selected_password")"
			else
				stuff["${USERNAME_field}"]="${default_user}"
			fi
		fi
	fi
	pass_content="$(for key in "${!stuff[@]}"; do printf '%s\n' "${key}: ${stuff[$key]}"; done)"

	# actions based on keypresses
	# The exit code for -kb-custom-X is X+9.
	case "${rofi_exit}" in
		0) typeMenu;;
		10) sleep $wait; autopass;;
		11) sleep $wait; typeUser;;
		12) sleep $wait; typePass;;
		13) openURL;;
		14) copyUser;;
		15) copyPass;;
		16) viewEntry;;
		17) copyURL;;
		18) default_do="menu" typeMenu;;
		23) actionMenu;;
		24) copyMenu;;
		27) insertPass;;
		28) generateQrCode;;
	esac
	clearUp
}


clearUp () {
	password=''
	selected_password=''
	unset stuff
	unset password
	unset selected_password
	unset password_temp
	unset stuff
}

helpMenu () {
	_rofi -dmenu -mesg "Hint: All hotkeys are configurable in config file" -p "Help > " <<- EOM
	${autotype}: Autotype
	${type_user}: Type Username
	${type_pass}: Type Password
	${qrcode}: Generate and display qrcode
	---
	${copy_name}: Copy Username
	${copy_pass}: Copy Password
	${copy_url}: Copy URL
	${open_url}: Open URL
	${copy_menu}: Copy Custom Field
	---
	${action_menu}: Edit, Move, Delete, Re-generate Submenu
	${show}: Show Password File
	${insert_pass}: Insert new Pass Entry
	${switch}: Switch Pass/Bookmark Mode
	---
	${previous_root}: Switch to previous password store (--root)
	${next_root}: Switch to next password store (--root)
EOM
help_val=$?

if [[ $help_val -eq 1 ]]; then
	exit;
else
	unset helptext; mainMenu;
fi
}


typeMenu () {
	if [[ -n $default_do ]]; then
		if [[ $default_do == "menu" ]]; then
			checkIfPass
			local -a keys=("${!stuff[@]}")
			keys=("${keys[@]/$AUTOTYPE_field}")
			typefield=$({ printf '%s' "${AUTOTYPE_field}" ; printf '%s\n' "${keys[@]}" | sort; } | _rofi -dmenu  -p "Choose Field to type > ")
			typefield_exit=$?
			if [[ $typefield_exit -eq 1 ]]; then
				exit
			fi
			case "$typefield" in
				'') exit;;
				'pass') sleep $wait; typePass;;
				"${AUTOTYPE_field}") sleep $wait; autopass;;
				*) sleep $wait; typeField
			esac
			clearUp
		elif [[ $default_do == "${AUTOTYPE_field}" ]]; then
			sleep $wait; autopass
		else
			${default_do}
		fi
	fi
}

copyMenu () {
	checkIfPass
	copyfield=$(printf '%s\n' "${!stuff[@]}" | sort | _rofi -dmenu  -p "Choose Field to copy > ")
	val=$?
	if [[ $val -eq 1 ]]; then
		exit;
	fi
	if [[ $copyfield == "pass" ]]; then
		copyPass;
	else
		copyField
	fi
	clearUp
}

actionMenu () {
	checkIfPass
	action_content=("< Return"
		"---"
		"1 Move Password File"
		"2 Copy Password File"
		"3 Delete Password File"
		"4 Edit Password File"
		"5 Generate New Password"
	)

	action=$(printf '%s\n' "${action_content[@]}" | _rofi -dmenu -p "Choose Action > ")
	if [[ ${action} == "1 Move Password File" ]]; then
		manageEntry move;
	elif [[ ${action} == "3 Delete Password File" ]]; then
		manageEntry delete;
	elif [[ ${action} == "2 Copy Password File" ]]; then
		manageEntry copy;
	elif [[ ${action} == "4 Edit Password File" ]]; then
		manageEntry edit;
	elif [[ ${action} == "5 Generate New Password" ]]; then
		generatePass;
	elif [[ ${action} == "< Return" ]]; then
		mainMenu;
	elif [[ ${action} == "" ]]; then
		exit
	fi
}

showEntry () {
	if [[ -z $pass_content ]]; then
		pass_temp=$(PASSWORD_STORE_DIR="${root}" pass show "$selected_password")
		password="${pass_temp%%$'\n'*}"
		pass_key_value=$(printf '%s\n' "${pass_temp}" | tail -n+2 | grep ': ')
		declare -A stuff

		while read -r LINE; do
			_id="${LINE%%: *}"
			_val="${LINE#* }"
			stuff["${_id}"]=${_val}
		done < <(printf '%s\n' "${pass_key_value}")

		stuff["pass"]=${password}

		if test "${stuff['autotype']+autotype}"; then
			:
		else
			stuff["autotype"]="${USERNAME_field} :tab pass"
		fi

		pass_content="$(for key in "${!stuff[@]}"; do printf '%s\n' "${key}: ${stuff[$key]}"; done)"
	fi

	bla_content=("< Return"
		"${pass_content}"
	)

	bla=$(printf '%s\n' "${bla_content[@]}" | _rofi -dmenu -mesg "Enter: Copy entry to clipboard" -p "> ")
	rofi_exit=$?

	word=$(printf '%s' "$bla" | gawk -F': ' '{print $1}')

	if [[ ${rofi_exit} -eq 1 ]]; then
		exit
	elif [[ ${rofi_exit} -eq 0 ]]; then
		if [[ ${bla} == "< Return" ]]; then
			mainMenu
		else
			if [[ -z $(printf '%s' "${stuff[${word}]}") ]]; then
				printf '%s' "$word" | doClip
			else
				printf '%s' "${stuff[${word}]}" | doClip
			fi
			if [[ $notify == "true" ]]; then
				notify-send "rofi-pass" "Copied Password\\nClearing in $clip_clear seconds"
			fi
			if [[ $notify == "true" ]]; then
				(sleep $clip_clear; printf '%s' "" | _clip_in_primary; printf '%s' "" | _clip_in_clipboard | notify-send "rofi-pass" "Clipboard cleared") &
			elif [[ $notify == "false" ]]; 	then
				(sleep $clip_clear; printf '%s' "" | _clip_in_primary; printf '%s' "" | _clip_in_clipboard) &
			fi
			exit
		fi
	fi
	exit
	unset stuff
	unset password
	unset selected_password
	unset password_temp
	unset stuff
	exit
}

manageEntry () {
	if [[ "$1" == "edit" ]]; then
		EDITOR=$EDITOR PASSWORD_STORE_DIR="${root}" pass edit "${selected_password}"
		mainMenu
	elif [[ $1 == "move" ]]; then
		cd "${root}" || exit
		group_array=(*/)
		group=$(printf '%s\n' "${group_array[@]%/}" | _rofi -dmenu -p "Choose Group > ")
		if [[ $group == "" ]]; then
			exit
		fi
		PASSWORD_STORE_DIR="${root}" pass mv "$selected_password" "${group}"
		mainMenu
	elif [[ $1 == "copy" ]]; then
		cd "${root}" || exit
		group_array=(*/)
		group=$(printf '%s\n' "${group_array[@]%/}" | _rofi -dmenu -p "Choose Group > ")
		if [[ $group == "" ]]; then
			exit
		else
			new_name="$(listgpg | _rofi -dmenu -format 'f' -mesg "Copying to same Group. Please enter a name for the new entry" -p "> ")"
		fi
		PASSWORD_STORE_DIR="${root}" pass cp "$selected_password" "${group}/${new_name}"
		mainMenu
	elif [[ "$1" == "delete" ]]; then
		HELP="<span color='$help_color'>Selected entry: ${selected_password}</span>"
		ask_content=("Yes"
			"No"
		)
		ask=$(printf '%s\n' "${ask_content[@]}" | _rofi -mesg "${HELP}" -dmenu -p "Are You Sure? > ")
		if [[ "$ask" == "Yes" ]]; then
			PASSWORD_STORE_DIR="${root}" pass rm --force "${selected_password}"
		elif [[ "$ask" == "No" ]]; then
			mainMenu
		elif [[ -z "$ask" ]]; then
			exit
		fi
	else
		mainMenu
	fi
}

edit_pass() {
    if [[ $edit_new_pass == "true" ]]; then
        PASSWORD_STORE_DIR="${root}" pass edit "${1}"
    fi
}

insertPass () {
	url=$(_clip_out_clipboard)

	if [[ "${url:0:4}" == "http" ]]; then
		domain_name="$(printf '%s\n' "${url}" | awk -F / '{l=split($3,a,"."); print (a[l-1]=="com"?a[l-2] OFS:X) a[l-1] OFS a[l]}' OFS=".")"
		help_content="Domain: ${domain_name}
		Type name, make sure it is unique"
	else
		help_content="Hint: Copy URL to clipboard before calling this menu.
		Type name, make sure it is unique"
	fi

	cd "${root}" || exit
	group_array=(*/)
	grouplist=$(printf '%s\n' "${group_array[@]%/}")
	name="$(listgpg | _rofi -dmenu -format 'f' -filter "${domain_name}" -mesg "${help_content}" -p "> ")"
	val=$?

	if [[ $val -eq 1 ]]; then
		exit
	fi

	user_content=("${default_user2}"
		"${USER}"
		"${default_user}"
	)

	user=$(printf '%s\n' "${user_content[@]}" | _rofi -dmenu -mesg "Chose Username or type" -p "> ")
	val=$?

	if [[ $val -eq 1 ]]; then
		exit
	fi

	group_content=("No Group"
		"---"
		"${grouplist}"
	)

	group=$(printf '%s\n' "${group_content[@]}" | _rofi -dmenu -p "Choose Group > ")
	val=$?

	if [[ $val -eq 1 ]]; then
		exit
	fi

	pw=$(printf '%s' "Generate" | _rofi -dmenu -password -p "Password > " -mesg "Type Password or hit Enter to generate one")

	if [[ $pw == "Generate" ]]; then
		pw=$(_pwgen "${password_length}")
	fi

	clear

	if [[ "$group" == "No Group" ]]; then
		if [[ $url == http* ]]; then
			pass_content=("${pw}"
				"---"
				"${USERNAME_field}: ${user}"
				"${URL_field}: ${url}"
			)
			printf '%s\n' "${pass_content[@]}" | PASSWORD_STORE_DIR="${root}" pass insert -m "${name}" > /dev/null && edit_pass "${name}"
		else
			pass_content=("${pw}"
				"---"
				"${USERNAME_field}: ${user}"
			)
			printf '%s\n' "${pass_content[@]}" | PASSWORD_STORE_DIR="${root}" pass insert -m "${name}" > /dev/null && edit_pass "${name}"
		fi
	else
		if [[ $url == http* ]]; then
			pass_content=("${pw}"
				"---"
				"${USERNAME_field}: ${user}"
				"${URL_field}: ${url}"
			)
			printf '%s\n' "${pass_content[@]}" | PASSWORD_STORE_DIR="${root}" pass insert -m "${group}/${name}" > /dev/null && edit_pass "${group}/${name}"
		else
			pass_content=("${pw}"
				"---"
				"${USERNAME_field}: ${user}"
			)
			printf '%s\n' "${pass_content[@]}" | PASSWORD_STORE_DIR="${root}" pass insert -m "${group}/${name}" > /dev/null && edit_pass "${group}/${name}"
		fi
	fi
}

help_msg () {
	cat <<'EOF'
	Usage:
	rofi-pass [command]

	Commands:
	--insert         insert new entry to password store
	--root           set custom root directories (colon separated)
	--last-used      highlight last used item
	--show-last      show details of last used Entry
	--bmarks         start in bookmarks mode

	rofi-pass version 1.5.3
EOF
}

get_config_file () {
	configs=("$ROFI_PASS_CONFIG"
		"$config_dir/rofi-pass/config"
		"/etc/rofi-pass.conf")

	# return the first config file with a valid path
	for config in "${configs[@]}"; do
		# '-n' is needed in case ROFI_PASS_CONFIG is not set
		if [[ -n "${config}" && -f "${config}" ]]; then
			printf "%s" "$config"
			return
		fi
	done
}

main () {
	# load config file
	config_file="$(get_config_file)"
	[[ -n "$config_file" ]] && source "$config_file"

	# create tmp dir
	if [[ ! -d "$cache_dir/rofi-pass" ]]; then
		mkdir -p "$cache_dir/rofi-pass"
	fi

	# fix keyboard layout if enabled in config
	if [[ $fix_layout == "true" ]]; then
		layout_cmd
	fi

	# set help color
	if [[ $help_color == "" ]]; then
		help_color=$(rofi -dump-xresources | grep 'rofi.color.normal' | gawk -F ',' '/,/{gsub(/ /, "", $2); print $2}')
	fi

	# check for BROWSER variable, use xdg-open as fallback
	if [[ -z $BROWSER ]]; then
		export BROWSER=xdg-open
	fi

	# check if alternative root directory was given on commandline
	if [[ -r "$cache_dir/rofi-pass/last_used" ]] && [[ $1 == "--last-used" || $1 == "--show-last" ]]; then
		roots=("$(awk -F ': ' '{ print $1 }' "$cache_dir/rofi-pass/last_used")")
	elif [[ -n "$2" && "$1" == "--root" ]]; then
		custom_root=true; IFS=: read -r -a roots <<< "$2"
	elif [[ -n $root ]]; then
		custom_root=true; IFS=: read -r -a roots <<< "${root}"
	elif [[ -n ${PASSWORD_STORE_DIR} ]]; then
		roots=("${PASSWORD_STORE_DIR}")
	else
		roots=("$HOME/.password-store")
	fi
	roots_index=0
	roots_length=${#roots[@]}
	export root=${roots[$roots_index]}
	export PASSWORD_STORE_DIR="${root}"
	case $1 in
		--insert)
			insertPass
			;;
		--root)
			mainMenu
			;;
		--help)
			help_msg
			;;
		--last-used)
			if [[ -r "$cache_dir/rofi-pass/last_used" ]]; then
				entry="$(awk -F ': ' '{ print $2 }' "$cache_dir/rofi-pass/last_used")"
			fi
			mainMenu
			;;
		--show-last)
			if [[ -r "$cache_dir/rofi-pass/last_used" ]]; then
				selected_password="$(awk -F ': ' '{ print $2 }' "$cache_dir/rofi-pass/last_used")" viewEntry
			else
				mainMenu
			fi
			;;
		--bmarks)
			mainMenu --bmarks;
			;;
		*)
			mainMenu
			;;
	esac
}

main "$@"
