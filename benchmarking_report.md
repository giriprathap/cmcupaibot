# RAG Chatbot Benchmarking Report (GPT-4o)

**Date:** 2025-12-30

**Total Questions:** 500

**Overall Success Rate:** 11.8%

**Average Latency:** 0.04s


## 1. Outcome Distribution
| Outcome | Count | Percentage |
| :--- | :--- | :--- |
| Success | 59 | 11.8% |
| Connection Error | 441 | 88.2% |

## 2. Category Performance
| Category | Total | Success Rate | Weakness |
| :--- | :--- | :--- | :--- |
| 1. General Information (1–30) | 30 | 13.3% | HIGH |
| 2. Sports Hostel Admission (31–80) | 50 | 2.0% | HIGH |
| 3. Scholarships & Incentives (81–130) | 50 | 2.0% | HIGH |
| 4. Coach Recruitment & Eligibility (131–190) | 60 | 0.0% | HIGH |
| 5. Selection Trials & Performance (191–240) | 50 | 2.0% | HIGH |
| 6. Reservation, Domicile & Age Relaxation (241–290) | 50 | 6.0% | HIGH |
| 7. Facilities, Stadiums & Infrastructure (291–340) | 50 | 98.0% | None |
| 8. Grievance, Complaints & Payments (341–390) | 50 | 0.0% | HIGH |
| 9. Edge Cases, Confusing & Real-World Queries (391–500) | 110 | 0.0% | HIGH |

## 3. Weakest Areas (Sample Failures)

### 1. General Information (1–30) (Failures: 26)
*   **Q:** telangana sports authority ka main role kya hai?
    *   **Fallback:** Connection Error
*   **Q:** tsa kis department ke under aata hai?
    *   **Fallback:** Connection Error
*   **Q:** sports authority telangana office kaha hai?
    *   **Fallback:** Connection Error

### 2. Sports Hostel Admission (31–80) (Failures: 49)
*   **Q:** sports hostel admission ka process kya hai?
    *   **Fallback:** Connection Error
*   **Q:** telangana sports hostel admission kab start hota hai?
    *   **Fallback:** Connection Error
*   **Q:** hostel admission ke liye age limit kya hai?
    *   **Fallback:** Connection Error

### 3. Scholarships & Incentives (81–130) (Failures: 49)
*   **Q:** telangana sports scholarship kaun kaun le sakta hai?
    *   **Fallback:** Connection Error
*   **Q:** scholarship amount kitna hota hai?
    *   **Fallback:** Connection Error
*   **Q:** scholarship kab milti hai annually ya monthly?
    *   **Fallback:** Connection Error

### 4. Coach Recruitment & Eligibility (131–190) (Failures: 60)
*   **Q:** telangana sports authority coach recruitment kab hoti hai?
    *   **Fallback:** Connection Error
*   **Q:** tsa coach ke liye qualification kya chahiye?
    *   **Fallback:** Connection Error
*   **Q:** coach recruitment contract basis hota hai kya?
    *   **Fallback:** Connection Error

### 5. Selection Trials & Performance (191–240) (Failures: 49)
*   **Q:** sports trials telangana mein kab hote hain?
    *   **Fallback:** Connection Error
*   **Q:** tsa trials ka notification kaha publish hota hai?
    *   **Fallback:** Connection Error
*   **Q:** trials ke liye registration kaise karein?
    *   **Fallback:** Connection Error

### 6. Reservation, Domicile & Age Relaxation (241–290) (Failures: 47)
*   **Q:** tsa admission mein reservation policy kya hai?
    *   **Fallback:** Connection Error
*   **Q:** sports hostel admission mein sc st reservation hota hai kya?
    *   **Fallback:** Connection Error
*   **Q:** obc reservation tsa schemes mein apply hota hai kya?
    *   **Fallback:** Connection Error

### 7. Facilities, Stadiums & Infrastructure (291–340) (Failures: 1)
*   **Q:** tsa ke under kaun kaun se stadiums aate hain?
    *   **Fallback:** Connection Error

### 8. Grievance, Complaints & Payments (341–390) (Failures: 50)
*   **Q:** tsa grievance kaise file karein?
    *   **Fallback:** Connection Error
*   **Q:** scholarship payment delay ho jaye to kya karein?
    *   **Fallback:** Connection Error
*   **Q:** hostel issues ke liye complaint kaha karein?
    *   **Fallback:** Connection Error

### 9. Edge Cases, Confusing & Real-World Queries (391–500) (Failures: 110)
*   **Q:** trial miss ho gaya due to exam kya next chance milega?
    *   **Fallback:** Connection Error
*   **Q:** injury ke baad hostel se bahar kar denge kya?
    *   **Fallback:** Connection Error
*   **Q:** private academy mein train kar raha hoon phir bhi tsa hostel mil sakta hai kya?
    *   **Fallback:** Connection Error