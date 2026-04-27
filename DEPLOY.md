# Tic Tac Toe - AWS EC2 Deployment Guide

This guide will help you deploy the Tic Tac Toe game to AWS EC2 so anyone can access it.

## Prerequisites
- AWS Account
- Basic knowledge of terminal/command line

---

## Step 1: Launch an EC2 Instance

1. Go to [AWS Console](https://console.aws.amazon.com/) and navigate to **EC2**
2. Click **Launch Instance**
3. Configure:
   - **Name**: TicTacToe-Server
   - **Amazon Machine Image (AMI)**: Amazon Linux 2 (Free tier eligible)
   - **Instance Type**: t2.micro (Free tier eligible)
   - **Key Pair**: Create a new key pair (download the .pem file)
   - **Security Group**: 
     - Add Rule: Type = **HTTP**, Source = **Anywhere (0.0.0.0/0)**
     - Add Rule: Type = **HTTPS**, Source = **Anywhere (0.0.0.0/0)**
     - Add Rule: Type = **Custom TCP**, Port = **5000**, Source = **Anywhere (0.0.0.0/0)**
4. Click **Launch Instance**

---

## Step 2: Connect to Your Instance

### On Windows (using PowerShell):
```powershell
ssh -i "your-key.pem" ec2-user@your-public-ip
```

### On Mac/Linux:
```bash
ssh -i "your-key.pem" ec2-user@your-public-ip
```

> **Note**: Replace `your-key.pem` with your actual key file path and `your-public-ip` with your EC2 instance's public IP address.

---

## Step 3: Install Dependencies

Run these commands on your EC2 instance:

```bash
# Update packages
sudo yum update -y

# Install Python 3 and pip
sudo yum install python3 -y

# Install Flask
pip3 install Flask

# Clone or upload your code
```

---

## Step 4: Upload Your Code

### Option A: Using Git (if you push to GitHub first)
```bash
git clone https://github.com/your-username/tic-tac-toe.git
cd tic-tac-toe
```

### Option B: Using SCP
From your local terminal:
```bash
scp -i "your-key.pem" -r f:\Tic_Tac_Toe\* ec2-user@your-public-ip:~/
```

---

## Step 5: Run the Application

```bash
cd ~/Tic_Tac_Toe
python3 app.py
```

The app will start on port 5000. You can access it at:
```
http://your-public-ip:5000
```

---

## Step 6: Keep the App Running (Optional)

To keep the app running after you close the terminal, use **tmux** or **screen**:

```bash
# Install tmux
sudo yum install tmux -y

# Start a tmux session
tmux new -s tictactoe

# Run the app
cd ~/Tic_Tac_Toe
python3 app.py

# Detach from tmux (press Ctrl+B, then D)
```

To reattach later:
```bash
tmux attach -t tictactoe
```

---

## Step 7: Access Your Game

Open your browser and visit:
```
http://your-public-ip:5000
```

Replace `your-public-ip` with your EC2 instance's public IP address.

---

## Troubleshooting

### Port 5000 not accessible?
- Check your Security Group rules allow inbound traffic on port 5000
- Make sure the app is running with `host='0.0.0.0'`

### App won't start?
- Make sure Flask is installed: `pip3 list | grep Flask`
- Check for errors: `python3 app.py`

### Need to restart the app?
```bash
# Find the process
ps aux | grep python

# Kill it
kill <process-id>

# Restart
python3 app.py
```

---

## Cost Note

- **t2.micro** instance is free tier eligible (750 hours/month)
- Make sure to **stop** or **terminate** the instance when not in use to avoid charges