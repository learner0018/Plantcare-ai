# 🌱 PlantCare AI - Disease Detection System

> AI-powered plant disease detection with 92% accuracy using Deep Learning

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.15.0-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An intelligent web application that uses Convolutional Neural Networks (CNN) to detect plant diseases from images and provides AI-powered treatment recommendations.

## ✨ Features

- 🔍 **Real-time Disease Detection** - Identify 38 different plant diseases with 92% accuracy
- 🤖 **AI Chat Assistant** - Get personalized plant care advice powered by Claude AI
- 📊 **Comprehensive Analysis** - Detailed symptoms, causes, and treatment plans
- 💊 **Treatment Solutions** - Step-by-step remediation guides
- 🌿 **Prevention Tips** - Proactive care recommendations
- 📱 **Responsive Design** - Beautiful UI that works on all devices
- ⚠️ **Confidence Warnings** - Low confidence alerts when model needs more data

## 🎯 Supported Plants

- 🍅 **Tomato** (10 diseases)
- 🥔 **Potato** (3 diseases)
- 🍎 **Apple** (4 diseases)
- 🌽 **Corn** (4 diseases)
- 🍇 **Grape** (4 diseases)
- 🍑 **Peach** (2 diseases)
- 🌶️ **Pepper** (2 diseases)
- 🍓 **Strawberry** (2 diseases)
- And more! **(38 total plant conditions)**

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Validation Accuracy | 92% |
| Top-3 Accuracy | 98% |
| Training Images | 43,456 |
| Validation Images | 10,864 |
| Classes | 38 |

## 🚀 Technology Stack

**Backend:**
- Python 3.12
- Flask 3.0
- TensorFlow 2.15
- Keras

**Machine Learning:**
- Transfer Learning (MobileNetV2)
- Image Preprocessing
- Data Augmentation
- CNN Architecture

**Frontend:**
- HTML5
- JavaScript (ES6+)
- Tailwind CSS
- Lucide Icons

**AI Integration:**
- Anthropic Claude API
- Natural Language Processing
- Context-aware responses

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection (for AI chat)

### Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/plantcare-ai.git
cd plantcare-ai
```

**2. Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the trained model**

The trained model file is too large for GitHub. Download it here:

📥 **[Download plant_model.h5 (45MB)](https://drive.google.com/YOUR_LINK_HERE)**

Place it in the `model/` folder:
```
model/plant_model.h5
```

**5. Set up environment variables**

Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from: https://console.anthropic.com/

**6. Run the application**
```bash
python app.py
```

**7. Open in browser**
```
http://localhost:5000
```

## 📸 Usage

1. **Upload Image** - Take or select a photo of the affected plant
2. **Analyze** - Click "Analyze Plant" to process the image
3. **Review Results** - See disease identification and confidence score
4. **Read Treatment** - Follow the step-by-step treatment guide
5. **Ask Questions** - Use the AI chat for personalized advice

## 📁 Project Structure
```
plantcare-ai/
│
├── app.py                      # Main Flask application
├── model_handler.py            # AI model inference
├── disease_database.py         # Disease information database
├── ai_chat_handler.py          # Claude AI integration
├── train_model.py              # Model training script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # This file
│
├── model/
│   ├── plant_model.h5         # Trained model (download separately)
│   ├── classes.txt            # Disease class names
│   └── training_history.png   # Training performance graph
│
├── templates/
│   └── index.html             # Frontend UI
│
├── static/
│   └── js/
│       └── app.js             # Frontend JavaScript
│
└── uploads/                    # Temporary image storage (not in repo)
```

## 🧠 How It Works

### Model Architecture
```
Input Image (224x224x3)
    ↓
MobileNetV2 (Pre-trained on ImageNet)
    ↓
Global Average Pooling
    ↓
Dense Layer (128 neurons, ReLU)
    ↓
Dropout (0.5)
    ↓
Output Layer (38 neurons, Softmax)
    ↓
Disease Prediction
```

### Training Process

1. **Data Collection** - PlantVillage dataset (54,000+ images)
2. **Preprocessing** - Resize, normalize, augment
3. **Transfer Learning** - Fine-tune MobileNetV2
4. **Training** - 10 epochs with validation
5. **Evaluation** - 92% accuracy achieved
6. **Deployment** - Export to .h5 format

## 🎓 Training Your Own Model

If you want to retrain the model:
```bash
# Download dataset from Kaggle
# Place in dataset/color/ folder

# Run training script
python train_model.py

# Model will be saved to model/plant_model.h5
```

## 🔒 Security

- ✅ API keys stored in `.env` (excluded from Git)
- ✅ No sensitive data in code
- ✅ Secure file upload validation
- ✅ CORS protection enabled
- ✅ Input sanitization

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large model file requires separate download
- First API request may be slow (model loading)
- Limited to 38 plant disease classes currently

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Offline mode support
- [ ] More plant species
- [ ] Disease progression tracking
- [ ] Community forum
- [ ] Multiple language support

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset:** [PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset) from Kaggle
- **Base Model:** MobileNetV2 from TensorFlow
- **AI Chat:** Anthropic Claude API
- **Icons:** Lucide Icons
- **Styling:** Tailwind CSS

## 📧 Contact

**Aditya Singh**

- GitHub: https://github.com/learner0018
- LinkedIn: https://www.linkedin.com/in/aditya-singh-083b02351/
- Email: adityasinghdrdo70@gmail.com

**Project Link:** https://github.com/learner0018/Plantcare-ai

---

⭐ **If you found this project helpful, please give it a star!** ⭐

Made with ❤️ and Python
```


✅ templates/index.htm
