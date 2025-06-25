if [ ${0##*/} == ${BASH_SOURCE[0]##*/} ]; then 
    echo "WARNING"
    echo "This script is not meant to be executed directly!"
    echo "Use this script only by sourcing it."
    echo
    exit 1
fi
source ./.linux_env/bin/activate
