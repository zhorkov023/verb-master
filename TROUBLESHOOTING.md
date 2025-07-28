# Troubleshooting Guide

## 🚨 Common Issues

### 1. Webhook Error: 404 Not Found

**Problem**: Webhook returns "Wrong response from the webhook: 404 Not Found"

**Causes**:
- Vercel can't find the webhook function
- Incorrect function structure
- Missing deployment

**Solution**:
1. **Redeploy to Vercel**:
   ```bash
   vercel --prod
   ```

2. **Check function structure**: Make sure `api/webhook.py` uses `BaseHTTPRequestHandler`

3. **Verify URL**: Webhook URL should be exactly:
   ```
   https://your-app-name.vercel.app/api/webhook
   ```

4. **Test the endpoint**: Visit the URL in browser - should show:
   ```json
   {"status": "Telegram Bot Webhook is running"}
   ```

### 2. Environment Variables Not Found

**Problem**: `TELEGRAM_BOT_TOKEN not found`

**Solution**:
1. Add environment variable in Vercel Dashboard:
   - Go to Settings → Environment Variables
   - Add `TELEGRAM_BOT_TOKEN` with your bot token
   - Select all environments (Production, Preview, Development)

2. Redeploy after adding variables:
   ```bash
   vercel --prod
   ```

### 3. Import Errors

**Problem**: `ModuleNotFoundError` for bot modules

**Solution**:
1. Make sure all files are in the project root
2. Check that `requirements.txt` includes all dependencies
3. Redeploy to Vercel

### 4. Webhook Setup Issues

**Problem**: Can't set webhook or webhook not responding

**Steps to fix**:
1. **Check current webhook status**:
   ```bash
   python3 set_webhook.py
   ```

2. **Remove old webhook** (if needed):
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook"
   ```

3. **Set new webhook**:
   ```bash
   python3 set_webhook.py
   ```
   Enter: `https://your-app-name.vercel.app/api/webhook`

## 🔧 Quick Fix Commands

### Reset webhook completely:
```bash
# 1. Delete current webhook
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook"

# 2. Set new webhook
python3 set_webhook.py
```

### Check Vercel logs:
```bash
vercel logs your-app-name
```

### Test webhook endpoint:
```bash
curl https://your-app-name.vercel.app/api/webhook
```

Should return: `{"status": "Telegram Bot Webhook is running"}`

## 📋 Verification Checklist

- [ ] `api/webhook.py` exists and uses `BaseHTTPRequestHandler`
- [ ] `vercel.json` has correct configuration
- [ ] Environment variables set in Vercel Dashboard
- [ ] Project deployed with `vercel --prod`
- [ ] Webhook URL ends with `/api/webhook`
- [ ] Webhook endpoint returns 200 when accessed directly
- [ ] Bot token is valid and active

## 🆘 Still Having Issues?

1. **Check Vercel function logs**: `vercel logs your-app-name`
2. **Verify bot token**: Test with a simple API call
3. **Test locally**: Run `python3 main.py` to test bot logic
4. **Check Telegram webhook info**: Run `python3 set_webhook.py` without entering URL
