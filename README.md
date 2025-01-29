# AI-Powered Image Generator

## Overview
This project is an AI-powered image generator that takes a **text prompt** as input, processes it using **LumoLabs Lumo 70B Instruct** for cleaning and enhancement, and then sends the refined text to **Stability AI's model** to generate an image. The generated image is displayed on the frontend with an option to download.

## Workflow
1. **User Input**: The user enters a text prompt in the frontend.
2. **Backend Processing**:
   - The prompt is sent to the backend.
   - The backend forwards the prompt to **LumoLabs Lumo 70B Instruct** for **text cleaning and enhancement**.
3. **Image Generation**:
   - The enhanced text is then sent to **Stability AI's model** to generate an image.
4. **Frontend Display**:
   - The generated image is received and displayed on the frontend.
   - The user is given an option to **download the image**.

## Tech Stack
- **Frontend**: React/Next.js (or any preferred framework)
- **Backend**: FastAPI/Flask/Node.js
- **AI Models**:
  - **LumoLabs Lumo 70B Instruct** for text enhancement
  - **Stability AI** for image generation
- **Hosting**: AWS/GCP/Vercel (based on preference)

## Installation & Setup
### Prerequisites
- Python 3.8+
- Node.js (for frontend)
- API keys for **LumoLabs Lumo 70B** and **Stability AI**

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-username/ai-image-generator.git
cd ai-image-generator/backend

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd ../frontend

# Install dependencies
yarn install  # or npm install

# Start the frontend
yarn dev  # or npm run dev
```

## API Endpoints
### **1. Process Prompt & Generate Image**
**Endpoint:** `POST /generate-image`
**Request Body:**
```json
{
  "prompt": "A futuristic city skyline at sunset"
}
```
**Response:**
```json
{
  "image_url": "https://generated-image-url.com/image.png"
}
```

## Features
✅ Accepts **user text prompts**  
✅ Enhances text using **LumoLabs Lumo 70B Instruct**  
✅ Generates images using **Stability AI**  
✅ Displays images in the **frontend**  
✅ Provides a **download option** for images  

## Future Enhancements
- Add support for **custom resolution** and **styles**.
- Implement **user authentication** for saved images.
- Improve **UI/UX** with better responsiveness.
- Add **webhooks** for real-time image processing updates.

## Contributing
Feel free to fork this repository and submit a pull request. Contributions are always welcome! 🚀

## License
This project is licensed under the **MIT License**.

---
Made with ❤️ by Shadow
