#!/bin/bash

# Generate private key
openssl genrsa -out server.key 2048

# Generate certificate signing request
openssl req -new -key server.key -out server.csr -subj "/C=NL/ST=State/L=City/O=Organization/CN=accesscontrol.home"

# Generate self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# Set proper permissions
chmod 644 server.crt
chmod 600 server.key
