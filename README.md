# Sleepy Time Stories

An agentic AI bedtime-story app for children aged 3–8. A parent picks a hero, place and length, or sets a goal for the week; an AI agent plans and writes a calm story, a safety reviewer checks it, and it is narrated over nature music that fades to silence.

## Why

Tired parents run out of stories, screens keep children awake, and most audio apps are generic, English-only and full of ads.

## What makes it agentic

The agent turns a parent's goal into a 7-night story plan, remembers how each night went ("fell asleep" / "still awake"), and adapts the next story's length, pace and sounds.

## Safety by design

- The child never chats with the AI; only a consenting parent uses the app (India DPDP Act).
- The AI never receives the child's name.
- Every story passes an AI safety reviewer plus rule-based checks.
- Stories that fail are replaced by a pre-approved story.
- Minimal data, stored in India. No ads.

## Tech stack

| Part | Technology |
| --- | --- |
| Mobile app | React Native |
| Web app | React |
| Core API (owns child data) | Python FastAPI |
| Agent API (story agents, never sees names) | Python FastAPI + LangGraph |
| AI | Claude on Vertex AI |
| Cloud | Google Cloud: Cloud Run, Cloud SQL Postgres (Mumbai), Cloud Storage, Text-to-Speech |

## Roadmap

| Week | Focus |
| --- | --- |
| 1 | Discover and design |
| 2 | Story engine |
| 3 | Apps and data |
| 4 | Pilot with 10 families |

## Status

Week 1 in progress.

## Author

Aghil Menon Udayakumaran, AI Specialist.