#!/bin/bash
# Run TRICKLE BOT banner generator
cd /home/hermes
pip install Pillow -q 2>/dev/null
python3 /home/hermes/.hermes/hermes-agent/../tools/trickle_bot_banner.py 2>&1 || \
python3 -c "import subprocess; subprocess.run(['pip','install','Pillow','-q']); exec(open('/home/hermes/.hermes/hermes-agent/tools/trickle_bot_banner.py').read().replace('/home/hermes/trickle_bot_banner.png','/home/hermes/trickle_bot_banner.png'))"