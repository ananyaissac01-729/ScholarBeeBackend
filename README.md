# ScholarBee AI Backend

FastAPI backend scaffold for the ScholarBee AI final-year project. All bundled courses are labelled demo data. The recommendation algorithm is an educational ABC-inspired prototype, not a verified reproduction of the paper. No research outcomes or performance metrics are claimed.

## Project structure

```text
app/
  main.py                    FastAPI application and CORS configuration
  api/routes/                HTTP endpoints (health, courses, recommendations, feedback)
  core/config.py             Environment-backed settings
  data/demo_courses.py       Clearly labelled sample courses
  models/                    Pydantic input and output validation
  algorithms/iabco.py        Isolated, deterministic ABC-inspired ranking prototype
  services/                  Recommendation and feedback business logic
tests/                       Algorithm, feedback, and API tests
requirements.txt             Runtime and test dependencies
```

## Dependencies

- **FastAPI** defines the REST API and interactive OpenAPI docs.
- **Uvicorn** runs the app locally.
- **Pydantic Settings** reads configuration from environment variables or `.env`.
- **pytest** and **HTTPX** run the unit and API tests.

## Windows setup

From PowerShell in this folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API. Run tests with `python -m pytest -q`.

## Endpoints

- `GET /health` — service status.
- `GET /courses` — demo course catalogue; every item includes `demo_data: true`.
- `POST /recommendations` — accepts `student_id`, `preferences` (`interests`, `skills`, and `preferred_difficulty`) and optional `limit` (1–20).
- `POST /feedback` — accepts `student_id`, `course_id`, and `outcome` (`completed`, `started`, `skipped`, or `disliked`).

Example recommendation request:

```json
{
  "student_id": "student-123",
  "preferences": {
    "interests": ["data", "ai"],
    "skills": ["python"],
    "preferred_difficulty": "beginner"
  },
  "limit": 3
}
```

## Feedback reward rules

The demo reinforcement-learning component records each event and applies fixed rewards: `completed` = `+1.0`, `started` = `+0.3`, `skipped` = `-0.5`, and `disliked` = `-1.0`. For the same student/course pair, the mean reward creates a bounded adjustment of at most `±0.15` to that course's next match score. This is a documented feedback heuristic, not a trained reinforcement-learning policy. Events are stored in memory and disappear when the server restarts; production use needs durable, access-controlled storage.

The IABCO-like module is independently testable and intentionally identifies itself as a prototype. Verify the paper's exact algorithm, privacy guarantees, and experimental protocol before describing the implementation as research-complete.

## FlutterFlow and CORS

The API uses JSON REST requests and Pydantic schemas, so a FlutterFlow app can call it using its API call configuration. Local CORS defaults allow any browser origin for easier FlutterFlow testing; mobile native requests generally do not use browser CORS enforcement. Before deployment, set `CORS_ORIGINS` to a JSON array containing only your production web app origins (for example, `["https://your-app.example"]` in the environment). Do not use `*` in production. Configure HTTPS and authentication for real student data.

No secret keys are required or included. Keep future credentials in deployment environment variables or a secret manager, never in source control.
