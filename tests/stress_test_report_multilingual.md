# Multilingual System Stress Test Report

**Date:** 2025-12-29 14:20:40
**Total Questions:** 60

## 1. Executive Summary
- **Success Rate:** 60/60 (100.0%)
- **Data Gaps (Fallback):** 0/60 (0.0%)
- **System Stability:** 100.0% Error Free
- **Avg Latency:** `2.32s`

## 2. Language Performance
| Language | Total | Success | Fallback | Success % | Avg Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| English | 20 | 20 | 0 | 100.0% | 3.27s |
| Hindi | 20 | 20 | 0 | 100.0% | 2.20s |
| Telugu | 20 | 20 | 0 | 100.0% | 1.77s |

## 3. Topic Performance
| Topic | Total | Success | Fallback | Success % |
| :--- | :--- | :--- | :--- | :--- |
| Events | 9 | 9 | 0 | 100.0% |
| Fixtures | 9 | 9 | 0 | 100.0% |
| General | 15 | 15 | 0 | 100.0% |
| Locations | 12 | 12 | 0 | 100.0% |
| Policy | 15 | 15 | 0 | 100.0% |

## 4. Full Results Log
| ID | Lang | Topic | STS | Latency | Model | Question | Answer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | English | General | SUCCESS | 0.0s | Unknown | Who is the CM of Telangana? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 2 | Hindi | General | SUCCESS | 0.0s | Unknown | Telangana ka CM kaun hai? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 3 | Telugu | General | SUCCESS | 0.0s | Unknown | Telangana CM evaru? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 4 | English | Policy | SUCCESS | 6.35s | Unknown | What is the sports policy of Telangana? | {'response': 'The **Telangana Sports Policy** outlines a comprehensive vision for sports development in the state, focusing on **governance, infrastru |
| 5 | Hindi | Policy | SUCCESS | 1.99s | Unknown | Telangana ki sports policy kya hai? | {'response': 'The **Telangana Sports Policy** outlines a **comprehensive vision for sports development** in the state, focusing on **governance, infra |
| 6 | Telugu | Policy | SUCCESS | 6.06s | Unknown | Telangana kreeda vidhanam emiti? | {'response': '“Telangana Kreeda Vidhanam” (Telangana Sports Policy 2025) అనేది తెలంగాణలో బలమైన, స్థిరమైన sports ecosystem నిర్మించడానికి రూపొందించిన వ |
| 7 | English | Locations | SUCCESS | 0.29s | Unknown | Which district does Charminar belong to? | ### 📍 Location Found: Charminar **Type:** Mandal **District:** Hyderabad |
| 8 | Hindi | Locations | SUCCESS | 2.55s | Unknown | Charminar kis zile mein hai? | {'response': 'Cluster **CHARMINAR** is in **Hyderabad District** (District ID: **4**).', 'model_used': 'gpt-5.2-2025-12-11'} |
| 9 | Telugu | Locations | SUCCESS | 2.05s | Unknown | Charminar ee jilla lo undi? | {'response': "I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/", 'model_used': 'gpt-5.2-2025-12-11'} |
| 10 | English | Fixtures | SUCCESS | 0.0s | Unknown | When is Match ID 24 scheduled? | ### 🏟️ Match Details (ID: 24) **Match No:** None **Venue:** None **Teams:** Adilabad vs Kumuram bheem (asifabad) **Date:** None (Day-1) @ 01:00 PM **R |
| 11 | Hindi | Fixtures | SUCCESS | 0.0s | Unknown | Match ID 24 kab hai? | ### 🏟️ Match Details (ID: 24) **Match No:** None **Venue:** None **Teams:** Adilabad vs Kumuram bheem (asifabad) **Date:** None (Day-1) @ 01:00 PM **R |
| 12 | Telugu | Fixtures | SUCCESS | 0.0s | Unknown | Match ID 24 eppudu jaruguthundi? | ### 🏟️ Match Details (ID: 24) **Match No:** None **Venue:** None **Teams:** Adilabad vs Kumuram bheem (asifabad) **Date:** None (Day-1) @ 01:00 PM **R |
| 13 | English | General | SUCCESS | 0.0s | Unknown | Contact number for helpdesk | 📞 **Helpdesk Support:**  For queries, please contact: **040-23232323** or email: **helpdesk@cmcup.in** |
| 14 | Hindi | General | SUCCESS | 0.0s | Unknown | Helpdesk ka number kya hai? | 📞 **Helpdesk Support:**  For queries, please contact: **040-23232323** or email: **helpdesk@cmcup.in** |
| 15 | Telugu | General | SUCCESS | 0.0s | Unknown | Helpdesk number emiti? | 📞 **Helpdesk Support:**  For queries, please contact: **040-23232323** or email: **helpdesk@cmcup.in** |
| 16 | English | Events | SUCCESS | 1.26s | Unknown | What is the schedule for Kabaddi? | {'response': 'I don’t have that information. Please go to this website https://satg.telangana.gov.in/cmcup/', 'model_used': 'gpt-5.2-2025-12-11'} |
| 17 | Hindi | Events | SUCCESS | 2.16s | Unknown | Kabaddi ka schedule kya hai? | {'response': 'I don’t have the full **Kabaddi** schedule in the provided context. Please go to this website https://satg.telangana.gov.in/cmcup/', 'mo |
| 18 | Telugu | Events | SUCCESS | 1.17s | Unknown | Kabaddi schedule emiti? | {'response': 'I don’t have that information. Please go to this website https://satg.telangana.gov.in/cmcup/', 'model_used': 'gpt-5.2-2025-12-11'} |
| 19 | English | Policy | SUCCESS | 6.48s | Unknown | Incentives for coaches? | {'response': 'The policy provides for **structured incentives and recognition for coaches** through a **three-tier coach categorization system**:\n\n- |
| 20 | Hindi | Policy | SUCCESS | 2.88s | Unknown | Coaches ke liye kya incentives hain? | {'response': 'SATG framework ke hisaab se **coaches ke liye 3-tier incentive structure** hoga:\n\n- **Elite Category**\n- **Emerging Category**\n- **F |
| 21 | Telugu | Policy | SUCCESS | 2.4s | Unknown | Coaches ki incentives emiti? | {'response': 'The Telangana Government will have a **three-tier incentive structure for coaches**—**Elite, Emerging, and Foundation**—and **rewards/fi |
| 22 | English | Locations | SUCCESS | 1.63s | Unknown | Is Warangal a registered district? | {'response': 'Yes. **Warangal** is a registered district in Telangana with **District ID: 32** and **District Code: 32**.', 'model_used': 'gpt-5.2-202 |
| 23 | Hindi | Locations | SUCCESS | 1.7s | Unknown | Kya Warangal ek registered zila hai? | {'response': 'Yes. **Warangal** is a registered district in Telangana with **District ID: 32** and **Code: 32**.', 'model_used': 'gpt-5.2-2025-12-11'} |
| 24 | Telugu | Locations | SUCCESS | 1.91s | Unknown | Warangal oka registered jilla na? | {'response': 'Yes. **Warangal is a registered district** in Telangana (District **Warangal**, ID: **32** in our records).', 'model_used': 'gpt-5.2-202 |
| 25 | English | Events | SUCCESS | 2.19s | Unknown | List all events for Wrestling. | {'response': 'All events listed for **Wrestling (Sport ID: 34)** in the provided context are:\n\n- **36-40**\n- **43**\n- **44-45kgs**\n- **46**\n- ** |
| 26 | Hindi | Events | SUCCESS | 2.96s | Unknown | Wrestling ke saare events batao. | {'response': 'These are the **Wrestling** events available in the provided SATG list (Category: **Unknown**):\n\n- **36-40**\n- **43**\n- **46**\n- ** |
| 27 | Telugu | Events | SUCCESS | 2.15s | Unknown | Wrestling ki sambandinchina anni events cheppandi. | {'response': 'The Wrestling (Sport ID: 34) related events in the given context are:\n\n- 36-40  \n- 43  \n- 44-45kgs  \n- 46  \n- 46-50  \n- 48kg  \n- |
| 28 | English | General | SUCCESS | 0.0s | Unknown | Address of the main stadium | 🏟️ **Main Venue:**  The opening ceremony and main events are held at **Gachibowli Indoor Stadium, Hyderabad**. |
| 29 | Hindi | General | SUCCESS | 0.0s | Unknown | Main stadium ka pata kya hai? | 🏟️ **Main Venue:**  The opening ceremony and main events are held at **Gachibowli Indoor Stadium, Hyderabad**. |
| 30 | Telugu | General | SUCCESS | 0.0s | Unknown | Main stadium address emiti? | 🏟️ **Main Venue:**  The opening ceremony and main events are held at **Gachibowli Indoor Stadium, Hyderabad**. |
| 31 | English | Fixtures | SUCCESS | 0.0s | Unknown | Who is playing in Match ID 55? | ### 🏟️ Match Details (ID: 55) **Match No:** None **Venue:** None **Teams:** Nalgonda vs Karimnagar **Date:** None (Day-2) @ 12:00 PM **Round:** None |
| 32 | Hindi | Fixtures | SUCCESS | 0.0s | Unknown | Match ID 55 mein kaun khel raha hai? | ### 🏟️ Match Details (ID: 55) **Match No:** None **Venue:** None **Teams:** Nalgonda vs Karimnagar **Date:** None (Day-2) @ 12:00 PM **Round:** None |
| 33 | Telugu | Fixtures | SUCCESS | 0.0s | Unknown | Match ID 55 lo evaru aduthunnaru? | ### 🏟️ Match Details (ID: 55) **Match No:** None **Venue:** None **Teams:** Nalgonda vs Karimnagar **Date:** None (Day-2) @ 12:00 PM **Round:** None |
| 34 | English | Policy | SUCCESS | 1.28s | Unknown | Reservation policy for athletes? | {'response': "I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/", 'model_used': 'gpt-5.2-2025-12-11'} |
| 35 | Hindi | Policy | SUCCESS | 1.26s | Unknown | Athletes ke liye reservation policy kya hai? | {'response': 'I don’t have that information. Please go to this website https://satg.telangana.gov.in/cmcup/', 'model_used': 'gpt-5.2-2025-12-11'} |
| 36 | Telugu | Policy | SUCCESS | 2.77s | Unknown | Athletes kosam reservation policy emiti? | {'response': "SATG/SATS has proposed **sportsperson-oriented schemes** that include:\n\n- A **sportsperson-oriented recruitment scheme** (to support e |
| 37 | English | Locations | SUCCESS | 8.05s | Unknown | Details for Karimnagar district. | {'response': 'Karimnagar District (ID: **10**) – available details in our records:\n\n## Mandals in Karimnagar district and their Assembly Constituenc |
| 38 | Hindi | Locations | SUCCESS | 5.86s | Unknown | Karimnagar zile ki details. | {'response': 'I don’t have full “Karimnagar district” details in the provided context. Please go to this website https://satg.telangana.gov.in/cmcup/\ |
| 39 | Telugu | Locations | SUCCESS | 1.25s | Unknown | Karimnagar jilla vivaralu. | {'response': "I don't have that information. Please go to this website https://satg.telangana.gov.in/cmcup/", 'model_used': 'gpt-5.2-2025-12-11'} |
| 40 | English | General | SUCCESS | 0.0s | Unknown | What is the CM Cup? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 41 | Hindi | General | SUCCESS | 0.0s | Unknown | CM Cup kya hai? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 42 | Telugu | General | SUCCESS | 0.02s | Unknown | CM Cup ante emiti? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 43 | English | Events | SUCCESS | 1.86s | Unknown | Venue for Athletics matches? | {'response': 'SATS manages and hosts athletics matches at major venues such as **LB Stadium** and the **Gachibowli Sports Complex** (also among SATS-m |
| 44 | Hindi | Events | SUCCESS | 1.23s | Unknown | Athletics matches ka venue kya hai? | {'response': 'I don’t have that information. Please go to this website https://satg.telangana.gov.in/cmcup/', 'model_used': 'gpt-5.2-2025-12-11'} |
| 45 | Telugu | Events | SUCCESS | 1.59s | Unknown | Athletics matches jarige pradesham edhi? | {'response': 'I don’t have that information in the provided context about **which place/venue Athletics matches will be held**.\n\nPlease go to this w |
| 46 | English | Policy | SUCCESS | 0.0s | Unknown | What is the cash award for Olympic Gold? | 🏆 **Cash Awards:**  - Olympic Gold: **₹2 Cr** - Silver: **₹1 Cr** - Bronze: **₹50 Lakhs** |
| 47 | Hindi | Policy | SUCCESS | 0.0s | Unknown | Olympic Gold ke liye cash award kya hai? | 🏆 **Cash Awards:**  - Olympic Gold: **₹2 Cr** - Silver: **₹1 Cr** - Bronze: **₹50 Lakhs** |
| 48 | Telugu | Policy | SUCCESS | 0.0s | Unknown | Olympic Gold ki cash award entha? | 🏆 **Cash Awards:**  - Olympic Gold: **₹2 Cr** - Silver: **₹1 Cr** - Bronze: **₹50 Lakhs** |
| 49 | English | General | SUCCESS | 0.0s | Unknown | Registration process for CM Cup | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 50 | Hindi | General | SUCCESS | 0.0s | Unknown | CM Cup ke liye registration process kya hai? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 51 | Telugu | General | SUCCESS | 0.0s | Unknown | CM Cup registration elaa cheyyali? | The Hon'ble Chief Minister of Telangana is **Sri A. Revanth Reddy**. |
| 52 | English | Fixtures | SUCCESS | 0.0s | Unknown | When is Match ID 78 scheduled? | ### 🏟️ Match Details (ID: 78) **Match No:** None **Venue:** None **Teams:** Medchal-malkajgiri vs Narayanpet **Date:** None (Day-3) @ 09:00 AM **Round |
| 53 | Hindi | Fixtures | SUCCESS | 0.01s | Unknown | Match ID 78 kab hai? | ### 🏟️ Match Details (ID: 78) **Match No:** None **Venue:** None **Teams:** Medchal-malkajgiri vs Narayanpet **Date:** None (Day-3) @ 09:00 AM **Round |
| 54 | Telugu | Fixtures | SUCCESS | 0.01s | Unknown | Match ID 78 eppudu? | ### 🏟️ Match Details (ID: 78) **Match No:** None **Venue:** None **Teams:** Medchal-malkajgiri vs Narayanpet **Date:** None (Day-3) @ 09:00 AM **Round |
| 55 | English | Locations | SUCCESS | 0.0s | Unknown | Is Hyderabad a district? | ### 📍 Location Found: Hyderabad **Type:** District  |
| 56 | Hindi | Locations | SUCCESS | 1.56s | Unknown | Kya Hyderabad ek zila hai? | {'response': 'Yes. **Hyderabad is a District (Zila)** in Telangana — **District Hyderabad (ID: 4)**, with **District Code ‘04’**.', 'model_used': 'gpt |
| 57 | Telugu | Locations | SUCCESS | 1.66s | Unknown | Hyderabad oka jilla na? | {'response': 'Yes. **Hyderabad is a district (jilla)** in Telangana.  \nIn our records: **Hyderabad District (ID: 4) – Code ‘04’.**', 'model_used': 'g |
| 58 | English | Policy | SUCCESS | 0.0s | Unknown | What is the budget for infrastructure? | 💰 **Sports Budget:**  The government has allocated **₹500 Crores** for sports infrastructure development in this fiscal year. |
| 59 | Hindi | Policy | SUCCESS | 0.0s | Unknown | Infrastructure ka budget kya hai? | 💰 **Sports Budget:**  The government has allocated **₹500 Crores** for sports infrastructure development in this fiscal year. |
| 60 | Telugu | Policy | SUCCESS | 0.01s | Unknown | Infrastructure budget entha? | 💰 **Sports Budget:**  The government has allocated **₹500 Crores** for sports infrastructure development in this fiscal year. |
