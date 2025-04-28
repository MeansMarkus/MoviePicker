document.getElementById("recommendation-form").addEventListener("submit", async function(event) {
    event.preventDefault();
  
    // Show the loading spinner when fetching recommendations
    document.getElementById("loading-spinner").style.display = "block";
  
    const users = [];
    for (let i = 1; i <= userCount; i++) {
      const url = document.getElementById(`user${i}-url`).value.trim();
      const manual = window[`selectedMovies${i}`]() || [];
      if (url) {
        users.push(url);
      } else if (manual.length) {
        users.push(manual);
      }
    }
  
    const includeText = document.getElementById("filter-include").value.trim();
    const excludeText = document.getElementById("filter-exclude").value.trim();
    const include = includeText ? includeText.split(",").map(w => w.trim()).filter(Boolean) : [];
    const exclude = excludeText ? excludeText.split(",").map(w => w.trim()).filter(Boolean) : [];
    const contentRatings = Array.from(document.querySelectorAll('#filter-content-ratings input:checked')).map(cb => cb.value);
    const [minRating, maxRating] = ratingSlider.noUiSlider.get().map(v => parseFloat(v));
    const payload = { users, include, exclude, content_ratings: contentRatings, rating_min: minRating, rating_max: maxRating, genres: selectedGenres };
  
    try {
      const resp = await fetch("/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
  
      // Hide the loading spinner once recommendations are fetched
      document.getElementById("loading-spinner").style.display = "none";
  
      // Show results
      const resultsDiv = document.getElementById("results");
      const overlapSec = document.getElementById("overlap-section");
      const overlapList = document.getElementById("overlap-list");
      const recSec = document.getElementById("recommendation-section");
      const recList = document.getElementById("recommendation-list");
  
      overlapSec.style.display = 'block';
      overlapList.innerHTML = data.overlapMovies.map(movie => `<li>${movie}</li>`).join('');
      recSec.style.display = 'block';
      recList.innerHTML = data.recommendations.map(movie => `<li>${movie}</li>`).join('');
      resultsDiv.style.display = 'block';
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      document.getElementById("loading-spinner").style.display = "none";
    }
  });
  