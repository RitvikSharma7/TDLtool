#!/bin/bash

fileName=tdlcli
	
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
	
  echo "Please add when it should be done in M-D-Y-T format"
  read -r date
  
  echo "$task------->$date" >> "$fileName"
  echo "Task added to list."
}


delete_task()
{
  echo "Please delete task on description or date."
  read -r desc

  if [[ -s "$fileName" ]]; then
    if grep -q "$desc" "$fileName"; then
      sed -i "/$desc/d" "$fileName"
      echo "Task deleted."
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
    cat "$fileName"
    echo "-------------------------------------"
  fi    
}

main()
{
  ui
}

main

