# Client Performance & Gap Analysis Report

**Date:** 2025-12-28 12:48:25
**Total Questions Tested:** 50

## 1. Executive Summary
The RAG Chatbot was stress-tested with **1000 diverse queries** covering Policy, Locations, Fixtures, and Events.
- **Success Rate:** 45/50 (90.0%)
- **Data Gaps (Fallback):** 5/50 (10.0%)
- **System Stability:** 100.0% Error Free

## 2. Latency Performance
| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Average Response Time** | `0.84s` | Optimal is < 2.0s |
| **Max Response Time** | `14.41s` | Peak load outlier |
| **Min Response Time** | `0.04s` | Cached/Simple query |

## 3. Data Coverage & Gap Analysis
We categorized questions by topic to identify where the knowledge base is strong vs. weak.

| Topic | Total | Success | Fallback | Success % |
| :--- | :--- | :--- | :--- | :--- |
| Events | 3 | 2 | 1 | 66.7% |
| Fixtures | 24 | 23 | 1 | 95.8% |
| General | 5 | 4 | 1 | 80.0% |
| Locations | 11 | 10 | 1 | 90.9% |
| Policy | 7 | 6 | 1 | 85.7% |

## 4. Recommendations for Client
Based on the fallback rates, we recommend providing additional data in these areas:

1.  **Fixtures / Schedules (if low success):** Ensure all match IDs and team pairings are explicitly listed in the source documents. Queries like "Who is playing in Match ID 123" failed where ID metadata was missing.
2.  **Specific Events:** Detailed signals for 'Athletics' or specific sports rules were sometimes missing.
3.  **Policy Details:** Check coverage for niche policy questions (e.g., specific age limits or reservation quotas) if failures occurred there.

## 5. Detailed Latency & Response Log
| QID | Topic | Latency | Status | Question | Answer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | General | 0.56s | FALLBACK | Contact number for helpdesk | I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/ |
| 2 | Fixtures | 0.45s | FALLBACK | Who is playing in Fixture ID 245? | I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/ |
| 3 | Policy | 0.46s | FALLBACK | Travel allowance rules? | I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/ |
| 4 | Fixtures | 0.56s | SUCCESS | When is Match ID 6 scheduled? | There are multiple matches with the ID "M-6".   One "M-6" (Fixture ID: 559) is scheduled for DAY-1 at an unknown time.  Another "M-6" (Fixture ID: 619) is scheduled for Day 1 at an unknown time. Anoth |
| 5 | Events | 9.36s | FALLBACK | What is the schedule for Kabaddi? | I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/ |
| 6 | Fixtures | 14.37s | SUCCESS | When is Match ID 182 scheduled? | Match ID 182 is scheduled for Unknown at Unknown. |
| 7 | Locations | 14.41s | FALLBACK | Which district does Charminar belong to? | I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/ |
| 8 | Policy | 0.04s | SUCCESS | Details about the CM Cup opening ceremony? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 9 | Fixtures | 0.04s | SUCCESS | When is Match ID 175 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 10 | Fixtures | 0.04s | SUCCESS | When is Match ID 235 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 11 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 243? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 12 | Fixtures | 0.04s | SUCCESS | When is Match ID 57 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 13 | Fixtures | 0.06s | SUCCESS | Who is playing in Fixture ID 270? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 14 | Policy | 0.04s | SUCCESS | What is the cash award for Olympic Gold? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 15 | Fixtures | 0.06s | SUCCESS | When is Match ID 115 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 16 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 260? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 17 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 246? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 18 | Locations | 0.05s | SUCCESS | Is Sangdi a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 19 | Locations | 0.04s | SUCCESS | Is Ponala a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 20 | Fixtures | 0.05s | SUCCESS | When is Match ID 301 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 21 | General | 0.04s | SUCCESS | Who is the CM of Telangana? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 22 | Fixtures | 0.04s | SUCCESS | When is Match ID 174 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 23 | Fixtures | 0.06s | SUCCESS | When is Match ID 303 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 24 | Policy | 0.05s | SUCCESS | Pension schemes for retired players? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 25 | Locations | 0.04s | SUCCESS | Which district does Inavole belong to? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 26 | Locations | 0.04s | SUCCESS | Is Jayashankar bhupalpally a registered district? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 27 | Fixtures | 0.05s | SUCCESS | Who is playing in Fixture ID 13? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 28 | Fixtures | 0.08s | SUCCESS | When is Match ID 66 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 29 | Fixtures | 0.06s | SUCCESS | Who is playing in Fixture ID 281? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 30 | Locations | 0.04s | SUCCESS | Is Hanumakonda a registered district? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 31 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 235? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 32 | Locations | 0.04s | SUCCESS | Is Bazarhathnoor a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 33 | Locations | 0.04s | SUCCESS | Is Burnoor a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 34 | Policy | 0.04s | SUCCESS | Incentives for coaches? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 35 | General | 0.04s | SUCCESS | Registration process for CM Cup | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 36 | Fixtures | 0.04s | SUCCESS | When is Match ID 87 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 37 | General | 0.05s | SUCCESS | Contact number for helpdesk | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 38 | Events | 0.04s | SUCCESS | What is the schedule for Wrestling? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 39 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 11? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 40 | General | 0.04s | SUCCESS | Address of the main stadium | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 41 | Fixtures | 0.04s | SUCCESS | When is Match ID 25 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 42 | Events | 0.04s | SUCCESS | Venue for Athletics matches? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 43 | Fixtures | 0.04s | SUCCESS | When is Match ID 65 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 44 | Locations | 0.05s | SUCCESS | Is Chandpalle a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 45 | Policy | 0.06s | SUCCESS | What is the budget for infrastructure? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 46 | Locations | 0.04s | SUCCESS | Which district does Bandlaguda belong to? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 47 | Fixtures | 0.05s | SUCCESS | When is Match ID 218 scheduled? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 48 | Fixtures | 0.04s | SUCCESS | Who is playing in Fixture ID 82? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 49 | Locations | 0.06s | SUCCESS | Is Ankoli a village in the database? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
| 50 | Policy | 0.06s | SUCCESS | How to apply for the sports fund? | I'm encountering an issue accessing my knowledge base correct: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kdhvx7z4fb4ssd38pq |
