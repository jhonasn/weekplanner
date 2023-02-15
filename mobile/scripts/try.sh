#!/bin/bash

sudo -v
#sudo docker run .
sudo docker run \
  --volume "$HOME/.buildozer":/home/user/.buildozer \
  --volume "$PWD":/home/user/hostcwd \
	kivy/buildozer
	#--entrypoint ~/projects/semanapp/buildozer.sh
