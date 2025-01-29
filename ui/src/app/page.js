"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [imageData, setImageData] = useState(null);
  const [loading, setLoading] = useState(false);

  const FLASK_ENDPOINT =
    "https://image-generator-pmi6.onrender.com/generate-image";

  const handleGenerate = async () => {
    if (!prompt) {
      alert("Please enter a prompt!");
      return;
    }

    setLoading(true);
    setImageData(null);

    try {
      const response = await fetch(FLASK_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || "Error generating image");
        setLoading(false);
        return;
      }

      const data = await response.json();
      setImageData(data.image_base64 || null);
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }

    setLoading(false);
  };

  const examplePrompts = [
    "A robotic jellyfish dancing in a neon ocean",
    "A medieval knight riding a giant corgi through a sushi restaurant",
    "A UFO shaped like a banana abducting a giant avocado",
    "A cat with laser eyes riding a motorcycle in a futuristic city",
    "A majestic eagle wearing a top hat playing electric guitar on Mars",
  ];

  const handleExampleClick = (example) => {
    setPrompt(example);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6">
      <h1 className="title-text text-4xl">Lumo Image Generator</h1>
      <p className="text-xl text-center max-w-2xl mb-6">
        Enter a prompt or pick one of the crazy examples below to generate an
        image.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {examplePrompts.map((ex, idx) => (
          <button
            key={idx}
            onClick={() => handleExampleClick(ex)}
            className="minimal-button"
          >
            {ex}
          </button>
        ))}
      </div>

      <textarea
        rows={3}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type a wild or creative prompt here..."
        className="mb-4 md:w-3/4 lg:w-1/2"
      />

      <button
        onClick={handleGenerate}
        className="minimal-button mt-2"
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Image"}
      </button>

      {imageData && (
        <div className="mt-10">
          <h2 className="title-text text-2xl mb-3">Generated Image</h2>
          <div className="relative group inline-block">
            <img
              src={`data:image/png;base64,${imageData}`}
              alt="Generated"
              className="max-w-[400px] h-auto rounded-md border border-gray-300 shadow"
            />
            <a
              href={`data:image/png;base64,${imageData}`}
              download="generated_image.png"
              className="download-overlay"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="download-icon"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3 16.5v2.25c0 
                    .414.336.75.75.75h16.5c.414 
                    0 .75-.336.75-.75V16.5M7.5 
                    10.5l4.5 4.5 4.5-4.5M12 
                    3.75v11.25"
                />
              </svg>
            </a>
          </div>
        </div>
      )}
    </main>
  );
}
