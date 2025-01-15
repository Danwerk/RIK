# RIK Osaühingud

---

## Paigaldusjuhend

### 1. **Eeltingimused**
Rakenduse töötamiseks on vajalik järgmine tarkvara:
- **Python 3.8 või uuem** (lae alla [siit](https://www.python.org/downloads/))
- **pip** (Python Package Manager, sisaldub Python 3.8+ versioonides)
- **Virtualenv** (soovitatav, installitakse käsuga `pip install virtualenv`)

---

### 2. **Projekti seadistamine**
1. **Klooni repositoorium**:
   ```bash
   git clone https://github.com/Danwerk/RIK.git
   cd RIK
   ```

2. **Loo ja aktiveeri virtuaalne keskkond**:
   - Linux/MacOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Paigalda sõltuvused**:
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. **Andmebaasi seadistamine**
1. **Andmebaasi loomine**:
   - Käivita järgmine käsk andmebaasi loomiseks:
     ```bash
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```
---

### 4. **Rakenduse käivitamine**
**Käivita käsk**:
   ```bash
   flask run
   ```
   Rakendus on nüüd kättesaadav [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

### 5. **Kujundus**
- Kõik CSS-failid asuvad kataloogis `static/css/`.
- HTML-failid asuvad kataloogis `templates/` ja kasutavad Flaski `Jinja2` mallimootorit.

---