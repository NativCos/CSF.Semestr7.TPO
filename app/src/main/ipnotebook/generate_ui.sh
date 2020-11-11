#!/usr/bin/env bash


pyuic5 -o ${0%/*}/mainwindow.py ${0%/*}/resources/mainwindow.ui
