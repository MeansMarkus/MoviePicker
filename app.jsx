import React, { useState } from 'react';

const FilmReelLoader = () => {
    return (
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <lottie-player
          src="https://lottie.host/06e5fcfc-1a3a-4c2c-930b-8ab64a3edbc6/2stN8voztY.json"
          background="transparent"
          speed="1"
          style={{ width: '200px', height: '200px', margin: '0 auto' }}
          loop
          autoplay
        />
      </div>
    );
  };
  

const App = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const handleFetch = async () => {
    setLoading(true);
    const res = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_inputs: ['Inception', 'Shrek'] }),
    });
    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  return (
    <div>
      <h1>Movie Recommender</h1>
      <button onClick={handleFetch}>Get Recommendations</button>
      {loading ? (
        <FilmReelLoader />
      ) : (
        data && (
          <div>
            <h3>Recommendations</h3>
            <ul>
              {data.recommendations.map((m, i) => (
                <li key={i}>{m.title}</li>
              ))}
            </ul>
          </div>
        )
      )}
    </div>
  );
};

export default App;
