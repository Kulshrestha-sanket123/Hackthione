app.post('/register', (req, res) => {
  const { username, email, password } = req.body;
  // Save the user into database
  db.users.insert({ username, email, password, profile: { bio: '', picture: '' } });
  res.redirect('/profile-setup');
});
  