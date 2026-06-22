import { useState, useRef } from "react";
import "./App.css";

function App() {
  const [started, setStarted] = useState(false);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ NEW INPUT STATES (ADDED FOR AGRICULTURE PROJECT)
  const [city, setCity] = useState("");
  const [N, setN] = useState("");
  const [P, setP] = useState("");
  const [K, setK] = useState("");
  const [ph, setPh] = useState("");

  const cameraRef = useRef(null);
  const galleryRef = useRef(null);
  const fileRef = useRef(null);

  const handleSubmit = async () => {
  if (!file) {
    alert("Please select an image");
    return;
  }

  if (!city || !N || !P || !K || !ph) {
    alert("Please fill all fields");
    return;
  }

  setLoading(true);
  setResult(null);

  try {
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    const formData = new FormData();

    formData.append("file", file);

    // 🔥 IMPORTANT: ensure backend-friendly values
    formData.append("city", city);
    formData.append("N", Number(N));
    formData.append("P", Number(P));
    formData.append("K", Number(K));
    formData.append("ph", Number(ph));

    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    console.log("API RESPONSE:", data);

    if (!response.ok) {
      console.log("FULL ERROR:", JSON.stringify(data, null, 2));
    }

    setResult(data);
  } catch (error) {
    console.error("ERROR:", error);
    alert(error.message);
  } finally {
    setLoading(false);
  }
};

  if (!started) {
    return (
      <div className="landing">
        <h1 className="main-title">Smart Agriculture System</h1>
        <h2>AI Powered Crop & Fertilizer Recommendation</h2>
        <button className="start-btn" onClick={() => setStarted(true)}>
          Get Started
        </button>
      </div>
    );
  }

  return (
    <div className="predict-page">
      {/* hidden inputs (camera + gallery + file) */}
      <input
        ref={cameraRef}
        type="file"
        accept="image/*"
        capture="environment"
        style={{ display: "none" }}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <input
        ref={galleryRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <input
        ref={fileRef}
        type="file"
        style={{ display: "none" }}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div className="predict-card">
        <h1 className="main-title predict-title">
          Smart Agriculture Predictor
        </h1>

        {/* ================= INPUT FIELDS ================= */}
        <div className="inputs">
          <input
            placeholder="City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <input
            placeholder="Nitrogen (N)"
            value={N}
            onChange={(e) => setN(e.target.value)}
          />

          <input
            placeholder="Phosphorus (P)"
            value={P}
            onChange={(e) => setP(e.target.value)}
          />

          <input
            placeholder="Potassium (K)"
            value={K}
            onChange={(e) => setK(e.target.value)}
          />

          <input
            placeholder="pH value"
            value={ph}
            onChange={(e) => setPh(e.target.value)}
          />
        </div>

        {/* ================= BUTTONS (UNCHANGED) ================= */}
        <div className="buttons">
          <button onClick={() => cameraRef.current.click()}>
            📷 Take Photo
          </button>
          <button onClick={() => galleryRef.current.click()}>
            🖼️ Gallery
          </button>
          <button onClick={() => fileRef.current.click()}>
            📁 Upload File
          </button>
        </div>

        {/* IMAGE PREVIEW */}
        {file && (
          <img
            src={URL.createObjectURL(file)}
            alt="preview"
            className="preview"
          />
        )}

        {/* PREDICT BUTTON */}
        <button
          className="predict-btn"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict"}
        </button>

        {/* ================= RESULT (UPDATED FOR YOUR API) ================= */}
        {result && (
          <div className="result">
            <h2>🌱 Soil: {result.soil_type}</h2>

            <h3>🌾 Crop: {result.recommended_crop}</h3>

            <h3>🌿 Fertilizer: {result.fertilizer}</h3>

            <p>🌡 Temperature: {result.temperature}</p>
            <p>💧 Humidity: {result.humidity}</p>
            <p>🌧 Rainfall: {result.rainfall}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;