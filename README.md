# smart_resume_analyzer

```mermaid
graph TD
    A[Start] --> B{User enters job description};
    B -- Job description entered --> C{User uploads resume PDF};
    C -- Resume uploaded --> D{User clicks 'Analyze My Resume' button};
    D -- Button clicked --> E{Are job description and resume present?};
    E -- Yes --> F{Has the user reached the query limit?};
    F -- Yes --> M[Display warning message: 'Query limit reached. Please try again later.'];
    F -- No --> G[Increment query count];
    G --> H[Extract text from PDF];
    H --> I[Send resume text and job description to Gemini model];
    I --> J[Gemini model analyzes resume against job description];
    J --> K[Generate report: match %, matched keywords, missing keywords, summary, improvement suggestions];
    K --> L[Display report to user];
    E -- No --> N[Display warning: 'Please upload a resume and enter a job description'];
    L --> A;
    M --> A;
    N --> A;
    ```
