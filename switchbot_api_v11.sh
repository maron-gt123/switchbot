#!/bin/bash
# ------region------
TOKEN="<トークン>"
SECRET="<シークレット>"
T=$(date +%s%3N)
NONCE=$(uuidgen -r)
SIGN=$(echo -n ${TOKEN}${T}${NONCE} | openssl dgst -sha256 -hmac ${SECRET} -binary | base64)
# ------------------

RESULT=$(
    curl -s "https://api.switch-bot.com/v1.1/devices" \
      --header "Authorization: ${TOKEN}" \
      --header "sign: ${SIGN}" \
      --header "t: ${T}" \
      --header "nonce: ${NONCE}" \
      --header "Content-Type: application/json; charset=utf8")

echo "$RESULT"
