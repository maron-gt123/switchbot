#!/bin/bash
# ------region------
token="<トークン>"
secret="<シークレット>"
t=$(date +%s%3N)
nonce=$(uuidgen -r)
sign=$(echo -n ${token}${t}${nonce} | openssl dgst -sha256 -hmac ${secret} -binary | base64)
DEVICEID="<デバイスID>"
# ------------------

result=$(
    curl -s "https://api.switch-bot.com/v1.1/devices" \
      --header "Authorization: ${token}" \
      --header "sign: ${sign}" \
      --header "t: ${t}" \
      --header "nonce: ${nonce}" \
      --header "Content-Type: application/json; charset=utf8" | jq '.')

echo "$result"
