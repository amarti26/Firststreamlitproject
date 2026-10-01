# RainCheck

A Streamlit weather dashboard powered by n8n and Open-Meteo.

## Features

- Today's weather report by city.
- Rain probability, temperature, wind and weather icon.
- Email subscriptions for rain alerts.
- Custom rain-probability threshold.
- Custom alert hour from 00:00–23:00 in Europe/Copenhagen time.
- n8n stores subscriptions and checks them hourly.
- Gmail sends alerts once the Gmail credential is connected in n8n.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

Deploy `raincheck/app.py` from this GitHub repository. The app uses the published n8n API automatically.

n8n API:
https://amarti26.app.n8n.cloud/workflow/fHTOU4XE2a7CaqyE

The separate scheduler workflow still needs a Gmail credential before automatic email alerts can be sent.
