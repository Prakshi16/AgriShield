import React, { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please choose a file first!");

    const formData = new FormData();
    formData.append("image", file);

    await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    alert("File uploaded!");
  };

  return (
    <div className="upload-box">
      <div className="upload-area">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Choose Photo</button>
      </div>
      <div className="tips">
        <h4>📸 Tips for best results:</h4>
        <ul>
          <li>Take photos in good lighting</li>
          <li>Focus on affected leaves or areas</li>
          <li>Avoid blurry or distant shots</li>
          <li>Include multiple affected areas if possible</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadForm;
