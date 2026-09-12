# Security remediation

## Current branch

- Removed DB usernames/passwords and Flask signing secrets from DEV and PROD YAML. Supply fresh values through the environment; `.env.example` contains fake placeholders.
- Removed both `certs/cert.pem` and `certs/key.pem`. OpenSSL parsed both as public X.509 certificates, byte-identical and expired on 2021-05-03. Neither contained a private-key block. This is not evidence of an exposed private key.
- Excluded local environment files, PEM files, and certificates from git and the Docker build context.
- Preserve DEV/PROD logging, validate required configuration, and explicitly constrain JWT verification to HS256.

## Required operator actions

1. Rotate all database passwords formerly stored in `dev-config.yml` and `prod-config.yml`, including any reused credentials. Review database accounts and access logs; retire unused accounts.
2. Replace each historical Flask/JWT signing secret. Invalidate existing tokens and sessions that depended on the old secret.
3. Review deployment secrets and historic branches/tags for additional exposure. The old public certificate files alone do not establish a private-key compromise; if a matching private key was exposed elsewhere, revoke/reissue that key pair separately.
4. Update deployments from a secret store or untracked environment configuration. Do not paste old values into tickets, PRs, logs, or discussions.

Rotation and deployment changes have not been performed by this PR.

## Git history requires separate remediation

Ordinary deletion leaves old YAML credentials available in existing commits, refs, clones, forks, caches, and PR diffs. This PR does not rewrite history or force-push. Rotate first. Repository owners should separately coordinate an approved history-cleanup operation with collaborators and GitHub support where necessary, including affected refs and cached views. Verify afterward with a secret scanner whose output redacts values. Do not assume history cleanup revokes a credential or erases all copies.

## Disposable local TLS (optional)

The default local HTTP server needs no certificate. If HTTPS is needed for local testing:

```sh
mkdir -p certs
umask 077
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout certs/key.pem -out certs/cert.pem -subj '/CN=localhost' \
  -addext 'subjectAltName=DNS:localhost,IP:127.0.0.1'
python -m flask --app main run --host 127.0.0.1 --cert certs/cert.pem --key certs/key.pem
```

Load the environment first. This generates a self-signed development-only certificate; never commit either generated file or use the key in a shared deployment.

## Remaining application risks

Unsalted password hashing, incomplete endpoint authorization, broad CORS, Socket.IO payload logging/unauthenticated writes, and prototype error handling remain. Resolve these before using real educational records. This change is not a full security audit.
