# Implementation Plan v2: UX Overhaul & Smart Features

## 1. Overview
This phase focuses on elevating the user experience (UX) to a "premium" standard and adding smart engagement features. We will transform the UI from a functional prototype to a polished, modern interface, and implement "Predictive Follow-up Questions" to guide the user conversation.

## 2. Key Features

### A. UX/UI Redesign (Premium & Clean)
*   **Goal**: Make the chatbot feel "comfortable" and "professional".
*   **Changes**:
    *   **Typography**: Increase readability with better line heights and font sizing (Inter font).
    *   **Chat Bubbles**: Modern "rounded-xl" style, distinct colors for clarity (User: University Red, Bot: White/Gray).
    *   **Shadows & Depth**: Add subtle drop shadows to the chat window and bubbles to make them pop.
    *   **Feedback UI**: Make Thumbs Up/Down icons always visible and intuitive.

### B. Smart Follow-up Suggestions (Tail Queries)
*   **Goal**: Anticipate what the user wants to ask next.
*   **Logic**:
    *   Modify `AI Engine` to generate 3 short, relevant follow-up questions for every response.
    *   **Structure**: The LLM will return JSON: `{ "text": "Answer...", "suggestions": ["Q1", "Q2", "Q3"] }`.
    *   **UI**: Render these as clickable "chips" immediately after the AI response.

### C. Feedback Loop Enhancement
*   **Goal**: Ensure user feedback (Thumbs Up/Down) is captured and acknowledged.
*   **Changes**:
    *   Visual confirmation ("Thanks for feedback!") upon clicking.
    *   Ensure data is sent to `FeedbackEngine`.

## 3. Technical Changes

### Backend (`ai_engine.py`)
*   **Prompt Engineering**: Update `qa_template` to enforce JSON output with `suggestions` field.
*   **Response Parsing**: Ensure `get_response` handles the JSON and returns a structured object (or passes it through to Flask).

### Backend (`main.py`)
*   Update `/api/chat` to pass the structured response (text + suggestions) to the frontend.

### Frontend (`code_hompage.html`)
*   **HTML/CSS**: Redesign the chat window container, header, and message list.
*   **JS**:
    *   Handle the new JSON response format.
    *   Dynamically create "Suggestion Chips" below AI messages.
    *   Improve the "Thinking..." animation.

## 4. Verification Plan
*   **Manual Test**: Run the app and ask "Tell me about Computer Science".
    *   **Expectation**:
        *   UI looks cleaner.
        *   Answer is accurate.
        *   **3 Suggestion Chips** appear below (e.g., "Fees?", "Entry Req?", "Scholarships?").
        *   Clicking a chip sends that message immediately.
