import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please choose a file!");

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      alert(data.message);
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
        <div className="upload-box">
          <div className="upload-icon">📷</div>
          <h2>Upload Plant Photo</h2>
          <p>
            Take a clear photo of the affected plant leaves or drag and drop an
            image here
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

          {file && <p className="filename">{file.name}</p>}

          <div className="tips">
            <h4>📸 Tips for best results:</h4>
            <ul>
              <li>Take photos in good lighting</li>
              <li>Focus on affected leaves or areas</li>
              <li>Avoid blurry or distant shots</li>
              <li>Include multiple affected areas if possible</li>
            </ul>
          </div>

          <button className="upload-btn" onClick={handleUpload}>
            Upload
          </button>
        </div>
      </main>

      <footer className="footer">
        © 2025 CAgriShield. Helping farmers protect their crops with AI
        technology.
      </footer>
    </div>
  );
}

export default App;
