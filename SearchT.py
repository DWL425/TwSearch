import datetime
import GetOldTweets3 as got
import time
from random import uniform
from tqdm import tqdm_notebook

days_range = []

start = datetime.datetime.strptime("2014-04-16", "%Y-%m-%d")
end = datetime.datetime.strptime("2014-04-18", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("==={} 부터 {} 까지===".format(days_range[0], days_range[-1]))
print("==={}일===".format(len(days_range)))




start_date = days_range[0]
end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


tweetCriteria = got.manager.TweetCriteria().setQuerySearch('세월호')\
                                           .setSince(start_date)\
                                           .setUntil(end_date)\
                                           .setMaxTweets(-1)\


print("===시작===")
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
start_time = time.time()
print(tweet.text)

print("=== 끝 {0:0.2f} Minutes ===".format((time.time() - start_time)/60))
print("=== 총 {} 개===".format(len(tweet)))

tweet_list = []

for index in tqdm_notebook(tweet):
    username = index.username
    link = index.permalink
    content = index.text
    tweet_date = index.date.strftime("%Y-%m-%d")
    tweet_time = index.date.strftime("%H:%M:%S")
    retweets = index.retweets
    favorites = index.favorites

    try:
        personal_link = 'https://twitter.com/' + username
        bs_obj = get_bs_obj(personal_link)
        uls = bs_obj.find("ul", {"class": "ProfileNav-list"}).find_all("li")
        div = bs_obj.find("div", {"class": "ProfileHeaderCard-joinDate"}).find_all("span")[1]["title"]

        joined_date = div.split('-')[1].strip()
        num_tweets = uls[0].find("span", {"class": "ProfileNav-value"}).text.strip()
        num_following = uls[1].find("span", {"class": "ProfileNav-value"}).text.strip()
        num_follower = uls[2].find("span", {"class": "ProfileNav-value"}).text.strip()

    except AttributeError:
        print("=== Attribute error occurs at {} ===".format(link))
        print("link : {}".format(personal_link))
        pass

    info_list = [tweet_date, tweet_time, username, content, link, retweets, favorites,
                 joined_date, num_tweets, num_following, num_follower]
    tweet_list.append(info_list)

    time.sleep(uniform(1, 2))

    import pandas as pd

    twitter_df = pd.DataFrame(tweet_list,
                              columns=["date", "time", "user_name", "text", "link", "retweet_counts", "favorite_counts",
                                       "user_created", "user_tweets", "user_followings", "user_followers"])

    twitter_df.to_csv("sample_twitter_data_{}_to_{}.csv".format(days_range[0], days_range[-1]), index=False)
    print("=== {} 저장완료 ===".format(len(tweet_list)))