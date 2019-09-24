const rp = require('request-promise-native');
const fs = require('fs');
const { DateTime } = require('luxon');

const URI = 'https://www.rottentomatoes.com/napi/userProfile/movieRatings/';

// Change to your Rotten Tomatoes user ID
const USER_ID = 'YOUR_ID';

async function getRatings(cursor) {
  try {
    let res = await rp({
      uri: URI + USER_ID,
      json: true,
      qs: { endCursor: cursor }
    });

    console.log('Got a chunk.');

    if (res.pageInfo.hasNextPage) {
      let nextRatings = await getRatings(res.pageInfo.endCursor);
      return res.ratings.concat(nextRatings);
    } else {
      return res.ratings;
    }
  } catch (err) {
    console.error('Oops, something went wrong!', err);
  }
}

function createImportFile(ratings) {
  let out = 'Title, Year, Directors, WatchedDate, Rating, Review\n';

  ratings.forEach(r => {
    let director = '';
    let {
      review: { age, score, comment },
      item: { fullTitle, releaseYear, rt_info }
    } = r;

    rt_info ? (director = rt_info.director.name) : (director = '');

    let ageParts = age.split(' ');
    let ageOffset = JSON.parse(`{ "${ageParts[1]}" : ${ageParts[0]}}`);

    let watchedDate = DateTime.utc()
      .minus(ageOffset)
      .toFormat('yyyy-MM-dd');

    out += `"${fullTitle}",${releaseYear},"${director}",`;
    out += `${watchedDate},${score},"${comment}"\n`;
  });

  fs.writeFile('importMe.csv', out, 'utf8', err => {
    if (err) console.log(err);
    console.log('Import file created');
  });
}

getRatings()
  .then(ratings => {
    createImportFile(ratings);
  })
  .catch(err => console.error(err));
