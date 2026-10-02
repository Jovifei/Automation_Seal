# Replacement Runtime Source Receive Contract

Date: 2026-10-02

## Scope

This contract defines how `jovi-xianyu-commerce-v1` is received.

It does not claim that Runtime code has been reviewed before baseline upload.

## Required Before Review

Required:

- private GitHub repository exists;
- uploaded baseline commit is identified;
- commit SHA is immutable;
- local and remote references match;
- no secrets are included.

## Review Sequence

After baseline upload:

1. inspect repository tree;
2. inspect commit history;
3. inspect build/test configuration;
4. review security boundaries;
5. create bounded implementation plan.

## Not Allowed

- no real Xianyu writes;
- no payment enablement;
- no credential import;
- no overwrite of Governance main;
- no replacement of historical audit evidence.

## Current Status

Waiting for Runtime repository baseline publication.
