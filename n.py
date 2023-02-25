import pandas as pd
# read in test.data and train.data
# test有20000行，train有80000行
# 每行有4个，分别为 user id | movie id | rating | timestamp. 
test = pd.read_csv('test.data', sep='\t', header=None)
train = pd.read_csv('train.data', sep='\t', header=None)
print("initial test shape,train shape",test.shape, train.shape)

def clean_data(df):
    # sort by user id, movie id, and timestamp in ascending order
    df = df.sort_values(by=[0, 1, 3])
    # drop duplicates
    df = df.drop_duplicates(subset=[0, 1], keep='last')
    # clean missing ratings 
    df = df[df[2] != 0]
    return df
test = clean_data(test)
train = clean_data(train)
print("After cleaning test shape,train shape",test.shape, train.shape)

# 3
user_set = set(train[0])
test = test[test[0].isin(user_set)]
print("After cleaning2 test shape,train shape",test.shape, train.shape)

# 4
df = pd.read_csv('id_map.csv')
idmap = df.set_index('id_in_movielens')['id_in_metadata'].to_dict()
metadata = pd.read_csv('movies_metadata.csv', low_memory=False)
metaid = metadata['id'].unique()
# change the type of metaid to int and drop those cannot be converted
metaid = [int(i) for i in metaid if i.isnumeric()]
# extract two lists from df
idinmetadata = df['id_in_metadata'].unique()
idinmovielens = df['id_in_movielens'].unique()
# Get ids from train and test
trainid = train[1].unique()
testid = test[1].unique()
for i in trainid:
    if i not in idinmovielens:
        # drop those not in id_map
        train = train[train[1] != i]
    elif idmap[i] not in metaid:
        # drop those not in metadata
        train = train[train[1] != i]
for i in testid:
    if i not in idinmovielens:
        # drop those not in id_map
        test = test[test[1] != i]
    elif idmap[i] not in metaid:
        # drop those not in metadata
        test = test[test[1] != i]
print("After mapping test shape,train shape",test.shape, train.shape)

# 5
user_movie_count = train.groupby(0)[1].nunique().reset_index()
user_movie_count.columns = ['user_id', 'movie_count']

movie_rating_count = train.groupby(1)[2].count().reset_index()
movie_rating_count.columns = ['movie_id', 'rating_count']

# sort by movie_count in descending order
user_movie_count = user_movie_count.sort_values(by='movie_count', ascending=False)
# sort by rating_count in descending order
movie_rating_count = movie_rating_count.sort_values(by='rating_count', ascending=False)
print("Top 5 users with most movies:")
print(user_movie_count.head(5))
print("\nTop 5 movies with most ratings:")
print(movie_rating_count.head(5))