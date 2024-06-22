# Cornucopia

A LLM powered knowledge assistant.

---

```mermaid
graph TD
  A["Question"]-->B["Agent"]
  B-->C["Small talk"]
  B-->D["Wikipedia"]
  B-->E["Custom knowledge"]
  B-->F["DuckDuckGo search"]
  C-->G["Response"]
  D-->G
  E-->H["Text/Markdown"]
  E-->I["Excel"]
  E-->J["PDF"]
  E-->K["Docx"]
  F-->G
  H-->G
  I-->G
  J-->G
  K-->G
```

### Usage

```sh
pip install -r requirements.txt
```

Run the API server

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload 
```

Set API url in frontend [chat.js](./frontend/js/chat.js) and visit `localhost`