#!/usr/bin/env bash

set -e
unset GIT_DIR

fail() {
    echo $1
    exit 1
}

which pandoc &>/dev/null \
    || fail 'please install pandoc'

WORK_DIR='./cryptography'

OUT_FILE="${WORK_DIR}/resources/notes.pdf"
TMP_FILE=$(mktemp)
rm -f ${TMP_FILE}
touch ${TMP_FILE}

for week in $(ls ${WORK_DIR} | grep 'week_' | sort -n); do
    cat ${WORK_DIR}/${week}/notes.md | tee >> $TMP_FILE
    echo >> $TMP_FILE
done

pandoc -o ${OUT_FILE} ${TMP_FILE} \
    && git add ${OUT_FILE} \
    && rm -f ${TMP_FILE}
