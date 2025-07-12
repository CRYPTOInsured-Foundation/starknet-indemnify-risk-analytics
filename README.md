# StarkInsure Risk Analytics

The **StarkInsure Risk Analytics** is a Django-powered microservice that provides AI-driven risk assessment for DeFi insurance underwriting. Running on port `5001`, it analyzes on-chain and off-chain data to calculate insurance premiums and detect fraudulent claims.

---

## 🔗 API Documentation  
[View Swagger Docs](http://localhost:5001/docs) | [Risk Model Docs](http://localhost:5001/model-docs)

---

## ✨ Risk Analytics Features  
- **Underwriting Intelligence**:  
  - 🧠 ML-powered risk scoring (XGBoost/Neural Nets)  
  - 📉 Historical claim probability analysis  
  - 🕵️‍♂️ Sybil attack detection  
- **Data Processing**:  
  - On-chain behavior analysis (StarkNet L2)  
  - Off-chain KYC data correlation  
  - Real-time oracle feeds processing  
- **Visualization**:  
  - Risk heatmaps for insurance pools  
  - Claim prediction dashboards  

---

## 🛠️ Tech Stack  
| Component           | Technology                                                                 |
|---------------------|---------------------------------------------------------------------------|
| Framework           | [Django 4.2](https://www.djangoproject.com/) + [DRF](https://www.django-rest-framework.org/) |
| Machine Learning   | [PyTorch](https://pytorch.org/) + [XGBoost](https://xgboost.readthedocs.io/) |
| Blockchain Data    | [StarkNet.py](https://github.com/software-mansion/starknet.py)           |
| Database           | PostgreSQL + [TimescaleDB](https://www.timescale.com/)                   |
| Visualization      | [Plotly Dash](https://plotly.com/dash/)                                  |

---

## 🚀 Quick Start  

### Prerequisites  
- Python 3.10+  
- PostgreSQL 15+ with TimescaleDB  
- CUDA 11.7+ (for GPU acceleration)  
- StarkNet full node access  

### Installation  
1. **Clone the repo**:  
   ```bash
   git clone https://github.com/CRYPTOInsured-Foundation/starkinsure-risk-analytics.git
   cd starkinsure-risk-analytics
   ```
2. Setup virtual environment:
   ```bash
   python -m venv ven
   source venv/ven/bin/activate  # Linux/Mac
   workon ven    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   ```bash
   cp .env.example .env
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the service:
   ```bash
   python manage.py runserver 5001
   ```
## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feat/your-feature
```
3. Commit changes following Conventional Commits
4. Push to the branch
5. Open a Pull Request

