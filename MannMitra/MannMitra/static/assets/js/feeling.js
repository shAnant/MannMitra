async function analyzeMood() {
  const text = document.getElementById("moodInput").value;
  const resultDiv = document.getElementById("moodResult");

  if (!text) {
    resultDiv.innerHTML = "⚠️ Please type something first.";
    resultDiv.style.color = "red";
    return;
  }

  try {
    // Call your Django API endpoint
    const response = await fetch("http://127.0.0.1:8000/analyze/text/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });

    const data = await response.json();

    // Assuming your API returns something like { emotion: "stressed", score: 0.85 }
    resultDiv.innerHTML = `Detected Emotion: <b>${data.emotion}</b> (confidence: ${(data.score * 100).toFixed(1)}%)`;

    // Optional color feedback
    if (data.emotion === "happy") resultDiv.style.color = "green";
    else if (data.emotion === "sad") resultDiv.style.color = "blue";
    else if (data.emotion === "stressed") resultDiv.style.color = "orange";
    else resultDiv.style.color = "gray";

  } catch (error) {
    console.error("Error analyzing mood:", error);
    resultDiv.innerHTML = "❌ Could not analyze mood. Please try again later.";
    resultDiv.style.color = "red";
  }
}
