# Hugging Face Spaces Deployment Guide

This guide explains how to deploy the NYC Taxi Fare Prediction model to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account**
   - Create account at https://huggingface.co
   - Generate an access token (Settings → Access Tokens)

2. **GitHub Repository**
   - This project should be pushed to GitHub
   - Public repository is recommended for automatic deployment

3. **Trained Model**
   - Run `python train.py` to generate `artifacts/taxi_fare_ann_model.joblib`
   - Commit the model to GitHub

## Deployment Steps

### Windows / PowerShell Setup

If you are in PowerShell, set environment variables like this:

```powershell
$env:HF_USERNAME = 'your_hf_username'
$env:HF_SPACE = 'your_space_name'
$env:HF_TOKEN = 'your_hf_token'
```

Then run the PowerShell helper:

```powershell
.\push_to_hf.ps1
```

This helper uploads the Space directly through the Hugging Face Hub API, so the binary model file is handled correctly.

### Step 1: Prepare Your Repository

Ensure your GitHub repository contains:

```
├── app.py                          ✓ Must be in root
├── taxi_fare.py                    ✓ Utilities
├── requirements.txt                ✓ All dependencies
├── artifacts/
│   └── taxi_fare_ann_model.joblib ✓ Trained model
├── data/
│   └── nyc_taxi_fare.csv          (optional, can generate)
└── README.md                       ✓ Documentation
```

**Commit and push to GitHub or upload directly with the helper:**

```bash
git add .
git commit -m "Prepare for Hugging Face deployment"
git push origin main
```

Or, from PowerShell, upload the current workspace directly:

```powershell
.\push_to_hf.ps1
```

### Step 2: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the form:
   - **Space name**: `nyc-taxi-fare-prediction` (or your choice)
   - **License**: Choose appropriate license
   - **SDK**: Select **"Gradio"**
   - **Visibility**: Public (recommended) or Private

### Step 3: Connect GitHub Repository

After creating the Space:

1. Go to your Space settings (⚙️ icon)
2. Under "Git configuration":
   - Select "Connected to a Git repository (GitHub)"
   - Connect your GitHub account (authorize if needed)
   - Select your repository
   - Select branch (usually `main`)

3. Enable automatic updates:
   - Check "Continuous Integration"
   - This will automatically redeploy when you push to GitHub

### Step 4: Check Deployment Status

1. Go to your Space page
2. You should see deployment in progress
3. Watch the build log:
   - Stack will install `Python 3.10+`
   - Dependencies from `requirements.txt` will be installed
   - `app.py` will be executed

### Step 5: Access Your Deployment

Once deployment completes:

- Your app URL: `https://huggingface.co/spaces/<username>/<space-name>`
- Share this URL with others
- The app is automatically hosted and publicly accessible

## Troubleshooting

### Issue: Build fails with "file not found"

**Solution:**
- Ensure `app.py` is in the root directory
- Ensure model file `artifacts/taxi_fare_ann_model.joblib` exists
- Check that all imports in Python files are correct

```bash
# Verify locally first
python app.py
```

### Issue: Model file is too large

**Solution:**
- The model (~283 KB) should fit fine
- If larger, consider using model optimization techniques
- Alternative: Download model from elsewhere during startup

### Issue: Dependency conflicts

**Solution:**
- Update Python versions
- Specify exact package versions where needed

```
# requirements.txt example with pinned versions
gradio==4.32.0
joblib==1.3.2
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
```

### Issue: "app.py" not recognized

**Solution:**
- Verify filename is exactly `app.py` (case-sensitive)
- Ensure `if __name__ == "__main__":` block ends with `demo.launch()`
- Check that Gradio Blocks/Interface is named `demo`

### Issue: Memory/timeout during training

**Solution:**
- Don't run training during deployment
- Train locally, commit the model to GitHub
- The Space should only run `app.py` for inference

## Continuous Integration (CI/CD)

### Automatic Redeployment

When you update the repository:

1. Push changes to GitHub:
   ```bash
   git push origin main
   ```

2. Hugging Face automatically:
   - Pulls latest code
   - Installs dependencies
   - Reruns `app.py`
   - Updates the live Space

### What Triggers Redeployment

- Upload via the helper script
- Update `app.py`
- Update `requirements.txt`
- Update model file `artifacts/taxi_fare_ann_model.joblib`

## Performance Optimization

### For Faster Inference

1. **Model Caching:**
   ```python
   import joblib
   
   # Cache model in memory (done in app.py)
   model = joblib.load('artifacts/taxi_fare_ann_model.joblib')
   ```

2. **Feature Optimization:**
   - Pre-compute feature statistics
   - Use efficient data types (float32 instead of float64)

3. **Request Batching:**
   - Gradio handles this automatically
   - Good for high-traffic applications

## Sharing and Collaboration

### Share Your Space

1. Get your Space URL: `https://huggingface.co/spaces/<username>/<space-name>`
2. Share on social media, forums, or in documentation
3. Anyone can use it without requiring an account

### Embed in Documentation

```html
<!-- Embed in markdown or HTML -->
<iframe 
    src="https://huggingface.co/spaces/<username>/<space-name>" 
    frameborder="0" 
    width="100%" 
    height="600">
</iframe>
```

### Make it Public and Listed

- Your Space appears in the Spaces browse page
- More visibility and discoverable
- Great for portfolio

## Advanced Configuration

### Custom Domain

Hugging Face supports custom domains for professional deployments (requires Pro account).

### Private Spaces

- Set visibility to "Private"
- Share with specific email addresses
- Useful for proprietary models

### Persistent Storage

If you need to maintain state or save uploads:

1. Use Hugging Face Hub for model storage
2. Use temporary `/tmp` directory (cleared after session)
3. For persistent data, use external services (database, cloud storage)

## FAQ

**Q: Can I retrain the model on Hugging Face?**  
A: Not recommended. Train locally, commit the model, deploy for inference.

**Q: Can I use GPU?**  
A: Free tier uses CPU. Pro tier (paid) offers GPU support.

**Q: Is there a cost?**  
A: Free tier available. Check https://huggingface.co/pricing for details.

**Q: Can I make the Space private?**  
A: Yes, in Space settings. Can be public or accessible only to specific users.

**Q: How long can the app run?**  
A: Apps run 24/7 on Hugging Face (free tier may have rate limits).

## Contact & Support

- Hugging Face Spaces Docs: https://huggingface.co/docs/hub/spaces
- Gradio Documentation: https://www.gradio.app/docs/
- Issue not listed? Check GitHub Discussions or Hugging Face Community

---

**Deployment Status:** ✓ Ready for production  
**Last Updated:** May 7, 2026
