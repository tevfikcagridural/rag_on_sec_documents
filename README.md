# Retrieval-Augmented Generation (RAG) System System Structure
Inspired from [cookie-cutter-data-science](https://cookiecutter-data-science.drivendata.org).

This work suggests an overview of how to structure a directory for a Retrieval-Augmented Generation (RAG) system. The proposed structure is designed to organize the various components and workflows typically involved in developing and maintaining them.

## Project Structure

```sh
rag-app/
├── data/                           # Only some samples. **It is recommended to separate data stores/databases from codebase**
│   ├── raw/                        # Raw, unprocessed data files
│   ├── processed/                  # Data files after preprocessing
│   └── external/                   # External data sources
├── models/                         # For using local models 
│   ├── embeddings/                 # Pretrained/fine-tuned embedding model(s)
│   └── llm/                        # Pretrained/fine-tuned language model(s)
├── prompts/            
│   ├── prompt1.txt                 # Sample prompt file
│   ├── prompt2.txt                 # Another sample prompt file
│   └── config.json                 # Configuration for prompts
├── reports/
│   ├── development_report.md       # Reports on experiments and/or analyses
│   └── figures/                    # Figures for reports
├── src/                            # Main source code for the application.
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_preparation.py     # Data preparation scripts
│   ├── models/
│   │   ├── __init__.py
│   │   ├── embedding_models.py     # Embedding model(s) handling
│   │   └── llm_models.py           # Language model(s) handling
│   ├── services/
│   │   ├── __init__.py
│   │   └── rag_service.py          # Core service for RAG system
│   │   └── monitoring_service.py   # Monitoring service of the RAG system
│   └── app/                        # Frontend application scripts (Streamlit, gradio, etc.)
│       ├── __init__.py
│       └── main.py                 # Main application entry point
├── tests/
│   ├── __init__.py
│   ├── test_data_preparation.py    # Unit tests for data preparation
│   ├── test_embedding_model.py     # Unit tests for embedding model
│   ├── test_llm_model.py           # Unit tests for language model
│   └── test_rag_service.py         # Unit tests for RAG service
├── notebooks/
│   └── data_exploration.ipynb      # Jupyter notebook for data exploration and analysis
│   ├── experiments.ipynb           # Jupyter notebook for experiments on different strategies
├── docker/                         # For containerized deployment 
│   ├── Dockerfile                  # Dockerfile for building the image
│   └── docker-compose.yml          # Docker Compose file for multi-container setups
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
├── README.md                       # Project README file
├── requirements.txt                # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (for containerized deployment)

### Installation
#### 1. Clone the repository:

```sh
git clone https://github.com/tevfikcagridural/rag_base.git
cd rag_base
```

#### 2. Set up a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Install the dependencies:

```sh
pip install -r requirements.txt
```

### Configuration
- **Environment Variables:** Copy the .env.example to .env and update the variables as needed.
- **Prompt Configuration:** Update the prompts/config.json with the necessary prompt configurations.

### Running the Application
#### 1. Local Deployment:

```sh
python src/app/main.py
```

#### 2. Docker Deployment:
```sh
docker-compose up --build
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact c.dural@gmail.com