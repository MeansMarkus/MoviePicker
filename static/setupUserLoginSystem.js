// Security: Implements signup/login forms, stores sessions in localStorage, and toggles UI on auth state. 

// This function will inject everything we need - both HTML and styles
function setupUserLoginSystem() {
    // Create the login UI HTML
    const loginHTML = `
      <div class="section" id="login-section">
        <h2>User Account</h2>
        <div id="login-container">
          <div id="login-form" class="auth-form">
            <h3>Login</h3>
            <input type="email" id="login-email" placeholder="Email" required>
            <input type="password" id="login-password" placeholder="Password" required>
            <button type="button" id="login-btn">Login</button>
            <p>Don't have an account? <a href="#" id="show-signup">Sign up</a></p>
          </div>
          
          <div id="signup-form" class="auth-form" style="display:none">
            <h3>Create Account</h3>
            <input type="text" id="signup-name" placeholder="Name" required>
            <input type="email" id="signup-email" placeholder="Email" required>
            <input type="password" id="signup-password" placeholder="Password" required>
            <button type="button" id="signup-btn">Sign Up</button>
            <p>Already have an account? <a href="#" id="show-login">Login</a></p>
          </div>
          
          <div id="user-profile" style="display:none">
            <h3>Welcome, <span id="user-name">User</span>!</h3>
            <button type="button" id="logout-btn">Logout</button>
            
            <div class="section" id="saved-movies-section">
              <h3> 
                Your Saved Movies 
                <button type="button" id="toggle-saved-movies" class="toggle-button">▶</button>
                <ul id="saved-movies-list" style="display:none;"></ul>
              </h3>
            </div>
          </div>
        </div>
      </div>
    `;
  
    // Create and add CSS styles dynamically
    const styleElement = document.createElement('style');
    styleElement.textContent = `
      .auth-form {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 6px;
      }
  
      .auth-form input {
        display: block;
        width: 100%;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #444;
        border-radius: 4px;
        background-color: #1e1e1e;
        color: #f1f1f1;
      }
  
      .auth-form a {
        color: #3FB8AF;
        text-decoration: none;
      }
  
      .auth-form a:hover {
        text-decoration: underline;
      }
  
      .movie-rating {
        display: flex;
        align-items: center;
        margin-top: 0.5rem;
      }
  
      .star {
        color: #aaa;
        font-size: 1.2rem;
        cursor: pointer;
        margin-right: 0.2rem;
      }
  
      .star.active {
        color: #FFD700;
      }
  
      .save-movie-btn {
        background-color: #3FB8AF;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.3rem 0.6rem;
        margin-left: 0.5rem;
        cursor: pointer;
        font-size: 0.8rem;
      }
  
      .save-movie-btn:hover {
        background-color: #30928c;
      }
  
      .movie-item {
        position: relative;
      }
  
      .rating-value {
        margin-left: 0.5rem;
        font-size: 0.9rem;
      }
  
      .user-rating-label {
        margin-right: 0.5rem;
        font-size: 0.9rem;
      }
      
      .remove-saved-movie {
        margin-left: 1rem;
        background: transparent;
        border: none;
        color: #e57373;
        cursor: pointer;
        font-size: 0.8rem;

      }
      .remove-saved-movie:hover {
        text-decoration: underline;
        background: transparent;
      }

      .toggle-button {
        background: none;
        border: none;
        color: #3FB8AF;
        font-size: 1.1rem;
        cursor: pointer;
        margin-right: 0.5rem;
      }
    `;
    document.head.appendChild(styleElement);
  
    // Insert the login section after the instructions section
    const instructionsSection = document.getElementById('instructions');
    const loginSectionDiv = document.createElement('div');
    loginSectionDiv.innerHTML = loginHTML;
    instructionsSection.after(loginSectionDiv.firstElementChild);
    
    const toggleBtn = document.getElementById('toggle-saved-movies');
    const savedList = document.getElementById('saved-movies-list');
    toggleBtn.addEventListener('click', () => {
      const open = savedList.style.display === 'block';
      savedList.style.display = open ? 'none' : 'block';
      toggleBtn.textContent = open ? '▶' : '▼';
    });
  
    // Authentication state
    let currentUser = null;
    
    // Check if user is already logged in
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      currentUser = JSON.parse(storedUser);
      updateUIForLoggedInUser(currentUser);
    }
    
    // Login form toggle
    document.getElementById('show-signup').addEventListener('click', function(e) {
      e.preventDefault();
      document.getElementById('login-form').style.display = 'none';
      document.getElementById('signup-form').style.display = 'block';
    });
    
    document.getElementById('show-login').addEventListener('click', function(e) {
      e.preventDefault();
      document.getElementById('signup-form').style.display = 'none';
      document.getElementById('login-form').style.display = 'block';
    });
    
    // Login functionality
    document.getElementById('login-btn').addEventListener('click', function() {
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      
      if (!email || !password) {
        alert('Please enter both email and password');
        return;
      }
      
      // Get users from localStorage
      const users = JSON.parse(localStorage.getItem('users') || '[]');
      const user = users.find(u => u.email === email && u.password === password);
      
      if (user) {
        currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        updateUIForLoggedInUser(user);
      } else {
        alert('Invalid email or password');
      }
    });
    
    // Signup functionality
    document.getElementById('signup-btn').addEventListener('click', function() {
      const name = document.getElementById('signup-name').value;
      const email = document.getElementById('signup-email').value;
      const password = document.getElementById('signup-password').value;
      
      if (!name || !email || !password) {
        alert('Please fill in all fields');
        return;
      }
      
      // Get existing users
      const users = JSON.parse(localStorage.getItem('users') || '[]');
      
      // Check if email already exists
      if (users.some(u => u.email === email)) {
        alert('Email already registered');
        return;
      }
      
      // Create new user
      const newUser = {
        id: Date.now().toString(),
        name,
        email,
        password,
        savedMovies: []
      };
      
      // Save user
      users.push(newUser);
      localStorage.setItem('users', JSON.stringify(users));
      
      // Login the user
      currentUser = newUser;
      localStorage.setItem('currentUser', JSON.stringify(currentUser));
      updateUIForLoggedInUser(newUser);
      
      alert('Account created successfully!');
    });
    
    // Logout functionality
    document.getElementById('logout-btn').addEventListener('click', function() {
      localStorage.removeItem('currentUser');
      currentUser = null;
      
      document.getElementById('user-profile').style.display = 'none';
      document.getElementById('login-form').style.display = 'block';
      document.getElementById('user-name').textContent = 'User';
      document.getElementById('saved-movies-list').innerHTML = '';
    });
    
    function updateUIForLoggedInUser(user) {
      document.getElementById('login-form').style.display = 'none';
      document.getElementById('signup-form').style.display = 'none';
      document.getElementById('user-profile').style.display = 'block';
      document.getElementById('user-name').textContent = user.name;
      
      // Load saved movies
      loadSavedMovies();
    }
    
    function loadSavedMovies() {
      if (!currentUser) return;
      const savedMoviesList = document.getElementById('saved-movies-list');
      savedMoviesList.innerHTML = '';
    
      // Refresh currentUser data
      const users = JSON.parse(localStorage.getItem('users') || '[]');
      const updatedUser = users.find(u => u.id === currentUser.id);
      if (!updatedUser) return;
    
      // Dedupe by title
      const uniqueMovies = [
        ...new Map(updatedUser.savedMovies.map(m => [m.title, m])).values()
      ];
    
      if (uniqueMovies.length > 0) {
        uniqueMovies.forEach((movie, idx) => {
          const li = document.createElement('li');
          li.innerHTML = `
            <strong>${movie.title} (${movie.year || 'N/A'})</strong>
            <button class="remove-saved-movie" data-index="${idx}">Remove</button>
            <div class="movie-rating">
              <span class="user-rating-label">Your rating:</span>
              ${renderStars(movie.userRating || 0, movie.id, true)}
              <span class="rating-value">${movie.userRating || 'Not rated'}</span>
            </div>
          `;
          savedMoviesList.appendChild(li);
        });
    
        // Delegate remove clicks
        savedMoviesList.addEventListener('click', e => {
          if (!e.target.classList.contains('remove-saved-movie')) return;
          const removeIdx = parseInt(e.target.dataset.index, 10);
    
          // Remove from array & persist
          updatedUser.savedMovies = uniqueMovies.filter((_, i) => i !== removeIdx);
          const allUsers = JSON.parse(localStorage.getItem('users') || '[]');
          const ui = allUsers.findIndex(u => u.id === updatedUser.id);
          allUsers[ui] = updatedUser;
          localStorage.setItem('users', JSON.stringify(allUsers));
          localStorage.setItem('currentUser', JSON.stringify(updatedUser));
    
          // Re-render
          loadSavedMovies();
        });
    
        // Update currentUser in storage
        currentUser = updatedUser;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
      } else {
        savedMoviesList.innerHTML = '<li>No saved movies yet.</li>';
      }
    }    
  
  }

