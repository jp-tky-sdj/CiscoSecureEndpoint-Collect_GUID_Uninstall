# Read in the client_id and client_secret if they are not already set.
[ -z "$client_id" ] && read -p "client_id: " client_id
[ -z "$client_secret" ] && read -p "client_secret: " client_secret

# Call the SecureX token endpoint and store the result in a variable.
result=$(curl -s 'https://visibility.apjc.amp.cisco.com/iroh/oauth2/token' \
     --user "${client_id}:${client_secret}" \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --header 'Accept: application/json' \
     -d 'grant_type=client_credentials')

# Extract the access_token from the result.
export SECUREX_TOKEN=$(echo "$result" | jq -r .access_token)

# Print the result.
[ -x "$(command -v jq)" ] && echo "$result" | jq . || echo "$result"


# Call the Secure Endpoint token endpoint and store the result in a variable.
result=$(curl -s 'https://api.apjc.amp.cisco.com/v3/access_tokens' \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $SECUREX_TOKEN" \
     -d 'grant_type=client_credentials')

# Extract the access_token from the result.
export BEARER_TOKEN=$(echo "$result" | jq -r .access_token)

# Print the result.
[ -x "$(command -v jq)" ] && echo "$result" | jq . || echo "$result"

# Call the Secure Endpoint API and store the result in a variable.
result=$(curl -s 'https://api.apjc.amp.cisco.com/v3/organizations?size=10' \
                --header "Authorization: Bearer ${BEARER_TOKEN}")

# Print the result.
[ -x "$(command -v jq)" ] && echo "$result" | jq . || echo "$result"

