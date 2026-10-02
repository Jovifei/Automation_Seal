# GitHub Bidirectional Handoff Contract

Date: 2026-10-02

## Purpose

Establish the next governance phase for the replacement Runtime handoff.

This document does not import Runtime source code and does not change any real-platform permission.

## Authority Flow

Governance repository:

`Jovifei/Automation_Seal`

Role:
- planning
- acceptance criteria
- review gates
- rollback policy
- source receiving contract

Replacement Runtime repository:

`Jovifei/jovi-xianyu-commerce-v1`

Role:
- implementation source
- build/test execution
- runtime evidence

## Current Boundary

The replacement Runtime baseline must be uploaded and verified before any Runtime review claim.

A local commit identifier alone is not sufficient evidence.

Required evidence:

- GitHub repository identity
- commit SHA
- branch/ref
- tree comparison
- build/test output

## Replacement Acceptance

The acceptance process is:

1. Local Runtime pushes reviewed baseline.
2. Governance records received SHA and source identity.
3. Remote review checks uploaded baseline.
4. Local Codex pulls review result.
5. Local Codex builds/tests and reports execution evidence.
6. Remote review validates returned evidence.

## Safety Boundary

Remain unchanged:

- issued_from_human=false
- production_integration_allowed=false
- real_payment=false
- real_customer=false
- xianyu=false
- auto_delivery=false
- n8n_production=false

No credentials, cookies, tokens, or real platform data belong in this repository.

## Rollback

Rollback means:

- stop accepting the new Runtime baseline;
- preserve previous Governance evidence;
- preserve history;
- never rewrite Git history to force acceptance.
