#!/bin/bash
# Vault Integration Script for GitHub Repos
# Adds Vault secrets to all GitHub repositories

set -e

# Vault AppRole credentials (from vault-infrastructure deployment)
VAULT_ADDR="http://vault.zazagaby.online"
VAULT_ROLE_ID="945989a3-d4ad-3a14-99ee-d6e0086d7c71"
VAULT_SECRET_ID="41e44bae-a83d-2914-324d-c657b5df4dad"

# Repositories to integrate
REPOS=(
    "fazaasro/vault-infrastructure"
    "fazaasro/aac-infrastructure"
    "fazaasro/aac-stack"
    "fazaasro/levy-agent"
    "fazaasro/overseer-monitoring"
    "fazaasro/project-levy-ssh"
)

echo "🔐 Vault Integration for GitHub Repos"
echo "========================================"
echo ""

# Add secrets to each repository
for repo in "${REPOS[@]}"; do
    echo "📦 Adding secrets to $repo"

    # Add VAULT_ADDR
    gh secret set -R "$repo" "VAULT_ADDR" --body "$VAULT_ADDR" 2>/dev/null || echo "  ⚠️  VAULT_ADDR already set"

    # Add VAULT_ROLE_ID
    gh secret set -R "$repo" "VAULT_ROLE_ID" --body "$VAULT_ROLE_ID" 2>/dev/null || echo "  ⚠️  VAULT_ROLE_ID already set"

    # Add VAULT_SECRET_ID
    gh secret set -R "$repo" "VAULT_SECRET_ID" --body "$VAULT_SECRET_ID" 2>/dev/null || echo "  ⚠️  VAULT_SECRET_ID already set"

    echo "  ✅ Secrets added to $repo"
    echo ""
done

echo "========================================"
echo "✅ Vault integration complete for all repos"
echo ""
echo "Next steps:"
echo "1. Add GitHub Actions workflows to each repo"
echo "2. Use hashicorp/vault-action@v3 to retrieve secrets"
echo "3. Example workflow:"
echo ""
cat << 'EOF'
  - name: Retrieve secrets from Vault
    uses: hashicorp/vault-action@v3
    with:
      url: ${{ secrets.VAULT_ADDR }}
      method: approle
      roleId: ${{ secrets.VAULT_ROLE_ID }}
      secretId: ${{ secrets.VAULT_SECRET_ID }}
      secrets: |
        secret/data/glm-api-key api_key | GLM_API_KEY ;
        secret/data/cloudflare-api-token api_token | CF_API_TOKEN ;
        secret/data/cloudflare-api-token zone_id | CF_ZONE_ID
EOF
