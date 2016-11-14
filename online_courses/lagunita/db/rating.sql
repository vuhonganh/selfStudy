/* Delete the tables if they already exist */ 
DROP TABLE if exists Movie;

DROP TABLE if exists Reviewer;

DROP TABLE if exists Rating;

/* Create the schema for our tables */ 
CREATE TABLE Movie
(
  mID        INT,
  title      TEXT,
  YEAR       INT,
  director   TEXT
);

CREATE TABLE Reviewer
(
  rID    INT,
  name   TEXT
);

CREATE TABLE Rating
(
  rID          INT,
  mID          INT,
  stars        INT,
  ratingDate   DATE
);

/* Populate the tables with our data */ 
INSERT INTO Movie
VALUES
(
  101,
  'Gone with the Wind',
  1939,
  'Victor Fleming'
);

INSERT INTO Movie
VALUES
(
  102,
  'Star Wars',
  1977,
  'George Lucas'
);

INSERT INTO Movie
VALUES
(
  103,
  'The Sound of Music',
  1965,
  'Robert Wise'
);

INSERT INTO Movie
VALUES
(
  104,
  'E.T.',
  1982,
  'Steven Spielberg'
);

INSERT INTO Movie
VALUES
(
  105,
  'Titanic',
  1997,
  'James Cameron'
);

INSERT INTO Movie
VALUES
(
  106,
  'Snow White',
  1937,
  NULL
);

INSERT INTO Movie
VALUES
(
  107,
  'Avatar',
  2009,
  'James Cameron'
);

INSERT INTO Movie
VALUES
(
  108,
  'Raiders of the Lost Ark',
  1981,
  'Steven Spielberg'
);

INSERT INTO Reviewer
VALUES
(
  201,
  'Sarah Martinez'
);

INSERT INTO Reviewer
VALUES
(
  202,
  'Daniel Lewis'
);

INSERT INTO Reviewer
VALUES
(
  203,
  'Brittany Harris'
);

INSERT INTO Reviewer
VALUES
(
  204,
  'Mike Anderson'
);

INSERT INTO Reviewer
VALUES
(
  205,
  'Chris Jackson'
);

INSERT INTO Reviewer
VALUES
(
  206,
  'Elizabeth Thomas'
);

INSERT INTO Reviewer
VALUES
(
  207,
  'James Cameron'
);

INSERT INTO Reviewer
VALUES
(
  208,
  'Ashley White'
);

INSERT INTO Rating
VALUES
(
  201,
  101,
  2,
  '2011-01-22'
);

INSERT INTO Rating
VALUES
(
  201,
  101,
  4,
  '2011-01-27'
);

INSERT INTO Rating
VALUES
(
  202,
  106,
  4,
  NULL
);

INSERT INTO Rating
VALUES
(
  203,
  103,
  2,
  '2011-01-20'
);

INSERT INTO Rating
VALUES
(
  203,
  108,
  4,
  '2011-01-12'
);

INSERT INTO Rating
VALUES
(
  203,
  108,
  2,
  '2011-01-30'
);

INSERT INTO Rating
VALUES
(
  204,
  101,
  3,
  '2011-01-09'
);

INSERT INTO Rating
VALUES
(
  205,
  103,
  3,
  '2011-01-27'
);

INSERT INTO Rating
VALUES
(
  205,
  104,
  2,
  '2011-01-22'
);

INSERT INTO Rating
VALUES
(
  205,
  108,
  4,
  NULL
);

INSERT INTO Rating
VALUES
(
  206,
  107,
  3,
  '2011-01-15'
);

INSERT INTO Rating
VALUES
(
  206,
  106,
  5,
  '2011-01-19'
);

INSERT INTO Rating
VALUES
(
  207,
  107,
  5,
  '2011-01-20'
);

INSERT INTO Rating
VALUES
(
  208,
  104,
  3,
  '2011-01-02'
);

-- see all from Movie
SELECT *
FROM Movie;

-- Q1:  Find the titles of all movies directed by Steven Spielberg. 
SELECT title
FROM Movie
WHERE director = 'Steven Spielberg';

-- Q2: Find all years that have a movie that received a rating of 4 or 5, and sort them in increasing order. 
SELECT DISTINCT year
FROM Movie
  JOIN Rating USING (mID)
WHERE stars >= 4
ORDER BY year;

-- Q3: Find the titles of all movies that have no ratings. 
SELECT title
FROM Movie
WHERE mID NOT IN (SELECT mID FROM Rating);

SELECT *
FROM Rating;

--Q4: Some reviewers didn't provide a date with their rating. 
--Find the names of all reviewers who have ratings with a NULL value for the date. 
SELECT *
FROM Reviewer
  JOIN Rating USING (rID)
WHERE ratingDate IS NULL;

