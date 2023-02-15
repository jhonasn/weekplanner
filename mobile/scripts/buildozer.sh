#!/bin/bash

buildozer -v android debug

mv ../.buildozer/android/platform/build-armeabi-v7a/dists/semanapp/build/outputs/apk/debug/semanapp-debug.apk ..
