# GitHub Repo Intelligence Analyzer

## 📌 Overview

The **GitHub Repo Intelligence Analyzer** is a backend system that evaluates any GitHub repository and generates a structured analysis report using a combination of deterministic scoring rules and AI-based reasoning.

It helps assess a repository’s:
- Popularity
- Activity level
- Codebase health
- Overall quality verdict
- AI-generated qualitative insights

---

## ⚙️ What the System Does

Given a GitHub repository URL, the system:

1. Fetches repository metadata from GitHub API  
2. Computes deterministic scores:
   - Popularity Score (stars + forks)
   - Activity Score (open issues heuristic)
   - Health Score (description + language presence)
   - Final weighted score + verdict  
3. Builds a structured prompt using repository + score data  
4. Sends the prompt to a Large Language Model (via HuggingFace Router API)  
5. Returns:
   - Repository details
   - Computed scores
   - AI-generated structured analysis (summary, strengths, weaknesses, audience, verdict)

---

## 🧠 Initial Implementation (Before Refactor)

The initial version of the system was built as a straightforward FastAPI pipeline where:

- Business logic, API calls, and AI integration were tightly coupled
- GitHub API logic lived inside service functions
- LLM calls were directly embedded in service layer
- Prompt generation and scoring logic were mixed together
- FastAPI endpoint orchestrated the entire flow directly

### ❌ Limitations of initial design:
- Tight coupling between components
- Hard to test individual parts
- Difficult to swap external services (GitHub / LLM)
- Business logic not isolated from infrastructure
- Low maintainability as system grows

---

## 🏗️ Refactored Architecture (Hexagonal Design)

The project was later refactored using **Hexagonal Architecture (Ports & Adapters)** to improve modularity, testability, and scalability.

### 🧩 Architecture Layers
      [ FastAPI ]
           │
 ┌─────────┴─────────┐
 │   Application     │
 │   (Use Case)     │
 └─────────┬─────────┘
           │
    ┌──────┴──────┐
    │   Domain    │
    │ (Core Logic)│
    └──────┬──────┘
           │
 ┌─────────┴─────────┐
 │      Ports        │
 └─────────┬─────────┘
           │
 ┌─────────┴─────────┐
 │    Adapters       │
 │ (GitHub / LLM)    │
 └───────────────────┘

 
---

## 🧠 Key Architectural Components

### 1. Domain Layer
Contains pure business logic:
- Repository scoring system
- Verdict calculation rules
- Prompt generation logic
- Data models

👉 No external dependencies

---

### 2. Ports (Interfaces)
Define contracts for external systems:
- `GitHubPort` → Fetch repository data
- `LLMPort` → Generate AI analysis

👉 No implementation, only abstraction

---

### 3. Adapters (Implementations)
Concrete integrations:
- GitHub Adapter → GitHub REST API (httpx)
- HuggingFace LLM Adapter → LLM inference API

👉 Replaceable without changing core logic

---

### 4. Application Layer (Use Case)
Orchestrates full workflow:
- Fetch repository data via GitHubPort
- Compute scores using domain logic
- Build prompt
- Call LLM via LLMPort
- Return structured response

---

### 5. API Layer (FastAPI)
Simple interface layer:
- Accepts GitHub URL request
- Calls application use case
- Returns structured response

👉 No business logic inside controller

---

## 🚀 Benefits of Hexagonal Refactor

- ✅ Fully decoupled architecture  
- ✅ Easy to test business logic in isolation  
- ✅ Swappable external services (GitHub / LLM)  
- ✅ Clear separation of concerns  
- ✅ Scalable for future features (caching, DB, new LLMs)  
- ✅ Framework-independent core logic  

---

## 🔄 Before vs After

| Aspect | Initial Design | Hexagonal Design |
|--------|---------------|------------------|
| Structure | Monolithic service layer | Layered architecture |
| Coupling | High | Low |
| Testability | Difficult | Easy |
| Flexibility | Low | High |
| External APIs | Direct dependency | Abstracted via ports |

---

## 📦 Tech Stack

- FastAPI
- Python
- httpx
- HuggingFace Inference API
- Pydantic
- Hexagonal Architecture (Ports & Adapters)

---

## 📌 Example Use Case

### Request:
```json
POST /repo/analyze
{
  "url": "https://github.com/user/repo"
}