--Q5:Write a query to return the ratings data in a more readable format: reviewer name, movie title, stars, and ratingDate. 
--Also, sort the data, first by reviewer name, then by movie title, and lastly by number of stars.  
SELECT name,
       title,
       stars,
       ratingDate
FROM (Movie
  JOIN Rating ON Movie.mID = Rating.mID)
  JOIN Reviewer ON Rating.rID = Reviewer.rID
ORDER BY name,
         title,
         stars;

--Q6: For all cases where the same reviewer rated the same movie twice and gave it a higher rating the second time, 
--return the reviewer's name and the title of the movie. 
SELECT name,
       title
FROM Movie,
     Reviewer,
     (SELECT R1.rID,
             R1.mID
      FROM Rating R1,
           Rating R2
      WHERE R1.rID = R2.rID
      AND   R1.mID = R2.mID
      AND   R1.stars < R2.stars
      AND   R1.ratingDate < R2.ratingDate) Twice
WHERE Movie.mID = Twice.mID
AND   Reviewer.rID = Twice.rID;

-- Q7: For each movie that has at least one rating, 
-- find the highest number of stars that movie received. Return the movie title and number of stars. Sort by movie title.
SELECT title,
       MAX(stars)
FROM Movie
  JOIN Rating ON Movie.mID = Rating.mID
GROUP BY title
ORDER BY title;

-- Q8: For each movie, return the title and the 'rating spread', 
-- that is, the difference between highest and lowest ratings given to that movie. 
-- Sort by rating spread from highest to lowest, then by movie title. 
--for each movie, calculate the rating spread
SELECT title,
       MAX(stars) -MIN(stars) AS ratingSpread
FROM Movie
  JOIN Rating ON Movie.mID = Rating.mID
GROUP BY title
ORDER BY ratingSpread DESC,
         title;

