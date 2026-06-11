# Authentication

Supported Gemini CLI auth modes for this adapter:

- Google OAuth only where the account remains eligible.
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` for paid Gemini API-key access.
- Vertex AI / Google Cloud with `GOOGLE_GENAI_USE_VERTEXAI=true`,
  `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION`.
- Enterprise or owner-approved authenticated environments.

Do not commit `.gemini/.env`, OAuth state, token files, service-account JSON,
Google Cloud ADC files, cookies, or runtime caches.
