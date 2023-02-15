p4a apk --private .. \
	--package=org.jojo.semanapp \
	--name "My library" \
	--version 0.1 \
	--bootstrap=service_library \
	--requirements=python3 \
	--release \
	--service=myservice:service.py \
	--arch=arm64-v8a \
	--arch=armeabi-v7a
