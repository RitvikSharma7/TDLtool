#!/bin/bash

fileName=tdlcli
header='###################################################################################'
title='#  Welcome to the TDL tool.\n# This tool will help you manage your task and time.'

echo -e "${header}\n${title}\n${header}"

	
ui()
{
  select option in ADD DELETE SEE QUIT; do

    case $option in
      ADD)
        add_task
        ;;

      DELETE)
        delete_task
        ;;

      SEE)
        see_tasks
        ;;

      QUIT)
	echo "Quitting...."
        exit 0
        ;;

      *)
	echo "Invalid operation."
        ;;
    esac
   done
}

add_task()
{
  echo "Please add task description required."
  read -r task
  task_val='^[a-zA-Z]+(?: [a-zA-Z]+)*$'
	
  echo "Please add when it should be done in M-D-Y-T format"
  read -r date
  date_val='^([1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-(\d{4})-([1-9]|1[0-2]):([0-9]{2}) (AM|PM)$'

  if [[ "$task" =~ $task_val && "$date_val" =~ $date_val ]]; then
    echo "$task------->$date" >> "$fileName"
    echo "Task added to list."
  else
    echo "Invalid format."
  fi
}


delete_task()
{
  echo "Please delete task on description or date."
  read -r desc
  last_line=$(wc -l < "$fileName")
  input_val='^[0-9]+$'

  if [[ -s "$fileName" ]]; then
    if grep -q "$desc" "$fileName"; then
      echo "Matching task(s) found:"
      grep -n "$desc" "$fileName"
      echo "what task do you want to delete in line:"
      read -r linenum
      if [[ ${linenum} =~ $input_val ]] && [[ ${linenum} -le last_line ]]; then
       sed -i "${linenum}d" "$fileName"
       echo "Task deleted."
      else
        echo "Invalid task line."
      fi
    else
      echo "Task not found."	
    fi
 else
    echo "No tasks in list."
  fi
}

see_tasks()
{
  if [[ ! -s "$fileName" ]]; then
    echo "File has no tasks to fetch."
  else
    echo "-------------------------------------"
    cat "$fileName" | sed = | sed 'N;s/\n/.) /'
    echo "-------------------------------------"
  fi    
}

main()
{
  ui
}

main

