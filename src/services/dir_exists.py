#!/bin/bash

from datetime import datetime

# Check if the directory for today's date exists

#directory=$(python3 -c "from datetime import datetime; print('/home/wrf/deployed/webb-downloading/wx_presentation/images/' + datetime.now().strftime('%Y%m%d'))")
directory=$(python3 -c "from datetime import datetime; print(\"/home/wrf/deployed/webb-downloading/wx_presentation/images/\" + datetime.now().strftime('%Y%m%d'))")
if [ -d "$directory" ]; then
#if [ -d "/home/wrf/deployed/webb-downloading/wx_presentation/images/$(date +%Y%m%d)" ]; then
  echo "Directory exists."
else
  echo "Directory does not exist."
fi