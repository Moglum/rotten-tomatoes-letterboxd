I wanted to transfer my 1000+ reviews from
[Rotten Tomatoes](https://www.rottentomatoes.com)
to [Letterboxd](https://letterboxd.com),
so I wrote this simple script to help me. It gets all the reviews for a given
User ID and creates a CSV file to be directly imported into Letterboxd. No extra
steps needed.

Both your 0-5 rating and the review text will be transfered. For each movie the
script gets Title, Year and Director Name to help Letterboxd correctly identify
the movie during import.

It might not be perfect, but it has worked for me. If you have any problems with
it, submit an issue and I'll try to help ;)

# Requirements

- [Node.js and npm](https://nodejs.org) - to run the script
- Your [Rotten Tomatoes](https://www.rottentomatoes.com) user ID

  Go to your Profile and it's the last part of the URL -
  `https://www.rottentomatoes.com/user/id/<your ID/`

- Your Rotten Tomatoes Profile must be public at least for the duration of the script running
  (it uses a public API to get your ratings, no authentication needed)

  Go to [Profile Privacy settings](https://www.rottentomatoes.com/user/account/profile_preferences/)
  and set visibility to: _Show to all. Everybody (including anonymous users) can see my profile._

- [Letterboxd](https://letterboxd.com) account to import the reviews

# How to

1. Clone or download the repo
2. Run `npm install` in the root folder of the repo to install the dependencies
3. Open `index.js` and replace `YOUR_ID` with your Rotten Tomatoes ID on line 8
4. Open `index.js` and replace `COOKIE` with the cookie you retrieve from the screenshot below. See the discussion in in #8 as to why this is necessary.
5. Run `npm start` It might take a while, the script gets max 20 reviews
   with each request.
6. When finished you should have a file 'importMe.csv' waiting for you
   (another file gets created - the raw Rotten Tomatoes format - rawRatings.json
   you can ignore it)
7. Import the file right here https://letterboxd.com/import/
8. Profit

<img width="1493" alt="Screenshot 2023-01-21 at 3 36 41 PM" src="https://user-images.githubusercontent.com/1892194/213886227-05096d0a-2778-40e1-9b15-a4e13e8fe651.png">

# Known issues

- The Rotten Tomatoes API doesn't return the exact date for each review, just an
  offset. Like `3 days`, `5 months` or `6 years`. I use these offsets
  to approximate the review date: `TODAY - offset`
