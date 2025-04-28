document.addEventListener("DOMContentLoaded", () => {
  const form    = document.getElementById("recommendation-form");
  const spinner = document.getElementById("loading-spinner");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    spinner.style.display = "flex";

    // build users array
    const users = [];
    for (let i = 1; i <= userCount; i++) {
      const url    = document.getElementById(`user${i}-url`).value.trim();
      const manual = window[`selectedMovies${i}`]() || [];
      if (url)                users.push(url);
      else if (manual.length) users.push(manual);
    }

    // build filters
    const includeText    = document.getElementById("filter-include").value.trim();
    const excludeText    = document.getElementById("filter-exclude").value.trim();
    const include        = includeText ? includeText.split(",").map(w => w.trim()).filter(Boolean) : [];
    const exclude        = excludeText ? excludeText.split(",").map(w => w.trim()).filter(Boolean) : [];
    const contentRatings = Array.from(
      document.querySelectorAll('#filter-content-ratings input:checked')
    ).map(cb => cb.value);
    const [minRating, maxRating] = ratingSlider.noUiSlider.get().map(v => parseFloat(v));

    const payload = {
      users,
      include,
      exclude,
      content_ratings: contentRatings,
      rating_min: minRating,
      rating_max: maxRating,
      genres: selectedGenres
    };

    try {
      const resp = await fetch("/recommendations", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(payload)
      });
      const data = await resp.json();

      spinner.style.display = "none";

      // grab the container elements
      const resultsDiv  = document.getElementById("results");
      const overlapSec  = document.getElementById("overlap-section");
      const overlapList = document.getElementById("overlap-list");
      const recSec      = document.getElementById("recommendation-section");
      const recList     = document.getElementById("recommendation-list");

      // clear old
      overlapList.innerHTML = "";
      recList.innerHTML     = "";

      // populate overlap (now treating items as objects)
      if (data.overlap && data.overlap.length) {
        overlapSec.style.display = "block";
        data.overlap.forEach(movie => {
          const li = document.createElement("li");
          li.innerHTML = `
            <strong>${movie.title} (${(movie.release_date||"").slice(0,4) || "?"})</strong>
            <!-- optional: (${movie.release_date?.split("-")[0]||"?"}) -->
            <button class="summary-toggle">▼</button>
            <div class="content-rating">${movie.content_rating||"NR"} | Audience Rating: ${movie.rating||"N/A"}</div>
            <div class="summary" style="display:none">${movie.summary||"No summary."}</div>
          `;
          // toggle summary
          li.querySelector(".summary-toggle").onclick = e => {
            const summ = li.querySelector(".summary");
            const show = summ.style.display === "none";
            summ.style.display = show ? "block" : "none";
            e.target.textContent = show ? "▲" : "▼";
          };
          overlapList.appendChild(li);
        });
      } else {
        overlapSec.style.display = "none";
      }

      // populate recommendations
      if (data.recommendations && data.recommendations.length) {
        recSec.style.display = "block";
        data.recommendations.forEach(movie => {
          const li = document.createElement("li");
          li.innerHTML = `
            <strong>${movie.title} (${(movie.release_date||"").slice(0,4) || "?"})</strong>
            <button class="summary-toggle">▼</button>
            <div class="content-rating">${movie.content_rating||"NR"} | Rating: ${movie.rating||"N/A"}</div>
            <div class="summary" style="display:none">${movie.summary||"No summary."}</div>
          `;
          li.querySelector(".summary-toggle").onclick = e => {
            const summ = li.querySelector(".summary");
            const show = summ.style.display === "none";
            summ.style.display = show ? "block" : "none";
            e.target.textContent = show ? "▲" : "▼";
          };
          recList.appendChild(li);
        });
      } else {
        recSec.style.display = "none";
      }

      resultsDiv.style.display = "block";

      if (typeof addMovieInteractions === "function") {
        addMovieInteractions("overlap-list");
        addMovieInteractions("recommendation-list");
      } else {
        console.warn("addMovieInteractions is not defined");
      }

    } catch (error) {
      console.error("Error fetching recommendations:", error);
      spinner.style.display = "none";
    }
  });
});
