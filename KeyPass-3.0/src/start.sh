#!/bin/bash
docker build --tag ctfuni-keepass3 . && docker run -it -p 4235:4235 ctfuni-keepass3