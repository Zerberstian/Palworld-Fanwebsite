# <span style="color: red">Teil 1!</span>

Auch bei einer einfachen Fan-Webseite ohne Login oder offensichtliche Datenerhebung greift die Datenschutz-Grundverordnung (DSGVO). Der Umfang ist aber deutlich geringer. Hier sind die wichtigsten Punkte, die du beachten solltest:

---

## 1. **Server-Logs (wichtig!)**

Auch wenn du selbst keine Daten erhebst, speichert dein Webserver automatisch:

* IP-Adresse
* Zeitpunkt der Anfrage
* Browser / User-Agent

👉 Diese gelten als **personenbezogene Daten**.

**Das musst du tun:**

* In der Datenschutzerklärung erwähnen
* Speicherzeit begrenzen (z. B. 7–14 Tage)
* „berechtigtes Interesse“ als Rechtsgrundlage angeben (Art. 6 Abs. 1 lit. f DSGVO)

---

## 2. **Hosting / Auftragsverarbeitung**

Wenn deine Seite bei einem Hoster läuft (z. B. IONOS, Netlify, Vercel etc.):

👉 Du brauchst:

* Einen **Auftragsverarbeitungsvertrag (AVV)** mit dem Anbieter

Das bieten die meisten Hoster automatisch an.

---

## 3. **Datenschutzerklärung (Pflicht!)**

Auch ohne Tracking brauchst du eine.

Inhalt:

* Wer du bist (Verantwortlicher)
* Welche Daten verarbeitet werden (z. B. Server-Logs)
* Zweck und Rechtsgrundlage
* Hosting-Anbieter
* Rechte der Nutzer

---

## 4. **Cookies / Tracking**

Wenn du **keine Cookies, kein Analytics, keine externen Einbindungen** hast:

👉 Dann brauchst du:

* **Kein Cookie-Banner**

ABER sobald du z. B. einbindest:

* Google Fonts (extern)
* YouTube
* Analytics

→ dann wird’s komplizierter (Einwilligung nötig)

---

## 5. **Externe Ressourcen vermeiden**

Selbst bei statischen Seiten können Probleme entstehen durch:

* CDNs (z. B. externe Fonts)
* APIs
* eingebettete Inhalte

👉 Empfehlung:

* Alles lokal hosten (Fonts, JS, CSS)
* Keine Drittanbieter-Requests

---

## 6. **JSON-Daten**

Du schreibst:

> „JSON enthält keine personenbezogenen Daten“

👉 Dann ist das **DSGVO-technisch unkritisch**, solange:

* keine indirekte Identifizierbarkeit möglich ist
* keine Kombination mit anderen Daten erfolgt

---

## 7. **HTTPS (technische Pflicht)**

* SSL-Zertifikat verwenden (heute Standard)
* schützt Datenübertragung

---

## 8. **Impressum (nicht DSGVO, aber Pflicht in DE)**

Nach dem Telemediengesetz bzw. heute im Digitale-Dienste-Gesetz:

👉 Du brauchst ein Impressum, wenn die Seite nicht rein privat ist.

---

## Kurzfazit

Für deine beschriebene Seite brauchst du im Grunde nur:

✅ Datenschutzerklärung
✅ AV-Vertrag mit Hoster
✅ Hinweis auf Server-Logs
✅ HTTPS
✅ Impressum

👉 **Kein Cookie-Banner**, solange du wirklich nichts extern einbindest.

---

## Typische Falle

Viele denken „keine Daten = keine DSGVO“ — stimmt leider nicht wegen:

* IP-Adressen
* Hosting
* unsichtbare Drittanbieter-Anfragen

---

Wenn du willst, kann ich dir:

* eine **fertige DSGVO-Datenschutzerklärung für genau deine Seite** schreiben
* oder deine konkrete Seite prüfen (inkl. versteckter Requests)


---

# <span style="color: red">Teil 2!</span>

Wenn du deine Seite über GitHub Pages (github.io) hostest, wird es tatsächlich **sehr schlank**, aber **nicht komplett DSGVO-frei**. Du betreibst zwar keinen eigenen Server, **GitHub tut es für dich** – und genau da greifen ein paar Pflichten.

Ich erklär dir konkret, ohne unnötigen Juristenkram:

---

# 🧩 1. Was passiert technisch überhaupt?

Auch bei GitHub Pages werden automatisch verarbeitet:

* IP-Adresse der Besucher
* Browserinfos
* Zeitpunkt des Zugriffs

