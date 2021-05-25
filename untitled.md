Og Feature set for clustering

- ~~acousticness (`exponential`)~~
- danceability
- energy
- liveness
- ~~loudness (`exponential`, skewed)~~
- ~~speechiness (`exponential`)~~
- tempo
- valence

# I removed all the above features which had exponential like distribution!

### Why?

The exponential distribution means that most(or almost) most of the points are clustered around min value of distribution, this this kind of distribution of data in 5-Dimensional data will create a lot of problem while clustering.