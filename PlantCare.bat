@echo off
title PlantCare AI Server

color 0A
echo ========================================
echo.
echo    🌱 PlantCare AI Server
echo    Disease Detection ^& Care Assistant
echo.
echo ========================================
echo.

REM Navigate to project directory
cd /d "C:\Users\adity\Documents\Projects\plant-disease-AI"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please make sure you're in the correct directory.
    pause
    exit
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting server...
echo.

REM Start Flask server in background
start /B python app.py

REM Wait for server to start
echo Waiting for server to initialize...
timeout /t 5 /nobreak > nul

REM Open browser automatically
echo Opening browser...
start http://localhost:5000

echo.
echo ========================================
echo ✓ Server is running!
echo ✓ Browser opened automatically
echo.
echo 📡 URL: http://localhost:5000
echo.
echo ⚠️  To STOP the server: Close this window
echo ========================================
echo.

REM Keep window open
cmd /k
```

3. **Click File → Save As**

4. **Save as:**
   - **File name:** `start_plantcare_ai.bat`
   - **Save as type:** `All Files (*.*)`
   - **Location:** `C:\Users\adity\Documents\Projects\plant-disease-AI\`

5. **Click Save**

---

## **Step 2: Test the Batch File**

1. **Go to:** `C:\Users\adity\Documents\Projects\plant-disease-AI\`
2. **Double-click** `start_plantcare_ai.bat`
3. **You should see:**
   - Command window opens with green text
   - Server starts
   - Browser opens automatically
   - App loads at `http://localhost:5000`

**Does it work?** ✅

---

## **Step 3: Create Desktop Shortcut**

### **Method A: Drag and Drop (Easiest)**

1. **Open File Explorer**
2. **Go to:** `C:\Users\adity\Documents\Projects\plant-disease-AI\`
3. **Find** `start_plantcare_ai.bat`
4. **Right-click and drag** the file to your Desktop
5. **Select** "Create shortcuts here"

### **Method B: Create Shortcut Manually**

1. **Right-click** on Desktop
2. **Select** New → Shortcut
3. **Type location:**
```
   C:\Users\adity\Documents\Projects\plant-disease-AI\start_plantcare_ai.bat
```
4. **Click Next**
5. **Name it:** `PlantCare AI`
6. **Click Finish**

---

## **Step 4: Customize the Shortcut Icon (Make it Pretty!)**

### **Option A: Use Built-in Windows Icons**

1. **Right-click** the shortcut on Desktop
2. **Select** Properties
3. **Click** "Change Icon..." button
4. **Click** "Browse..."
5. **Navigate to:**
```
   C:\Windows\System32\shell32.dll