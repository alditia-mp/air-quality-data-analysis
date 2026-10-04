# Analisis Data: Air Quality Dataset

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan berjalan pada alamat:

```text
http://localhost:8501
```

## Online Dashboard

Dashboard juga tersedia secara online melalui Streamlit Cloud. Tautan dashboard terdapat pada file `url.txt`.
