FROM python:3.11

# Copy pyproject.toml
COPY pyproject.toml pyproject.toml
COPY .git .git
COPY macro macro

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .

# Run gunicorn
COPY gunicorn-cfg.py gunicorn-cfg.py
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "macro.main:app"]
