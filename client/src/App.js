import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]; // ✅ FIXED: declare properly
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleUpload = async () => {
  if (!file) return alert("Please choose a file!");

  const formData = new FormData();
  formData.append("file", file); // ✅ must be "file" to match Flask

  try {
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    alert("Prediction: " + data.prediction);
  } catch (err) {
    console.error(err);
    alert("Upload failed");
  }
};


  return (
    <div className="app">
      <header className="header">
        <div className="logo">🌱 AgriShield</div>
        <p>Upload a photo and detect crop diseases instantly!</p>
      </header>

      <main className="upload-section">
        {!preview ? ( // ⭐ NEW: Conditional UI (choose vs uploaded)
          <div className="upload-box">
            <div className="upload-icon">📷</div>
            <h2>Upload Plant Photo</h2>
            <p>
              Take a clear photo of the affected plant leaves or drag and drop
              an image here
            </p>

            <input
              type="file"
              id="fileInput"
              onChange={handleFileChange}
              hidden
            />
            <button
              className="choose-btn"
              onClick={() => document.getElementById("fileInput").click()}
            >
              Choose Photo
            </button>
          </div>
        ) : (
          <div className="preview-card">
            {" "}
            {/* ⭐ NEW: Preview UI */}
            <div className="preview-header">
              <h3>Uploaded Image</h3>
              <button
                className="choose-btn"
                onClick={() => {
                  document.getElementById("fileInput").click();
                }}
              >
                Upload New
              </button>
              <input
                type="file"
                id="fileInput"
                onChange={handleFileChange}
                hidden
              />
            </div>
            <img src={preview} alt="Uploaded preview" className="preview-img" />
            <button className="analyze-btn" onClick={handleUpload}>
              🍃 Analyze Plant Health
            </button>
          </div>
        )}
      </main>

      <footer className="footer">
        © 2025 AgriShield. Helping farmers protect their crops with AI.
      </footer>
    </div>
  );
}

export default App;