👉 Das läuft über GitHub (Microsoft-Infrastruktur)

➡️ Heißt: **personenbezogene Daten werden verarbeitet**, auch wenn du selbst nichts speicherst.

---

# ✅ 2. Was musst du konkret machen

## ✔️ A. Datenschutzerklärung (Pflicht)

Du brauchst eine einfache Seite wie:

```
/datenschutz
```

**Inhalt:**

* Hinweis auf GitHub Pages Hosting
* Hinweis auf Server-Logs (IP etc.)
* Rechtsgrundlage: „berechtigtes Interesse“ (Art. 6 Abs. 1 lit. f DSGVO)
* Hinweis, dass du selbst keine Daten erhebst
* Verlinkung auf GitHub Privacy Policy

👉 GitHub ist hier **Auftragsverarbeiter bzw. teilweise eigener Verantwortlicher**

---

## ✔️ B. AV-Vertrag – Sonderfall GitHub

Normalerweise brauchst du einen AV-Vertrag.

👉 Problem:

* GitHub bietet **keinen klassischen AV-Vertrag für Pages**

👉 Lösung (üblich & akzeptiert in der Praxis):

* Du verweist in der Datenschutzerklärung auf:

  * GitHub als Dienstleister
  * deren Privacy Policy
* Rechtsgrundlage: **berechtigtes Interesse**

⚠️ Das ist ein Graubereich, aber Standard bei statischen Seiten.

---

## ✔️ C. Impressum (Deutschland!)

Nach dem Digitale-Dienste-Gesetz:

👉 Pflicht, wenn:

* nicht rein privat
* oder öffentlich zugänglich (Fan-Seite zählt meist)

---

## ✔️ D. HTTPS

👉 Ist automatisch bei GitHub Pages aktiv → ✔️ erledigt

---

## ✔️ E. Cookies / Tracking

Wenn du wirklich nur:

* statisches HTML/JS
* JSON mit Items/Stats

verwendest:

👉 Dann gilt:

* ❌ kein Cookie-Banner nötig
* ❌ keine Einwilligung nötig

ABER NUR wenn du NICHT nutzt:

* Google Analytics
* externe Fonts (Google Fonts!)
* APIs
* YouTube Embeds

---

# ⚠️ 3. Häufige versteckte DSGVO-Fallen

Auch bei „einfachen“ Seiten passieren oft diese Dinge:

### ❌ Externe Assets

```html
<link href="https://fonts.googleapis.com/...">
```

👉 Problem: IP wird an Google gesendet

➡️ Lösung: Fonts lokal speichern

---

### ❌ Icons/CDN

```html
https://cdn.jsdelivr.net/...
```

👉 ebenfalls Datenübertragung

➡️ Alles lokal hosten

---

### ❌ JavaScript Libraries per CDN

👉 Gleiches Problem

---

# 🧾 4. Deine JSON-Daten

Du schreibst:

> nur stats zu items icons usw

👉 Perfekt, das ist:

* **kein personenbezogenes Datum**
* DSGVO-unproblematisch

---

# 📄 5. Minimal-Setup (was du wirklich brauchst)

Für deine Seite reicht:

### 1. Impressum

### 2. Datenschutzerklärung mit:

* GitHub Pages Hosting
* Server-Logs (IP-Adresse etc.)
* keine eigene Datenerhebung
* keine Cookies
* keine Drittanbieter

---

# ✍️ 6. Mini-Vorlage (kurz & passend)

Wenn du willst, kannst du das fast so verwenden:

---

**Datenschutzerklärung (Kurzfassung)**

* Diese Website wird über GitHub Pages gehostet.
* Beim Aufruf werden durch GitHub automatisch Informationen erfasst (IP-Adresse, Zeitpunkt, Browser).
* Diese Daten sind technisch erforderlich, um die Website bereitzustellen.
* Ich selbst erhebe oder speichere keine personenbezogenen Daten.
* Es werden keine Cookies oder Tracking-Tools eingesetzt.

---

# 🧠 Fazit

Du bist in einer der einfachsten DSGVO-Situationen überhaupt:

👉 Kein Login
👉 Keine Userdaten
👉 Keine Tracker
👉 Nur statische Inhalte

➡️ Ergebnis: **Minimalpflichten reichen völlig aus**

---

Wenn du möchtest, kann ich dir:

* eine **komplett fertige rechtssichere Datenschutzerklärung + Impressum** für GitHub Pages schreiben
* oder deinen Code checken (ob irgendwo doch versteckte Datenabflüsse sind)
