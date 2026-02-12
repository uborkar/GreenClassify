# .gitignore File Documentation

## Overview
A comprehensive `.gitignore` file has been created for the GreenClassify project to exclude unnecessary files from version control.

## What's Being Ignored

### 🐍 Python Files
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.egg-info/` - Package metadata
- Virtual environments (`venv/`, `env/`, `.venv`)

### 🤖 Machine Learning Files
- **Model files**: `*.h5`, `*.hdf5`, `*.pkl`, `*.pt`, `*.pth`
- **Checkpoints**: `checkpoints/`, `saved_models/`
- These files are typically large and should be stored separately (e.g., Git LFS, cloud storage)

### 📓 Jupyter Notebooks
- `.ipynb_checkpoints/` - Notebook auto-save files
- Keeps your actual notebooks tracked while ignoring temporary checkpoints

### 📁 Data Files
- `*.csv`, `*.xlsx`, `*.json` - Dataset files
- `data/`, `datasets/` - Data directories
- Archive files: `*.zip`, `*.tar.gz`, `*.rar`

### 🖼️ Uploaded Files
- `flask/uploads/*` - User-uploaded images
- Exception: `flask/uploads/.gitkeep` is tracked to preserve directory structure

### 💻 IDE & Editor Files
- `.vscode/`, `.idea/` - IDE configuration
- `*.swp`, `*.swo` - Vim swap files
- `.DS_Store` - macOS metadata

### 🔐 Environment Variables
- `.env`, `.flaskenv` - Environment configuration files
- These often contain sensitive information like API keys

### 📝 Logs & Temporary Files
- `*.log` - Log files
- `*.tmp`, `*.bak` - Temporary and backup files

### 🗄️ Database Files
- `*.db`, `*.sqlite`, `*.sqlite3` - Local database files

## Important Notes

### ✅ What IS Tracked
- Source code (`.py` files)
- Templates (`.html` files)
- Static assets (`.css`, `.js` files in static/)
- Configuration templates
- Documentation (`.md` files)
- Requirements file (`requirements.txt`)
- License and README

### ❌ What IS NOT Tracked
- Virtual environments
- **Model files** (`.h5` files) - These are large and should be downloaded separately
- User uploads
- IDE configurations
- Temporary files
- Environment variables

## Special Considerations

### Model Files
The trained model file (`vegetable_classification.h5`) is **ignored** because:
1. It's large (~40MB+)
2. It can be regenerated from the training notebook
3. Should be stored in Git LFS or cloud storage for distribution

### Uploads Directory
- The `flask/uploads/` directory structure is preserved via `.gitkeep`
- Actual uploaded files are ignored to prevent repository bloat
- Users need to create this directory or it will be auto-created on first upload

## Recommendations

### For Model Distribution
Consider using one of these approaches:
1. **Git LFS** (Large File Storage) - for version-controlled large files
2. **Cloud Storage** - Google Drive, Dropbox, AWS S3
3. **Release Assets** - GitHub Releases with attached model files
4. **Model Registry** - MLflow, Weights & Biases

### For Collaboration
Team members should:
1. Clone the repository
2. Create their own virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Download the model file separately (if not using Git LFS)
5. Create their own `.env` file for local configuration

## Files Created
- `.gitignore` - Main ignore file
- `flask/uploads/.gitkeep` - Preserves uploads directory structure

## Usage
The `.gitignore` file is automatically recognized by Git. No additional configuration needed!
