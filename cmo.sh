#!/bin/bash

python manage.py count_model_objects 2> $(date +'%F').dat
