const rp = require('request-promise-native')
const fs = require('fs')
const { DateTime } = require('luxon')

async function getRatings(cursor) {
  try {
    const json = require('./input.json')
    return json.ratings
  } catch (err) {
    console.error('Oops, something went wrong!', err)
  }
}

function createImportFile(ratings) {
  let out = 'Title, Year, Directors, WatchedDate, Rating, Review\n'

  ratings.forEach(r => {
    if (!r) {
      return
    }
    if (!r.displayName || r.displayName == '' || !r.item) {
      return
    }

    let {
      review: { age, score, comment },
      item: { title, releaseYear, rt_info },
    } = r

    let director = ''
    rt_info ? (director = rt_info.director.name) : (director = '')

    let watchedDate = DateTime.fromFormat(age, 'MMM dd, yyyy')
      .toFormat('yyyy-MM-dd')

    score = score || ''

    if (comment === undefined) {
      comment = ""
    } else {
      comment = comment.replace(/\n/g, '<br>')
      comment = comment.replace(/\"/g, '\\"')
    }

    out += `"${title}",${releaseYear},"${director}",`
    out += `${watchedDate},${score},"${comment}"\n`
  })

  fs.writeFile('importMe.csv', out, 'utf8', err => {
    if (err) console.log(err)
    console.log('Import file created - importMe.csv')
  })
}

getRatings()
  .then(ratings => {
    fs.writeFileSync(
      'rawRatings.json',
      JSON.stringify(ratings, null, 2),
      'utf8'
    )
    console.log('Raw ratings file created - rawRatings.json')
    createImportFile(ratings)
  })
  .catch(err => console.error(err))

// let ratings = JSON.parse(fs.readFileSync('rawRatings.json'))
// createImportFile(ratings)
