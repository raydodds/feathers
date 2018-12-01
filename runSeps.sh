#!/bin/bash

SEP_SCRIPT_DIR='~/Courses/CSCI716/project/image_proc'

SEP_SCRIPT='feather_sep.py'

function rec_sep()
{
	local stuff=`ls $search_dir`;
	
	local here=`pwd`;

	for entry in $stuff; 
	do
		if [[ -f $entry ]] ;
		then
	    	echo "File" $entry
			
			# Make a dir to store the files
			local edir=`echo $entry | cut -d'.' -f1`_feath
			mkdir edir
			cd edir

			# Run the file seperation
			python3 $SEP_SCRIPT_DIR/$SEP_SCRIPT ../$entry

			cd ..


		elif [[ -d $entry && $entry != *'feath' ]] ; 
		then
			echo "Dir" $entry
			cd $entry
			rec_sep
			cd ..
		else
			echo "Doh!"
		fi
	done

}

rec_sep
