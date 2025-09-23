
FROM python:3.11.9

# Install uv (modern Python package installer) and uvx
RUN pip install uv

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -LsSf https://astral.sh/uv/install.sh | sh

RUN uv tool install crewai

RUN ln -s /root/.local/bin/crewai /usr/local/bin/crewai

# Set work directory
WORKDIR /app

# Copy application code
COPY ./src ./src
COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock

# Install Python dependencies using uv 
RUN uv venv && uv sync


# Default command - can be overridden
CMD ["crewai", "run"]
