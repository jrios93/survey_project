## 📋 SURVEYS API

### 1. `POST /surveys` — Create a New Survey

**Input:**

* `title` *(string, required)*.
* `description` *(string, optional)*.
* `is_active` *(true,optional)*.

---

### 2. `POST /surveys/:survey_id/questions` — Add a Question to a Survey

**Input:**

* `text` *(string, required)*.
* `question_type` *(int, required)*.
* `is_active` *(true,optional)*.

**Path Params:**
* `survey_id` *(int,required)*

---

### 3. `POST /surveys/questions/:question_id/options` — Add an Option to a Question

**Input:**

* `text` *(string, required)*.


**Path Params:**
* `question_id` *(int,required)*

### 4. `POST /surveys/questions/question_type` — Create Question Type

**Input:**

* `title` *(string, required)*.
* `description` *(string, optional)*.
* `allow_options` *(true,optional)*.

### 5. `GET /surveys/question_type` - List Question Type

### 6. `GET /surveys/:survey_id` - Get Survey by Id

**Path Params:**
* `survey_id` *(int,required)*