-- Q9: Find the difference between the average rating of movies 
-- released before 1980 and the average rating of movies released after 1980. 
-- (Make sure to calculate the average rating for each movie, 
-- then the average of those averages for movies before 1980 and movies after. 
-- Don't just calculate the overall average rating before and after 1980.) 
-- break into small pieces: average for each movie 


SELECT ABS(S1.avgRatingAll - S2.avgRatingAll) AS diff
FROM (SELECT AVG(avgRating) AS avgRatingAll
      FROM (SELECT AVG(stars) AS avgRating
            FROM Movie
              JOIN Rating USING (mID)
            WHERE YEAR< 1980
            GROUP BY title,
                     YEAR) filmsBf1980) S1,
     (SELECT AVG(avgRating) AS avgRatingAll
      FROM (SELECT AVG(stars) AS avgRating
            FROM Movie
              JOIN Rating USING (mID)
            WHERE YEAR> 1980
            GROUP BY title,
                     YEAR) filmsAf1980) S2;


-- Extra Exercies of rating database:

-- Q1: Find the names of all reviewers who rated Gone with the Wind. 
SELECT DISTINCT name
FROM (Reviewer
  JOIN Rating USING (rID))
  JOIN Movie USING (mID)
WHERE title = 'Gone with the Wind';


-- Q2: For any rating where the reviewer is the same as the director of the movie,
-- return the reviewer name, movie title, and number of stars. 

SELECT name,
       title,
       stars
FROM (Movie
  JOIN Reviewer ON director = name)
  JOIN Rating USING (rID,mID);



-- Q3: Return all reviewer names and movie names together in a single list, alphabetized. 
-- (Sorting by the first name of the reviewer and first word in the title is fine; 
-- no need for special processing on last names or removing "The".) 

select name as a_name from Reviewer 
union 
select title as a_name from Movie
order by a_name;


-- q4: Find the titles of all movies not reviewed by Chris Jackson. 

-- below is a wrong approach because exclude rows with name Chris Jackson 
-- is not equivalent to find movies that not reviewed by him
SELECT title
FROM (Reviewer
  JOIN Rating USING (rID))
  JOIN Movie USING (mID)
WHERE name <> 'Chris Jackson';

-- correct approach: find mID of name reviewed by Chris Jackson, exclude these out of Movie table to get result
SELECT title
FROM Movie
WHERE mID NOT IN (SELECT mID
                  FROM Reviewer
                    JOIN Rating USING (rID)
                  WHERE name = 'Chris Jackson');

-- q5: For all pairs of reviewers such that both reviewers gave a rating to the same movie, 
-- return the names of both reviewers. Eliminate duplicates, don't pair reviewers with themselves, 
-- and include each pair only once. For each pair, return the names in the pair in alphabetical order. 

-- first find reviewer and title of rated movie

WITH PairReviewer AS
(
  SELECT name,
         title
  FROM (Reviewer
    JOIN Rating USING (rID))
    JOIN Movie USING (mID)
)
SELECT DISTINCT P1.name,
       P2.name
FROM PairReviewer P1
  JOIN PairReviewer P2 USING (title)
WHERE P1.name < P2.name;


-- to run on older version sqlite (can not avoid dupplication de code)
SELECT DISTINCT P1.name,
       P2.name
FROM (SELECT name,
             title
      FROM (Reviewer
        JOIN Rating USING (rID))
        JOIN Movie USING (mID)) P1
  JOIN (SELECT name,
               title
        FROM (Reviewer
          JOIN Rating USING (rID))
          JOIN Movie USING (mID)) P2 USING (title)
WHERE P1.name < P2.name;


-- Q6: For each rating that is the lowest (fewest stars) currently in the database, return the reviewer name, 
-- movie title, and number of stars. 

select name, title, stars
from ( Reviewer join Rating using(rID) ) join Movie using(mID)
where stars = (select min(stars) from Rating);

-- Q7: List movie titles and average ratings, from highest-rated to lowest-rated. 
-- If two or more movies have the same average rating, list them in alphabetical order. 

-- first find average rating of each movie
SELECT title,
       avg_stars
FROM (SELECT mID, AVG(stars) AS avg_stars FROM Rating GROUP BY mID) AS AvgRating
  JOIN Movie USING (mID)
ORDER BY avg_stars desc,
         title;


-- Q8: Find the names of all reviewers who have contributed three or more ratings.
-- (As an extra challenge, try writing the query without HAVING or without COUNT.) 

-- one reviewer <=> same rID, multiple ratings <=> 3 times (different in movie or rating dates)
SELECT name
FROM Reviewer
  JOIN (SELECT DISTINCT R1.rID
        FROM Rating R1,
             Rating R2,
             Rating R3
        WHERE R1.rID = R2.rID
        AND   (R1.mID <> R2.mID OR R1.ratingDate <> R2.ratingDate)
        AND   R1.rID = R3.rID
        AND   (R1.mID <> R3.mID OR R1.ratingDate <> R3.ratingDate)
        AND   (R2.mID <> R3.mID OR R2.ratingDate <> R3.ratingDate)) Contributer USING (rID);


-- Q9: Some directors directed more than one movie. 
-- For all such directors, return the titles of all movies directed by them, along with the director name. 
-- Sort by director name, then movie title.
-- (As an extra challenge, try writing the query both with and without COUNT.)

-- with COUNT ver:
SELECT title,
       director
FROM Movie
  JOIN (SELECT director
        FROM Movie
        GROUP BY director
        HAVING COUNT(mID) > 1) AS GoodDir USING (director)
ORDER BY director,
         title;


-- without COUNT ver:
SELECT M2.title,
       M2.director
FROM Movie M1
  JOIN Movie M2
    ON (M1.mID <> M2.mID
   AND M1.director = M2.director)
ORDER BY M2.director,
         M2.title;


-- q10: Find the movie(s) with the highest average rating. Return the movie title(s) and average rating. 
-- (Hint: This query is more difficult to write in SQLite than other systems; you might 
-- think of it as finding the highest average rating and then choosing the movie(s) with that average rating.) 

-- sqlite ver:
SELECT title,
       cur_avg_rating
FROM (SELECT mID,
             AVG(stars) AS cur_avg_rating
      FROM Rating
      GROUP BY mID) CurAvgRating
  JOIN Movie USING (mID)
WHERE cur_avg_rating = (SELECT MAX(avg_rating) AS highest_avg_rating
                        FROM (SELECT mID, AVG(stars) AS avg_rating FROM Rating GROUP BY mID) AS AvgRating);




-- postgre ver:
WITH AvgRating AS
(
  SELECT mID,
         AVG(stars) AS cur_avg_rating
  FROM Rating
  GROUP BY mID
)
SELECT title,
       cur_avg_rating
FROM AvgRating
  JOIN Movie USING (mID)
WHERE cur_avg_rating >= ALL (SELECT cur_avg_rating FROM AvgRating);


-- q11: Find the movie(s) with the lowest average rating. Return the movie title(s) and average rating. 
WITH AvgRating AS
(
  SELECT mID,
         AVG(stars) AS cur_avg_rating
  FROM Rating
  GROUP BY mID
)
SELECT title,
       cur_avg_rating
FROM AvgRating
  JOIN Movie USING (mID)
WHERE cur_avg_rating <= ALL (SELECT cur_avg_rating FROM AvgRating);


-- q12:
-- For each director, return the director's name
-- together with the title(s) of the movie(s) they directed that received the 
-- highest rating among all of their movies, and the value of that rating. Ignore movies whose director is NULL. 

SELECT DISTINCT Movie.director,
       Movie.title,
       stars
FROM Movie
  JOIN Rating USING (mID)
  JOIN (SELECT director,
               MAX(stars) AS max_stars
        FROM Movie
          JOIN Rating USING (mID)
        WHERE director IS NOT NULL
        GROUP BY director) AS DirHighestRating
    ON Movie.director = DirHighestRating.director
   AND Rating.stars = DirHighestRating.max_stars;


