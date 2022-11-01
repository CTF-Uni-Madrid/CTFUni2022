#!/bin/bash
docker build --tag ctfuni-notebook .
docker run -it -p 5000:5000 ctfuni-notebook