function addMovieInteractions(listId) {
  const movieList = document.getElementById(listId);
  if (!movieList) return;

  const movieItems = movieList.querySelectorAll('li');
  movieItems.forEach((item, index) => {
    // Don’t double-add
    if (item.querySelector('.movie-interaction')) return;

    // Grab the title text
    const titleElement = item.querySelector('strong');
    const fullText     = titleElement ? titleElement.textContent : '';

    // Extract a trailing "(YYYY)" if present
    const match    = fullText.match(/\((\d{4})\)$/);
    const movieYear  = match ? match[1] : '';

    // Strip off " (YYYY)" from the title for storage
    const movieTitle = match
      ? fullText.replace(/\s*\(\d{4}\)$/, '')
      : fullText;

    // Build unique ID
    const movieId = `movie-${listId}-${index}`;

    // Create star-rating + Save button UI
    const interactionDiv = document.createElement('div');
    interactionDiv.className = 'movie-interaction';
    interactionDiv.innerHTML = `
      <div class="movie-rating">
        <span class="user-rating-label">Rate:</span>
        ${renderStars(0, movieId)}
        <span class="rating-value" id="rating-value-${movieId}">Not rated</span>
        <button class="save-movie-btn"
                data-movie-id="${movieId}"
                data-movie-title="${movieTitle}"
                data-movie-year="${movieYear}">
          Save Movie
        </button>
      </div>
    `;
    item.appendChild(interactionDiv);

    // Wire up Save button to saveMovie()
    const saveBtn = interactionDiv.querySelector('.save-movie-btn');
    saveBtn.addEventListener('click', () => {
      saveMovie(
        saveBtn.dataset.movieId,
        saveBtn.dataset.movieTitle,
        saveBtn.dataset.movieYear
      );
    });
  });
}

  
  function renderStars(currentRating = 0, movieId, readonly = false) {
    let starsHtml = '';
    
    for (let i = 1; i <= 5; i++) {
      const activeClass = i <= currentRating ? 'active' : '';
      
      if (readonly) {
        starsHtml += `<span class="star ${activeClass}">★</span>`;
      } else {
        starsHtml += `<span class="star ${activeClass}" data-rating="${i}" data-movie-id="${movieId}">★</span>`;
      }
    }
    
    // Add click handlers if not readonly
    setTimeout(() => {
      if (!readonly) {
        const stars = document.querySelectorAll(`.star[data-movie-id="${movieId}"]`);
        stars.forEach(star => {
          star.addEventListener('click', function() {
            const rating = parseInt(this.dataset.rating);
            updateStarRating(movieId, rating);
          });
        });
      }
    }, 0);
    
    return starsHtml;
  }
  
  function updateStarRating(movieId, rating) {
    // Update visual stars
    const stars = document.querySelectorAll(`.star[data-movie-id="${movieId}"]`);
    stars.forEach(star => {
      const starRating = parseInt(star.dataset.rating);
      if (starRating <= rating) {
        star.classList.add('active');
      } else {
        star.classList.remove('active');
      }
    });
    
    // Update rating value display
    const ratingValueElement = document.getElementById(`rating-value-${movieId}`);
    if (ratingValueElement) {
      ratingValueElement.textContent = rating.toString();
    }
    
    // Update saved movie if this movie is already saved
    updateSavedMovieRating(movieId, rating);
  }
  
  function saveMovie(movieId, title, year) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
      alert('Please log in to save movies');
      document.getElementById('login-form').scrollIntoView({ behavior: 'smooth' });
      return;
    }
    
    // Get the current rating
    const ratingElement = document.getElementById(`rating-value-${movieId}`);
    const rating = ratingElement && ratingElement.textContent !== 'Not rated' 
      ? parseInt(ratingElement.textContent) 
      : 0;
    
    // Get all users to update the current user
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    if (userIndex === -1) {
      alert('User not found. Please log in again.');
      return;
    }
    
    // Check if movie is already saved
    const savedMovieIndex = users[userIndex].savedMovies.findIndex(m => 
      m.title === title && m.year === year);
    
    if (savedMovieIndex !== -1) {
      // Update existing saved movie
      users[userIndex].savedMovies[savedMovieIndex].userRating = rating;
      alert('Movie rating updated!');
    } else {
      // Add new saved movie
      users[userIndex].savedMovies.push({
        id: movieId,
        title: title,
        year: year,
        userRating: rating,
        dateSaved: new Date().toISOString()
      });
      alert('Movie saved to your profile!');
    }
    
    // Update users in localStorage
    localStorage.setItem('users', JSON.stringify(users));
    
    // Update current user
    localStorage.setItem('currentUser', JSON.stringify(users[userIndex]));
    
    // Refresh the saved movies list
    loadSavedMovies();
  }
  
  function updateSavedMovieRating(movieId, rating) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;
    
    // Get all users to update the current user
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    if (userIndex === -1) return;
    
    // Find the movie in saved movies
    const savedMovieIndex = users[userIndex].savedMovies.findIndex(m => m.id === movieId);
    
    if (savedMovieIndex !== -1) {
      // Update the rating
      users[userIndex].savedMovies[savedMovieIndex].userRating = rating;
      
      // Update users in localStorage
      localStorage.setItem('users', JSON.stringify(users));
      
      // Update current user
      localStorage.setItem('currentUser', JSON.stringify(users[userIndex]));
      
      // Refresh the saved movies list
      loadSavedMovies();
    }
  }
  
  function loadSavedMovies() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;
  
    const savedMoviesList = document.getElementById('saved-movies-list');
    savedMoviesList.innerHTML = '';
  
    // Re-fetch latest user data
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const updatedUser = users.find(u => u.id === currentUser.id);
    if (!updatedUser) return;
  
    // Strip year from title and dedupe by title
    const uniqueMovies = Array.from(
      updatedUser.savedMovies
        .map(m => {
          // e.g. m.title = "Iron Man 3 (2013)" → strip the year suffix
          const match = m.title.match(/^(.*)\s*\((\d{4})\)$/);
          return {
            ...m,
            title: match ? match[1] : m.title,
            year: match ? match[2] : m.year || ''
          };
        })
        .reduce((map, m) => map.set(m.title, m), new Map())
        .values()
    );
  
    if (uniqueMovies.length === 0) {
      savedMoviesList.innerHTML = '<li>No saved movies yet.</li>';
      return;
    }
  
    uniqueMovies.forEach((movie, idx) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <strong>${movie.title} (${movie.year || 'N/A'})</strong>
        <button class="remove-saved-movie" data-index="${idx}">Remove</button>
        <div class="movie-rating">
          <span class="user-rating-label">Your rating:</span>
          ${renderStars(movie.userRating || 0, movie.id, true)}
          <span class="rating-value">${movie.userRating || 'Not rated'}</span>
        </div>
      `;
      savedMoviesList.appendChild(li);
    });
  
    // Delegate removal clicks
    savedMoviesList.onclick = (e) => {
      if (!e.target.classList.contains('remove-saved-movie')) return;
      const removeIdx = parseInt(e.target.dataset.index, 10);
  
      // Remove and persist
      const toKeep = uniqueMovies.filter((_, i) => i !== removeIdx);
      updatedUser.savedMovies = toKeep;
      const allUsers = JSON.parse(localStorage.getItem('users') || '[]');
      const userPos = allUsers.findIndex(u => u.id === updatedUser.id);
      allUsers[userPos] = updatedUser;
      localStorage.setItem('users', JSON.stringify(allUsers));
      localStorage.setItem('currentUser', JSON.stringify(updatedUser));
  
      loadSavedMovies();  // re-render
    };
  
    // Update currentUser in storage
    currentUser = updatedUser;
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
  }
  