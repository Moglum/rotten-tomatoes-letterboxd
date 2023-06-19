const rp = require("request-promise-native");
const fs = require("fs");
const { DateTime } = require("luxon");

const URI = "https://www.rottentomatoes.com/napi/profiles/ratings/{0}/tv?after=eyJyZWFsbV91c2VySWQiOiJSVF9kNDM5NTZiMS01MGI4LTQ3MjktOTcyOC1mZGMwODI1Mzc5ODUiLCJlbXNJZCI6IjhmZmNhYzQ5LTY5YWEtM2E0Yi05MGMxLWYxYTA5Y2NlZDQ5MCIsImNyZWF0ZURhdGUiOiIyMDIyLTExLTEyVDIwOjQzOjEzLjUyMFoifQ%3D%3D&pagecount=10
// const URI = "https://www.rottentomatoes.com/napi/userProfile/movieRatings/";

https://www.rottentomatoes.com/profiles/ratings/USER_ID/movie

// Change to your Rotten Tomatoes user ID
const USER_ID = process.env.ROTTEN_TOMATOES_ID;
const COOKIE = process.env.ROTTEN_TOMATOES_COOKIE;

async function getRatings(cursor) {
  try {
    let res = await rp({
      uri: URI + USER_ID,
      json: true,
      qs: {
        endCursor: cursor,
      },
      // headers: {
      //   cookie: COOKIE,
      // },
    });

    console.log("Got a chunk.");

    if (res.pageInfo.hasNextPage) {
      let nextRatings = await getRatings(res.pageInfo.endCursor);
      return res.ratings.concat(nextRatings);
    } else {
      return res.ratings;
    }
  } catch (err) {
    console.error("Oops, something went wrong!", err);
  }
}

function createImportFile(ratings) {
  let out = "Title, Year, Directors, WatchedDate, Rating, Review\n";

  ratings.forEach((r) => {
    if (!r) {
      return;
    }
    if (!r.displayName || r.displayName == "" || !r.item) {
      return;
    }

    let {
      review: { age, score, comment },
      item: { title, releaseYear, rt_info },
    } = r;

    let director = "";
    rt_info ? (director = rt_info.director.name) : (director = "");

    var date = new Date(age);
    var watchedDate =
      date.getFullYear() +
      "-" +
      (date.getMonth() + 1).toString().padStart(2, "0") +
      "-" +
      date.getDate().toString().padStart(2, "0");

    score = score || "";
    comment = comment || "";

    comment = comment.replace(/\n/g, "<br>");
    comment = comment.replace(/\"/g, '\\"');

    out += `"${title}",${releaseYear},"${director}",`;
    out += `${watchedDate},${score},"${comment}"\n`;
  });

  fs.writeFile("importMe.csv", out, "utf8", (err) => {
    if (err) console.log(err);
    console.log("Import file created - importMe.csv");
  });
}

getRatings()
  .then((ratings) => {
    fs.writeFileSync(
      "rawRatings.json",
      JSON.stringify(ratings, null, 2),
      "utf8"
    );
    console.log("Raw ratings file created - rawRatings.json");
    createImportFile(ratings);
  })
  .catch((err) => console.error(err));

// let ratings = JSON.parse(fs.readFileSync('rawRatings.json'))
// createImportFile(ratings)
