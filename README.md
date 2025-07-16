## 📋 SURVEYS API

### 1. `POST /surveys` — Create a New Survey

**Input:**

* `title` *(string, required)* — Title of the survey.
* `description` *(string, optional)* — Description or context for the survey.

**Design Considerations:**

* **Creation Date:**
  Store the creation date using a timestamp (e.g. `created_at`) field in the database. This enables tracking survey lifecycle and auditability.

* **Empty Surveys Allowed:**
  Allow creating surveys without initial questions. This provides flexibility for survey drafts and allows incremental construction of surveys. However, before making the survey publicly available, ensure it contains at least one question.

---

### 2. `POST /surveys/{survey_id}/questions` — Add a Question to a Survey

**Input:**

* `text` *(string, required)* — The question prompt.
* `question_type` *(string, required)* — One of the following:

  * `"text"` (Open-ended)
  * `"single_choice"`
  * `"multiple_choice"`

**Validation:**

* Ensure that the `survey_id` exists before attaching the question.

**Design Decisions:**

* **Storing `question_type`:**
  Use an **enumerated type (enum)** in the database. This:

  * Ensures type safety and valid values.
  * Provides better performance and clarity than using strings.
  * Reduces room for typos or mismatches in the code or database.

---

### 3. `POST /questions/{question_id}/options` — Add an Option to a Question

**Input:**

```json
{
  "text": "Very satisfied"
}
```

**Constraints:**

* This endpoint is only valid for questions of type:

  * `"single_choice"`
  * `"multiple_choice"`

**Validation:**

* Ensure that the `question_id` exists.
* Reject adding options to `"text"` (open-ended) questions.

**Enforcement Strategy:**

* **Application-level validation** is preferred:

  * Easier to maintain, update, and test.
  * Keeps business logic close to the service layer.
* Optionally, enforce with a **database-level constraint** (e.g. check constraint or foreign key with conditional logic) for additional robustness.

