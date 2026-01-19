#!/bin/sh

# ISM Policies Application Script
# This script applies ISM policies to OpenSearch

set -e

OPENSEARCH_HOST=${OPENSEARCH_HOST:-http://localhost:9200}
POLICY_DIR=$(dirname "$0")

echo "Waiting for OpenSearch to be ready..."
until curl -sf "$OPENSEARCH_HOST/_cluster/health" > /dev/null 2>&1; do
  echo "Waiting for OpenSearch..."
  sleep 2
done

echo "OpenSearch is ready!"

# Function to apply a policy
apply_policy() {
  local policy_file=$1
  local policy_id=$(basename "$policy_file" .json)
  
  echo "Applying policy: $policy_id from $policy_file"
  
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X PUT "$OPENSEARCH_HOST/_plugins/_ism/policies/$policy_id?pretty" \
    -H "Content-Type: application/json" \
    -d @"$policy_file")

  if [ "$status" = "200" ] || [ "$status" = "201" ]; then
    echo "=> Policy $policy_id applied successfully"
  elif [ "$status" = "409" ]; then
    echo "=> Policy $policy_id already exists (conflict)"
  else
    echo "=> Failed to apply policy $policy_id (HTTP $status)"
    return 1
  fi
}

# Apply all policies
echo "Applying ISM policies..."

# Apply log policy
apply_policy "$POLICY_DIR/log-policy.json"

# Apply metric policy
apply_policy "$POLICY_DIR/metric-policy.json"

# Apply trace policy
apply_policy "$POLICY_DIR/trace-policy.json"

echo "All policies applied successfully!"
