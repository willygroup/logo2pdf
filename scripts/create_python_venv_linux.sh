if [ ${0##*/} == ${BASH_SOURCE[0]##*/} ]; then 
    echo "WARNING"
    echo "This script is not meant to be executed directly!"
    echo "Use this script only by sourcing it."
    echo
    exit 1
fi
python -m venv .linux_env && . ./.linux_env/bin/activate && \
python -m pip install --upgrade pip && \
pip install wheel && \
pip install -r requirements.txt
