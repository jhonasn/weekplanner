sudo docker run --interactive --tty --rm \
	--volume "$HOME/.buildozer":/home/user/.buildozer \
	--volume "$PWD":/home/user/hostcwd \
	--entrypoint /bin/bash kivy/buildozer
