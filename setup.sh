echo "[ `date +%H:%M ` ]": "START"
echo "[ `date +%H:%M ` ]": "CREATING VIRTUAL ENV"
python3 -m venv .venv
echo "[ `date +%H:%M ` ]": "ACTIVATING VIRTUAL ENV"
source .venv/bin/activate
echo "[ `date +%H:%M ` ]": "INSTALLING REQUIREMENTS"
pip install -r requirements.txt
echo "[ `date +%H:%M ` ]": "END"
