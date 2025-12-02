# Quick Start Guide - Resource Planning Engine

## 🚀 5-Minute Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/alexianaturecopy/resource-planning-engine.git
cd resource-planning-engine
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit (dashboard framework)
- pandas (data manipulation)
- numpy (numerical computing)
- plotly (visualizations)
- pulp (optimization)

### Step 3: Validate Installation
```bash
python validate.py
```

**Expected output:**
```
✅ ALL VALIDATION TESTS PASSED!
Dashboard is ready to launch!
```

### Step 4: Launch Dashboard
```bash
streamlit run app.py
```

Browser opens automatically to `http://localhost:8501`

---

## 📊 Exploring the Dashboard

### Page 1: Strategic Resource Allocation
- View budget requests vs available budget
- See PuLP optimization results
- Compare allocation strategies
- Review expected ROI and returns

### Page 2: Driver-Based Planning
- Model sales capacity (revenue → reps needed)
- Calculate marketing efficiency (CAC, LTV:CAC)
- Plan operations capacity (projects → team size)
- Adjust drivers interactively

### Page 3: Scenario Modeling
- Define Conservative/Base/Aggressive scenarios
- Compare resource needs across scenarios
- Run sensitivity analysis
- View financial impact

### Page 4: Six Sigma Dashboard
- Track DMAIC framework progress
- View process control charts
- Analyze defect root causes (Pareto)
- Monitor quality metrics

### Page 5: ROI Prioritization
- See ranked project list by composite score
- Understand scoring methodology
- Compare projects side-by-side
- Review funding recommendations

---

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Data files not found
**Solution:**
```bash
python src/generate_sample_data.py
```

### Issue: Optimization not working
**Solution:** Make sure PuLP is installed:
```bash
pip install pulp
python -c "from pulp import *; print('PuLP installed successfully')"
```

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

---

## 📝 Customizing Data

### Option 1: Modify Existing Data
Edit CSV files in `data/` folder:
- `resource_requests.csv` - Change service lines, budgets, ROI
- `constraints.csv` - Adjust budget limits
- `service_metrics.csv` - Update process metrics

### Option 2: Regenerate Sample Data
```bash
python src/generate_sample_data.py
```

Modify parameters in `src/generate_sample_data.py` first if desired.

---

## 🎯 Using for Job Applications

### Add to Resume:
```
PROJECTS
Resource Planning Engine | GitHub Portfolio
• Built optimization engine allocating $18M across 10 service lines using linear programming
• Implemented driver-based planning models and scenario analysis
• Integrated Six Sigma DMAIC framework for process improvement
• Technologies: Python, PuLP, Streamlit, Pandas
```

### LinkedIn Post:
```
🚀 Just published my Resource Planning Engine on GitHub!

Demonstrates strategic resource allocation using:
✅ Linear programming optimization (PuLP)
✅ Driver-based planning models
✅ Six Sigma process improvement
✅ Interactive scenario analysis

Optimizes $18M budget allocation achieving 2.7x ROI.

Check it out: [your-github-url]

#CFO #ResourcePlanning #Optimization #SixSigma
```

### Interview Talking Point:
> "I built a resource planning engine that uses linear programming to optimize budget allocation. It takes $18M budget and 10 competing service requests, applies constraints, and finds the allocation that maximizes ROI. The result was 2.7x blended return vs 2.3x with equal distribution. It's on my GitHub with working code."

---

## 🚀 Deploying to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Resource Planning Engine"
git remote add origin https://github.com/YOUR_USERNAME/resource-planning-engine.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

### Step 3: Get Your URL
After 2-3 minutes:
```
https://resource-planning-engine-[random].streamlit.app
```

Add this URL to your README!

---

## 📚 Next Steps

1. ✅ **Test locally** - Make sure everything works
2. ✅ **Customize** - Add your personal context
3. ✅ **Deploy** - Make it publicly accessible
4. ✅ **Share** - Add to resume, LinkedIn, applications

---

## 💡 Pro Tips

### Customize for Your Industry:
- Change service lines to match your business
- Adjust ROI ranges for your sector
- Update Six Sigma targets for your context

### Add Real Data:
- Replace sample CSVs with actual company data
- Connect to ERP via SQL queries in `sql/` folder
- Schedule daily data refresh

### Expand Functionality:
- Add ML forecasting (separate repo recommended)
- Implement multi-period optimization
- Build API integration layer

---

**Need Help?** Check README.md for comprehensive documentation.

**Ready to Showcase?** Deploy to Streamlit Cloud and share your link!
