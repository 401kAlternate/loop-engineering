# Browser app

The repository includes a Streamlit interface for the batch regression loop.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens a browser window at `http://localhost:8501`. Upload a fixed-width transaction file or use the included sample. The app validates each record, calculates the transaction count and total, generates the batch output, and compares it with the golden file.

## Deploy

The app can be deployed to Streamlit Community Cloud:

1. Create an account at [Streamlit Community Cloud](https://share.streamlit.io/).
2. Select the `401kAlternate/loop-engineering` repository.
3. Set the main file to `app.py`.
4. Deploy using `requirements.txt`.

No mainframe or COBOL compiler is required for the browser demo. The COBOL source and JCL remain in the repository as the production-shaped reference artifacts.
