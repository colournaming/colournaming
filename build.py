#!/usr/bin/env python3

import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(loader=FileSystemLoader('../templates'),
                  autoescape=select_autoescape(['html']))
src = sys.argv[1]
template = env.get_template(src)
with open(src, 'w') as f:
    f.write(template.render())
