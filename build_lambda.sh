#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [[ -h "${SOURCE}" ]]; do # resolve ${SOURCE} until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "${SOURCE}" )" && pwd )"
    SOURCE="$(readlink "${SOURCE}")"
    [[ ${SOURCE} != /* ]] && SOURCE="${DIR}/${SOURCE}" # if ${SOURCE} was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
CURRENT_DIR="$( cd -P "$( dirname "${SOURCE}" )" && pwd )"


#reset the build directory
rm -r "${CURRENT_DIR}/build"
mkdir -p "${CURRENT_DIR}/build"

#reset the dist directory
rm -r "${CURRENT_DIR}/dist"
mkdir -p "${CURRENT_DIR}/dist"

cp "${CURRENT_DIR}/lambda_handler/"*.py "${CURRENT_DIR}/build"

cd "${CURRENT_DIR}/build"

zip -r "lambda.zip" .

cp "${CURRENT_DIR}/build/lambda.zip" "${CURRENT_DIR}/dist"
