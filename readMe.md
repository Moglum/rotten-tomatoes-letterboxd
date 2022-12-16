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
  `https://www.rottentomatoes.com/user/id/<your ID>/`

- [Letterboxd](https://letterboxd.com) account to import the reviews

# How to

1. Clone or download the repo
2. Run `npm install` in the root folder of the repo to install the dependencies
3. Log into Rotten Tomatoes. Save the output of `https://www.rottentomatoes.com/napi/userProfile/movieRatings/<your ID>`
   to a file called `input.json` in this project's root.
4. Run `npm start` It might take a while, the script gets max 20 reviews
   with each request.
5. When finished you should have a file 'importMe.csv' waiting for you
   (another file gets created - the raw Rotten Tomatoes format - rawRatings.json
   you can ignore it)
6. Import the file right here https://letterboxd.com/import/
7. Profit

# Known issues

- Rotten Tomatoes no longer provides the Director.
