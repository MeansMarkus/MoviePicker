const firebaseConfig = {
  apiKey: "AIzaSyD1wAKyRzU9EavqFUgvofwelpj7gM79sbY",
  authDomain: "moviepicker-e14f4.firebaseapp.com",
  projectId: "moviepicker-e14f4",
  storageBucket: "moviepicker-e14f4.firebasestorage.app",
  messagingSenderId: "164660100747",
  appId: "1:164660100747:web:bb074c168dc4b7f5131e8e",
  measurementId: "G-YJF568XBTE"
};

// This function will be called when the DOM is loaded
function setupUserLoginSystem() {
  // Firebase Imports (Add these to the <head> section of your HTML)
  // <script type="module">
  //   import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
  //   import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-analytics.js";
  //   import { getAuth } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
  //   window.initializeFirebase = function() {
  //     window.firebaseApp = initializeApp(firebaseConfig);
  //     window.firebaseAuth = getAuth(window.firebaseApp);
  //     window.firebaseAnalytics = getAnalytics(window.firebaseApp);
  //   };
  // </script>

  // Initialize Firebase if it's not already initialized
  if (!window.firebaseAuth) {
    console.error("Firebase Auth not initialized! Make sure to add the Firebase scripts to your HTML.");
    return;
  }

  // Elements
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const userProfile = document.getElementById('user-profile');
  const movieSection = document.getElementById('recommendation-form');
  
  const loginEmail = document.getElementById('login-email');
  const loginPassword = document.getElementById('login-password');
  const loginBtn = document.getElementById('login-btn');
  
  const signupName = document.getElementById('signup-name');
  const signupEmail = document.getElementById('signup-email');
  const signupPassword = document.getElementById('signup-password');
  const signupBtn = document.getElementById('signup-btn');
  
  const userName = document.getElementById('user-name');
  const logoutBtn = document.getElementById('logout-btn');
  
  const showSignupLink = document.getElementById('show-signup');
  const showLoginLink = document.getElementById('show-login');
  
  // Toggle between login and signup forms
  showSignupLink.addEventListener('click', (e) => {
    e.preventDefault();
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
  });
  
  showLoginLink.addEventListener('click', (e) => {
    e.preventDefault();
    signupForm.style.display = 'none';
    loginForm.style.display = 'block';
  });

  // Login functionality
  loginBtn.addEventListener('click', async () => {
    const email = loginEmail.value;
    const password = loginPassword.value;
    
    if (!email || !password) {
      alert('Please enter both email and password');
      return;
    }
    
    try {
      const { signInWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js');
      await signInWithEmailAndPassword(window.firebaseAuth, email, password);
      // Login successful - UI will update via auth state listener
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed: ' + error.message);
    }
  });
  
  // Sign up functionality
  signupBtn.addEventListener('click', async () => {
    const name = signupName.value;
    const email = signupEmail.value;
    const password = signupPassword.value;
    
    if (!name || !email || !password) {
      alert('Please fill out all fields');
      return;
    }
    
    try {
      const { createUserWithEmailAndPassword, updateProfile } = await import('https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js');
      const userCredential = await createUserWithEmailAndPassword(window.firebaseAuth, email, password);
      
      // Update user profile with display name
      await updateProfile(userCredential.user, {
        displayName: name
      });
      
      // Signup successful - UI will update via auth state listener
    } catch (error) {
      console.error('Signup error:', error);
      alert('Sign up failed: ' + error.message);
    }
  });
  
  // Logout functionality
  logoutBtn.addEventListener('click', async () => {
    try {
      const { signOut } = await import('https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js');
      await signOut(window.firebaseAuth);
      // Logout successful - UI will update via auth state listener
    } catch (error) {
      console.error('Logout error:', error);
      alert('Logout failed: ' + error.message);
    }
  });
  
  // Listen for auth state changes
  const { onAuthStateChanged } = await import('https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js');
  onAuthStateChanged(window.firebaseAuth, (user) => {
    if (user) {
      // User is signed in
      userName.textContent = user.displayName || user.email;
      loginForm.style.display = 'none';
      signupForm.style.display = 'none';
      userProfile.style.display = 'block';
      
      // Enable movie picker functionality
      if (movieSection) {
        movieSection.style.display = 'block';
      }
      
      // Load saved movies if applicable
      loadSavedMovies(user.uid);
    } else {
      // User is signed out
      loginForm.style.display = 'block';
      signupForm.style.display = 'none';
      userProfile.style.display = 'none';
      
      // Disable movie picker functionality (optional)
      if (movieSection) {
        // Either hide it or keep it visible for non-logged in users
        // movieSection.style.display = 'none';
      }
    }
  });
}

// Function to load saved movies from Firebase (this is a placeholder - implement as needed)
async function loadSavedMovies(userId) {
  try {
    const { getFirestore, collection, query, where, getDocs } = 
      await import('https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js');
    
    const db = getFirestore(window.firebaseApp);
    const savedMoviesCollection = collection(db, 'savedMovies');
    const userMoviesQuery = query(savedMoviesCollection, where('userId', '==', userId));
    
    const querySnapshot = await getDocs(userMoviesQuery);
    const savedMoviesList = document.getElementById('saved-movies-list');
    savedMoviesList.innerHTML = '';
    
    querySnapshot.forEach((doc) => {
      const movieData = doc.data();
      const li = document.createElement('li');
      li.textContent = movieData.title;
      savedMoviesList.appendChild(li);
    });
    
    if (querySnapshot.empty) {
      savedMoviesList.innerHTML = '<li>No saved movies yet.</li>';
    }
  } catch (error) {
    console.error('Error loading saved movies:', error);
  }
}